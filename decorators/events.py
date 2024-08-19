from models.appointment_model import AppointmentModel
from utils.load_statics import load_admin_appt_tmpl
from utils.email_server import mail_sender
from typing import Callable


def event_email(func: Callable) -> Callable:
    def wrapper(self, **kwargs):
        print(kwargs.get("object_result"))
        appt_data: AppointmentModel = kwargs.get("object_result")
        mail_sender(
            load_admin_appt_tmpl(
                appt_id=str(appt_data.id),
                issue=appt_data.issue,
                created_at=str(appt_data.created_at),
                timestamp=str(appt_data.timestamp)
            ),
            "Nueva cita agendada",
            "jaredbrandon970@gmail.com"
        )
        return func(self, **kwargs)
    return wrapper
