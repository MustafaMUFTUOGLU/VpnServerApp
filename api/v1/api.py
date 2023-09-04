from fastapi import APIRouter
from api.v1.endpoints import login, users, otps, email, file
from websocket.wbsocket import IncomingConnection


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
# api_router.include_router(forms.router, prefix="/forms", tags=["forms"])
api_router.include_router(otps.router, prefix="/otp", tags=["otps"])
# api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(email.router, prefix="/email", tags=["email"])
api_router.include_router(file.router, prefix="/file", tags=["file"])
# api_router.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])
		
 

