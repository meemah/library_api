
from .user_service import UserService
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from src.db.main import get_session
from fastapi import Depends
from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.user.schema import UserSchema, UserCreateSchema, UserLoginSchema
from src.db.models import UserModel
from src.utils.password_util import verify_password
user_router = InferringRouter()

@cbv(user_router)
class UserRoutes:
    user_service = UserService()
    @user_router.get("/",response_model=UserSchema)
    async def get_user(self,  session: AsyncSession = Depends(get_session) ):
        user = await self.user_service.get_user(session,"test@getnada.com")
        if(user is not None):
            return {"message":"Welcome"}
        else:
            raise HTTPException(detail="Couldnt find",status_code=status.HTTP_404_NOT_FOUND)
    
    @user_router.post("/create_account", response_model=UserModel,status_code=status.HTTP_201_CREATED)
    async def create_account(self,
            user_create_schema:UserCreateSchema,
            session: AsyncSession = Depends(get_session)):
        if await self.user_service.does_user_exist(session, user_create_schema.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User Exist")
        else:
          user = await self.user_service.create_account(session,user_create_schema,)
          return JSONResponse(
              status_code=status.HTTP_201_CREATED,
              content={
                  "message":"Account created",
                #   "data":  user.model_dump()
              }
          )
            
    @user_router.post("/login", response_model=UserModel)
    async def login(
        self,
        login_details: UserLoginSchema, 
                    session: AsyncSession = Depends(get_session)
                    ):
        user = await self.user_service.get_user(session=session, email=login_details.email)
        if user is not None:
            is_password_valid = verify_password(login_details.password, user.password)
            if is_password_valid:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "message": "Login Successful"
                    }
                )
            else:
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User doesnt exist/password is incorrect"
            )
        
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User doesnt exist/password is incorrect"
            )


       