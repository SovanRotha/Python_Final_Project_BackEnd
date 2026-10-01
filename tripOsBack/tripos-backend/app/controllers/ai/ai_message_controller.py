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
        self.require_owned(
            self.db.query(AIConversation).filter(
                AIConversation.id == conversation_id,
                AIConversation.user_id == self.user.id,
            ),
            "AI conversation",
        )

        # 1. Save user's message
        user_message = AIMessage(
            conversation_id=conversation_id,
            role="user",
            message=message,
        )

        self.db.add(user_message)
        self.db.flush()

        # 2. Send message to OpenAI
        ai_service = AIService()

        response = ai_service.generate_response(message)

        # 3. Save AI response
        assistant_message = AIMessage(
            conversation_id=conversation_id,
            role="assistant",
            message=response,
        )

        self.db.add(assistant_message)
        self.db.commit()

        return assistant_message