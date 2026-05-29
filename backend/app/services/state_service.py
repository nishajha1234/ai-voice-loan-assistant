from app.core.constants import (
    ConversationState,
    IntentType
)


class StateService:

    @staticmethod
    def determine_next_state(
        current_state,
        intent,
        transcript=""
    ):

        if (
            current_state
            == ConversationState.CALL_END
        ):

            return ConversationState.CALL_END

        text = transcript.lower().strip()

        if intent == IntentType.ANGRY:

            return ConversationState.CALL_END

        if any(word in text for word in [
            "bye",
            "goodbye",
            "thank you",
            "thanks",
            "end call",
            "that's all",
            "धन्यवाद",
            "ठीक है धन्यवाद",
            "कॉल खत्म",
            "thank you bhai",
            "call end karo"

        ]):

            return ConversationState.CALL_END

        if intent == IntentType.CALLBACK:

            return ConversationState.CALLBACK_BOOKING

        if any(word in text for word in [
            "call later",
            "callback",
            "busy now",
            "call tomorrow",
            "call me later",
            "बाद में कॉल करना",
            "कल कॉल करना",
            "अभी बिजी हूं",
            "baad mein call karo",
            "kal call karna",
            "abhi busy hoon"

        ]):

            return ConversationState.CALLBACK_BOOKING

        if intent == IntentType.ESCALATION_REQUEST:

            return ConversationState.ESCALATION

        if intent == IntentType.HIGH_TICKET:

            return ConversationState.ESCALATION

        if intent == IntentType.INTERESTED:

            return ConversationState.ELIGIBILITY

        if intent == IntentType.EMI_QUERY:

            return ConversationState.EMI_QUERY

        if intent == IntentType.DOCUMENT_QUERY:

            return ConversationState.DOCUMENT_REMINDER

        if intent == IntentType.CONFUSED:

            return ConversationState.OBJECTION_HANDLING

        return current_state