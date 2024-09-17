from services.stack_services import StackServices
from utils.notify_email import notify_user
from utils.config_orm import SessionLocal
from tasks.email_task import mail_sender
from utils.celery_config import app
from datetime import datetime


@app.task
def check_table_stack():
    stack = StackServices(SessionLocal())

    for record in stack.get_stacks():
        try:
            appt: tuple = stack.get_appointment(record.appointment_id)
            diff = appt[0].timestamp.date() - datetime.now().date()

            if diff.days == 1 or diff.days == 0:
                notify_user(
                    issue=appt[0].issue,
                    price=appt[0].price,
                    timestamp=appt[0].timestamp.strftime("%Y-%m-%d %I:%M:%S %p"),
                    created_at=appt[0].created_at.strftime("%Y-%m-%d %I:%M:%S %p"),
                    pet=appt[2].name,
                    user=appt[1].email,
                    addressee=appt[1].email
                )
                appt[0].expired = True
                stack.update_appointment(appt[0])
                stack.delete_stack(record)

        except AttributeError as e:
            stack.delete_stack(record)

        except Exception as e:
            print(e)
