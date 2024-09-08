from services.stack_services import StackServices
from utils.config_orm import SessionLocal
from tasks.email_task import mail_sender
from utils.load_statics import load_appt_reminder
from utils.celery_config import app
from datetime import datetime


@app.task
def check_table_stack():
    stack = StackServices(SessionLocal())

    for record in stack.get_stacks():
        try:
            appt: tuple = stack.get_appointment(record.appointment_id)
            appt_date, today = appt[0].timestamp.date(), datetime.now().date()
            formatted_time = appt[0].timestamp.strftime("%I:%M %p")
            diff = appt_date - today

            if diff.days == 1:
                mail_sender(
                    load_appt_reminder(
                        issue=appt[0].issue,
                        price=appt[0].price,
                        timestamp=appt_date,
                        created_at=appt[0].created_at.date(),
                        pet=appt[2].name,
                        user=appt[1].email,
                        time=formatted_time
                    ),
                    "Recordatorio de Cita",
                    appt[1].email
                )

        except AttributeError as e:
            stack.delete_stack(record)

        except Exception as e:
            print(e)
