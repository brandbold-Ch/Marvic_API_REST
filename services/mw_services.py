from errors.exception_classes import DoesNotExistInDatabase, InvalidUUID
from models.quote_model import QuoteModel
from models.user_model import UserModel
from sqlalchemy.exc import DataError
from models.pet_model import PetModel
from utils.config_orm import Session


class MWServices:

    def __init__(self):
        self.session = Session()

    def get_user(self, user_id: str) -> None:
        try:
            user = self.session.query(UserModel).get(user_id)
            if user is None:
                raise DoesNotExistInDatabase("The user does not exist ❌")

        except DataError:
            raise InvalidUUID("UUID with invalid format 🆔")

    def get_pet(self, pet_id: str) -> None:
        try:
            pet = self.session.query(PetModel).get(pet_id)
            if pet is None:
                raise DoesNotExistInDatabase("The pet does not exist ❌")

        except DataError:
            raise InvalidUUID("UUID with invalid format 🆔")

    def get_quote(self, quote_id: str) -> None:
        try:
            quote = self.session.query(QuoteModel).get(quote_id)
            if quote is None:
                raise DoesNotExistInDatabase("The quote does not exist ❌")

        except DataError:
            raise InvalidUUID("UUID with invalid format 🆔")

