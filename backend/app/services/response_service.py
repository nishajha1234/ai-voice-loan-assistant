from app.core.constants import (
    ConversationState,
    IntentType
)


class ResponseService:

    @staticmethod
    def generate_response(
        intent,
        state,
        transcript=""
    ):

        # ====================================
        # TERMINAL STATES
        # ====================================

        if state == ConversationState.CALL_END:

            return (
                "Thank you for your time. "
                "Have a great day."
            )

        if state == ConversationState.ESCALATION:

            return (
                "I will connect you "
                "to a human agent shortly."
            )

        # ====================================
        # ANGRY USERS
        # ====================================

        if intent == IntentType.ANGRY:

            return (
                "I understand. "
                "We will stop further calls. "
                "Thank you."
            )

        # ====================================
        # CALLBACK REQUEST
        # ====================================

        if intent == IntentType.CALLBACK:

            return (
                "Sure. "
                "We will schedule a callback "
                "at a better time for you."
            )

        # ====================================
        # EMI QUESTIONS
        # ====================================

        if intent == IntentType.EMI_QUERY:

            return (
                "EMI depends on your loan amount, "
                "income, and repayment duration."
            )

        # ====================================
        # DOCUMENT QUESTIONS
        # ====================================

        if intent == IntentType.DOCUMENT_QUERY:

            return (
                "Typically Aadhaar card, "
                "PAN card, salary slips, "
                "and bank statements are required."
            )

        # ====================================
        # HIGH VALUE LEADS
        # ====================================

        if intent == IntentType.HIGH_TICKET:

            return (
                "I will connect your request "
                "to our senior loan specialist."
            )

        # ====================================
        # CONFUSED USERS
        # ====================================

        if intent == IntentType.CONFUSED:

            return (
                "Let me explain it more simply. "
                "We are helping customers "
                "with loan assistance and follow-up."
            )

        # ====================================
        # INTERESTED USERS
        # ====================================

        if intent == IntentType.INTERESTED:

            return (
                "Great. "
                "May I know which type of loan "
                "you are interested in?"
            )

        # ====================================
        # DEFAULT
        # ====================================

        return (
            "Could you please tell me "
            "a little more?"
        )