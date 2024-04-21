from typing import Type

import beanie
from motor.motor_asyncio import AsyncIOMotorClient

from .constants import constants


class Storage:
    @staticmethod
    async def initialize(documents: list[Type[beanie.Document]]) -> None:
        client = AsyncIOMotorClient(constants.mongodb.MONGO_URL)
        await beanie.init_beanie(
            database=client[constants.mongodb.MONGO_NAME],
            document_models=documents,
        )
