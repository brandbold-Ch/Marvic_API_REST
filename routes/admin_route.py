from controllers.admin_controller import AdminControllers
from utils.config_orm import SessionLocal
from fastapi import APIRouter


admin = APIRouter()
admin_controller = AdminControllers(SessionLocal())
