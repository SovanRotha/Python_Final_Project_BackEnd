from app.controllers.common.scoped_resource_controller import ScopedResourceController
from app.models.ai.ai_conversation import AIConversation
from app.models.ai.ai_message import AIMessage


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