from services.stack_services import StackServices
from utils.config_orm import SessionLocal
from tasks.email_task import mail_sender
from utils.load_statics import load_reminder_appt_tmpl
from utils.celery_config import app
from datetime import datetime


@app.task
def check_table_stack():
    stack = StackServices(SessionLocal())

    for record in stack.get_stacks():
        try:
            appt: tuple = stack.get_appointment(record.appointment_id)
            diff = appt[0].timestamp.date() - datetime.now().date()

            if diff.days == 1:
                mail_sender(
                    load_reminder_appt_tmpl(
                        issue=appt[0].issue,
                        price=appt[0].price,
                        timestamp=appt[0].timestamp.strftime("%Y-%m-%d %I:%M:%S %p"),
                        created_at=appt[0].created_at.strftime("%Y-%m-%d %I:%M:%S %p"),
                        pet=appt[2].name,
                        user=appt[1].email
                    ),
                    "Recordatorio de Cita",
                    appt[1].email
                )

        except AttributeError as e:
            stack.delete_stack(record)

        except Exception as e:
            print(e)
