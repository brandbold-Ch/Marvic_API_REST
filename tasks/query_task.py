from services.stack_services import StackServices
from utils.notify_email import notify_user
from utils.config_orm import SessionLocal
from utils.celery_config import app
from datetime import datetime


@app.task
def check_table_stack():
    stack = StackServices(SessionLocal())

    for record in stack.get_stacks():
        try:
            data: tuple = stack.get_appointment(record.appointment_id)
            
            if None in data:
                stack.delete_stack(record)
                return
            
            else:    
                appt_data, pet_data, auth_data = data
                diff = (appt_data.timestamp.date() - datetime.now().date()).days

                if appt_data.expired == True:
                    stack.delete_stack(record)
                    return
            
                elif diff in [0, 1]:
                    notify_user(
                        issue=appt_data.issue,
                        price=appt_data.price,
                        timestamp=appt_data.timestamp.strftime("%Y-%m-%d %I:%M:%S %p"),
                        created_at=appt_data.created_at.strftime("%Y-%m-%d %I:%M:%S %p"),
                        pet_name=pet_data.name,
                        user_email=auth_data.email,
                        pet_id=pet_data.id
                    )
                    appt_data.expired = True
                    stack.update_appointment(appt_data)
                    stack.delete_stack(record)

        except Exception:
            stack.delete_stack(record)
