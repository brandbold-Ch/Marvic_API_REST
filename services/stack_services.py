from decorators.error_decorators import handle_exceptions
from models.stack_model import StackModel
from utils.config_orm import SessionLocal
from sqlalchemy.orm import Session


class StackServices:

    def __init__(self, session: Session = SessionLocal()):
        self.session = session

    @handle_exceptions
    def get_stack(self, stack_id: str) -> dict | None:
        stack = self.session.get(StackModel, stack_id)
        if stack is not None:
            return {
                "ref": stack,
                "parsed": stack.to_dict()
            }

    @handle_exceptions
    def get_stacks(self) -> list:
        stacks = self.session.query(StackModel).all()
        return stacks

    @handle_exceptions
    def delete_stack(self, stack_id: str) -> None:
        stack = self.get_stack(stack_id)["ref"]
        self.session.delete(stack)
        self.session.commit()
