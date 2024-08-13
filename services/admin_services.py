from sqlalchemy.orm.session import Session
from models.admin_model import AdminModel
from models.auth_model import AuthModel
from uuid import uuid4


class AdminServices:

    def __init__(self, session: Session):
        self.session = session
        self.create_admin()

    def create_admin(self) -> None:
        try:
            admin_create = AdminModel(
                id=uuid4(),
                name="Admin",
                lastname="Admin",
                occupation="Admin"
            )
            auth_create = AuthModel(
                id=uuid4(),
                admin_id=admin_create.id,
                email="admin@gmail.com",
                password="admintrustpwd",
                role="ADMINISTRATOR"
            )

            self.session.add(admin_create)
            self.session.add(auth_create)
            self.session.commit()

        except:
            pass
