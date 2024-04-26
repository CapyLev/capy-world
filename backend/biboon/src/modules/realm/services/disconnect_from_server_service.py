from src.utils.singlton_meta import SingletonMeta


class DisconnectFromServerService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        pass

    async def execute(self) -> None:
        pass


disconnect_from_server_service = DisconnectFromServerService()
