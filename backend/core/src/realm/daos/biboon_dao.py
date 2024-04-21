class BiboonDAO:
    class BiboonDAOError(Exception):
        pass

    def send_welcome_message(
        self,
        server_id: int,
        user_id: int,
    ) -> None:
