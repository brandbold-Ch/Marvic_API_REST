from services.quote_services import QuoteServices


class QuoteControllers:

    def __init__(self) -> None:
        self.service = QuoteServices()

    def create_quote(self, user_id: str, pet_id: str, quote_data: dict) -> None:
        self.service.create_quote(user_id, pet_id, quote_data)

    def get_quote(self, user_id: str, quote_id: str, pet_id: str) -> dict:
        return self.service.get_quote(user_id, quote_id, pet_id)

    def get_quotes(self, user_id: str, pet_id: str) -> list[dict]:
        return self.service.get_quotes(user_id, pet_id)

    def delete_quotes(self, user_id: str, quote_id: str, pet_id: str) -> None:
        self.service.delete_quotes(user_id, quote_id, pet_id)
