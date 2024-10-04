from services.pet_services import PetServices
from sqlalchemy.orm import Session


class PetController:

    def __init__(self, session: Session) -> None:
        self.pet = PetServices(session)

    async def create_pet(self, **kwargs) -> dict:
        return await self.pet.create_pet(**kwargs)

    def get_pets(self, **kwargs) -> list[dict]:
        return self.pet.get_pets(**kwargs)

    def get_pet(self, **kwargs) -> dict:
        return self.pet.get_pet(**kwargs)

    async def update_pet(self, **kwargs) -> dict:
        return await self.pet.update_pet(**kwargs)

    def delete_pet(self, **kwargs) -> None:
        self.pet.delete_pet(**kwargs)

    def delete_image(self, **kwargs) -> None:
        self.pet.delete_image(**kwargs)