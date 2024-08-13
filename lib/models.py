from typing import List, Optional, Union

from pydantic import BaseModel


class MessageEvent(BaseModel):
    id: int
    date: int
    peer_id: int
    from_id: int
    text: str
    attachments: List[Union[dict, str]] = []
    conversation_message_id: Optional[int] = None
    fwd_messages: List[dict] = []
    important: bool = False
    is_hidden: bool = False
    random_id: Optional[int] = None
    reply_message: Optional[dict] = None

    @classmethod
    def from_update(cls, data: dict):
        return cls(**data)
