from services.admin_services import AdminServices
from sqlalchemy.orm import Session


class AdminControllers:

    def __init__(self, session: Session) -> None:
        self.admin = AdminServices(session)
