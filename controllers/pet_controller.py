from services.pet_services import PetServices
from sqlalchemy.orm import Session


class PetController:

    def __init__(self, session: Session) -> None:
        self.pet = PetServices(session)

    async def create_pet(self, user_id: str, pet_data: dict) -> dict:
        return await self.pet.create_pet(user_id, pet_data)

    def get_pets(self, user_id: str) -> list[dict]:
        return self.pet.get_pets(user_id)

    def get_pet(self, user_id: str, pet_id: str) -> dict:
        return self.pet.get_pet(user_id, pet_id)

    async def update_pet(self, user_id: str, pet_id: str, pet_data: dict) -> dict:
        return await self.pet.update_pet(user_id, pet_id, pet_data)

    def delete_pet(self, user_id: str, pet_id: str) -> None:
        self.pet.delete_pet(user_id, pet_id)
