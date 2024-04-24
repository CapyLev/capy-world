from src.utils.singlton_meta import SingletonMeta


class BroadcastService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        pass

    def execute(self) -> None:
        pass


broadcast_service = BroadcastService()
