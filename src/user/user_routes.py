
from .user_service import UserService


from src.db.main import get_session
from fastapi import Depends,status,APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession
from src.user.schema import  UserCreateSchema, UserLoginSchema
from src.db.models import UserModel
from src.utils.password_util import verify_password
from src.utils.response.error import UserAlreadyExists,InvalidCredentials, UserNotFound, ContactSupport
from src.utils.response.success import SuccessResponse
from src.utils.token_util import create_access_token
from src.utils.redis import add_jti_to_blocklist

from datetime import timedelta
from src.utils.token_bearer import get_user,AccessToken
user_router = APIRouter()



    
@user_router.post("/create_account", response_model=SuccessResponse[UserModel],status_code=status.HTTP_201_CREATED)
async def create_account(
            user_create_schema:UserCreateSchema,
            session: AsyncSession = Depends(get_session)):
        if await UserService.does_user_exist(session, user_create_schema.email):
            raise UserAlreadyExists()
        else:
          user = await UserService.create_account(session,user_create_schema,)
          return SuccessResponse(
              message="Account created",
              data=user
          )
    
            
@user_router.post("/login",response_model=SuccessResponse)
async def login(
        login_details: UserLoginSchema, 
        session: AsyncSession = Depends(get_session)):
        user = await UserService.get_user(session=session, email=login_details.email)
        if user is not None:
            is_password_valid = verify_password(login_details.password, user.password)
            if is_password_valid:
                access_token = create_access_token(user=user)
                refresh_token = create_access_token(user=user,refresh=True,expiry=timedelta(2))
                return  SuccessResponse(
                    message =  "Login Successful",
                    data={
                        "user":user.model_dump(),
                        "access_token": access_token,
                        "refresh_token": refresh_token
                      },
                    
                )
            else:
                raise InvalidCredentials()
        else:
            raise InvalidCredentials()
        
    
@user_router.get("/me")
async def get_my_profile(

        user_model: UserModel = Depends(get_user)
        
    ):
        if user_model is not None:
            return SuccessResponse(
                message= "Profile Fetched",
                data=user_model
            )
        else:
            raise UserNotFound()
    
@user_router.get("/logout")
async def logout(
        token_details=Depends(AccessToken)
    ):   
        jti = token_details["jti"]
        if jti is not None:
            add_jti_to_blocklist(jti)
            return SuccessResponse(
                message="Logout successful"
            )
        else: 
            raise ContactSupport()
        
            
        



       