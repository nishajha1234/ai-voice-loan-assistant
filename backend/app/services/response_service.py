from app.core.constants import (
    ConversationState,
    IntentType
)


class ResponseService:

    HINDI_RESPONSES = {
        "CALL_END":
            "धन्यवाद। आपका दिन शुभ हो।",

        "ESCALATION":
            "मैं आपको हमारे लोन विशेषज्ञ से जोड़ता हूँ।",

        "ANGRY":
            "हम आपकी बात समझते हैं। आगे से कॉल नहीं की जाएगी।",

        "CALLBACK":
            "ठीक है। हम आपको बाद में कॉल करेंगे।",

        "EMI_QUERY":
            "ईएमआई आपके लोन अमाउंट, आय और अवधि पर निर्भर करती है।",

        "DOCUMENT_QUERY":
            "आधार कार्ड, पैन कार्ड, सैलरी स्लिप और बैंक स्टेटमेंट की आवश्यकता होगी।",

        "HIGH_TICKET":
            "मैं आपकी जानकारी हमारे वरिष्ठ लोन विशेषज्ञ को भेज रहा हूँ।",

        "CONFUSED":
            "हम आपको लोन सहायता और फॉलो-अप सेवाएँ प्रदान कर रहे हैं।",

        "INTERESTED":
            "बहुत बढ़िया। आप किस प्रकार का लोन लेना चाहते हैं?",

        "DEFAULT":
            "क्या आप थोड़ा और विस्तार से बता सकते हैं?"
    }

    @staticmethod
    def generate_response(
        intent,
        state,
        language="en",
        transcript=""
    ):

        is_hindi = language == "hi"

        # ====================================
        # TERMINAL STATES
        # ====================================

        if state == ConversationState.CALL_END:

            if is_hindi:
                return ResponseService.HINDI_RESPONSES["CALL_END"]

            return (
                "Thank you for your time. "
                "Have a great day."
            )

        if state == ConversationState.ESCALATION:

            if is_hindi:
                return ResponseService.HINDI_RESPONSES["ESCALATION"]

            return (
                "I will connect you "
                "to a human agent shortly."
            )

        # ====================================
        # INTENT RESPONSES
        # ====================================

        if intent == IntentType.ANGRY:

            if is_hindi:
                return ResponseService.HINDI_RESPONSES["ANGRY"]

            return (
                "I understand. "
                "We will stop further calls. "
                "Thank you."
            )

        if intent == IntentType.CALLBACK:

            if is_hindi:
                return ResponseService.HINDI_RESPONSES["CALLBACK"]

            return (
                "Sure. "
                "We will schedule a callback "
                "at a better time for you."
            )

        if intent == IntentType.EMI_QUERY:

            if is_hindi:
                return ResponseService.HINDI_RESPONSES["EMI_QUERY"]

            return (
                "EMI depends on your loan amount, "
                "income, and repayment duration."
            )

        if intent == IntentType.DOCUMENT_QUERY:

            if is_hindi:
                return ResponseService.HINDI_RESPONSES["DOCUMENT_QUERY"]

            return (
                "Typically Aadhaar card, "
                "PAN card, salary slips, "
                "and bank statements are required."
            )

        if intent == IntentType.HIGH_TICKET:

            if is_hindi:
                return ResponseService.HINDI_RESPONSES["HIGH_TICKET"]

            return (
                "I will connect your request "
                "to our senior loan specialist."
            )

        if intent == IntentType.CONFUSED:

            if is_hindi:
                return ResponseService.HINDI_RESPONSES["CONFUSED"]

            return (
                "Let me explain it more simply. "
                "We are helping customers "
                "with loan assistance and follow-up."
            )

        if intent == IntentType.INTERESTED:

            if is_hindi:
                return ResponseService.HINDI_RESPONSES["INTERESTED"]

            return (
                "Great. "
                "May I know which type of loan "
                "you are interested in?"
            )

        if is_hindi:
            return ResponseService.HINDI_RESPONSES["DEFAULT"]

        return (
            "Could you please tell me "
            "a little more?"
        )