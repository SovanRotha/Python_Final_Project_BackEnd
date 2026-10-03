from fastapi import HTTPException

from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.ai.ai_conversation import AIConversation
from app.models.ai.ai_message import AIMessage
from app.services.ai_service import AIService


class AIMessageController(ScopedResourceController):
    model = AIMessage
    resource_name = "AI message"
    set_user_id = False

    def owner_filter(self):
        return AIMessage.conversation.has(
            AIConversation.user_id == self.user.id
        )

    def validate_create(self, fields: dict) -> None:
        self.require_owned(
            self.db.query(AIConversation).filter(
                AIConversation.id == fields["conversation_id"],
                AIConversation.user_id == self.user.id,
            ),
            "AI conversation",
        )

    def send_message(
        self,
        conversation_id: int,
        message: str,
    ):
        conversation = self.require_owned(
            self.db.query(AIConversation).filter(
                AIConversation.id == conversation_id,
                AIConversation.user_id == self.user.id,
            ),
            "AI conversation",
        )

        user_message = AIMessage(
            conversation_id=conversation_id,
            role="user",
            message=message,
        )
        self.db.add(user_message)
        self.db.flush()

        prior_messages = (
            self.db.query(AIMessage)
            .filter(
                AIMessage.conversation_id == conversation_id,
                AIMessage.id != user_message.id,
            )
            .order_by(AIMessage.created_at, AIMessage.id)
            .all()
        )
        trip_context = ""
        if conversation.trip is not None:
            trip = conversation.trip
            trip_context = (
                f" The user is planning {trip.name} to "
                f"{trip.destination.name}, from {trip.start_date} to "
                f"{trip.end_date}, using {trip.currency}."
            )
        prompt_messages = [
            {
                "role": "system",
                "content": (
                    "You are TripOS, a helpful travel-planning assistant. "
                    "Give practical, clear answers and ask a concise follow-up "
                    "when important trip details are missing."
                    f"{trip_context}"
                ),
            },
            *[
                {"role": item.role.value, "content": item.message}
                for item in prior_messages
            ],
            {"role": "user", "content": message},
        ]

        try:
            response = AIService().generate_response(prompt_messages)
        except HTTPException:
            self.db.rollback()
            raise

        assistant_message = AIMessage(
            conversation_id=conversation_id,
            role="assistant",
            message=response,
        )
        self.db.add(assistant_message)
        self.db.commit()
        self.db.refresh(user_message)
        self.db.refresh(assistant_message)
        return {
            "user_message": user_message,
            "assistant_message": assistant_message,
        }