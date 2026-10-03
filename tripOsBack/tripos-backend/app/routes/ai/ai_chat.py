from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.controllers.ai.ai_message_controller import AIMessageController
from app.core.database import get_db
from app.models.user.user import User
from app.schemas.ai.ai_message import AIChatSendRequest, AIChatSendResponse

router = APIRouter(
    prefix="/api/v1/ai/conversations",
    tags=["AI chat"],
)


@router.post(
    "/{conversation_id}/messages",
    response_model=AIChatSendResponse,
)
def send_message(
    conversation_id: int,
    payload: AIChatSendRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AIMessageController(db, current_user).send_message(
        conversation_id,
        payload.message,
    )
