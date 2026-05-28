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

        text = transcript.lower().strip()

        # ====================================
        # TERMINATION STATES
        # ====================================

        if intent == IntentType.ANGRY:

            return ConversationState.CALL_END

        if any(word in text for word in [

            # English
            "bye",
            "goodbye",
            "thank you",
            "thanks",
            "end call",
            "that's all",

            # Hindi
            "धन्यवाद",
            "ठीक है धन्यवाद",
            "कॉल खत्म",

            # Hinglish
            "thank you bhai",
            "call end karo"

        ]):

            return ConversationState.CALL_END

        # ====================================
        # CALLBACK BOOKING
        # ====================================

        if intent == IntentType.CALLBACK:

            return ConversationState.CALLBACK_BOOKING

        if any(word in text for word in [

            # English
            "call later",
            "callback",
            "busy now",
            "call tomorrow",
            "call me later",

            # Hindi
            "बाद में कॉल करना",
            "कल कॉल करना",
            "अभी बिजी हूं",

            # Hinglish
            "baad mein call karo",
            "kal call karna",
            "abhi busy hoon"

        ]):

            return ConversationState.CALLBACK_BOOKING
        
        if intent == IntentType.ESCALATION_REQUEST:

          return ConversationState.ESCALATION

        # ====================================
        # HIGH VALUE LEADS
        # ====================================

        if intent == IntentType.HIGH_TICKET:

            return ConversationState.ESCALATION

        # ====================================
        # INTERESTED → ELIGIBILITY
        # ====================================

        if intent == IntentType.INTERESTED:

            return ConversationState.ELIGIBILITY

        # ====================================
        # EMI QUERY
        # ====================================

        if intent == IntentType.EMI_QUERY:

            return ConversationState.EMI_QUERY

        # ====================================
        # DOCUMENT QUERY
        # ====================================

        if intent == IntentType.DOCUMENT_QUERY:

            return ConversationState.DOCUMENT_REMINDER

        # ====================================
        # CONFUSED USER
        # ====================================

        if intent == IntentType.CONFUSED:

            return ConversationState.OBJECTION_HANDLING

        # ====================================
        # DEFAULT
        # ====================================

        return current_state