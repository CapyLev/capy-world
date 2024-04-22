from config.message_transmitter import MessageDTO
from src.modules.realm.models import MessageDocument


async def convert_msg_document_to_transmitter_dto(msg: MessageDocument) -> MessageDTO:
    return MessageDTO(
            server_id=msg.server_id,
            user_id=msg.user_id,
            content=msg.content,
            attachments=msg.attachments,
            created_at=msg.created_at,
        )