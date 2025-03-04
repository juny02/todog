class TokenMapper:

    @staticmethod
    def user_id_to_access_token_key(user_id: str) -> str:
        return user_id + ":access_token"

    @staticmethod
    def user_id_to_refresh_token_key(user_id: str) -> str:
        return user_id + ":refresh_token"