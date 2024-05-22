from services.pet_services import PetServices


class PetController:

    def __init__(self) -> None:
        self.pet = PetServices()

    def create_pet(self, user_id: str, pet_data: dict) -> None:
        self.pet.create_pet(user_id, pet_data)

    def get_pets(self, user_id: str) -> list[dict]:
        return self.pet.get_pets(user_id)

    def get_pet(self, user_id: str, pet_id: str) -> dict:
        return self.pet.get_pet(user_id, pet_id)

    def update_pet(self, user_id: str, pet_id: str, pet_data: dict) -> None:
        self.pet.update_pet(user_id, pet_id, pet_data)

    def delete_pet(self, user_id: str, pet_id: str) -> None:
        self.pet.delete_pet(user_id, pet_id)
