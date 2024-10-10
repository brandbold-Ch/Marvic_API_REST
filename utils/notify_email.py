from services.admin_services import AdminServices
from utils.config_orm import SessionLocal
from tasks.email_task import mail_sender
from utils.load_statics import (
    load_admin_appt_tmpl, 
    load_reminder_appt_tmpl
)


def notify_admin(**kwargs) -> None:
    admin = AdminServices(SessionLocal()).get_unique_admin()
    
    mail_sender.delay(
        load_admin_appt_tmpl(
            admin=admin["name"],
            appt_id=kwargs.get("appt_id"),
            issue=kwargs.get("issue"),
            created_at=kwargs.get("created_at"),
            timestamp=kwargs.get("timestamp"),
            price=kwargs.get("price")
        ),
        "Nueva cita agendada",
        admin["auth_data"]["email"]
    )


def notify_user(**kwargs) -> None:
    mail_sender(
        load_reminder_appt_tmpl(
            issue=kwargs.get("issue"),
            price=kwargs.get("price"),
            timestamp=kwargs.get("timestamp"),
            created_at=kwargs.get("created_at"),
            pet_name=kwargs.get("pet_name"),
            user_name=kwargs.get("user_email"),
            pet_id=kwargs.get("pet_id")
        ),
        "Recordatorio de Cita",
        kwargs.get("user_email")
    )
