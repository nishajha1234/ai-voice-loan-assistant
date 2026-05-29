from app.core.constants import IntentType


class IntentService:

    INTERESTED_KEYWORDS = [
        "interested",
        "tell me more",
        "loan details",
        "need loan",
        "want loan",
        "looking for loan",
        "can you explain",
        "loan information",
        "i need a loan",
        "i want a loan",
        "personal loan",
        "home loan",
        "car loan",
        "loan required",
        "need personal loan",
        "मुझे लोन चाहिए",
        "जानकारी",
        "दिलचस्पी",
        "लोन चाहिए",
        "मुझे जानकारी चाहिए",
        "loan chahiye",
        "loan lena hai",
        "loan lena chahta",
        "loan lena chahti",
        "loan ke bare mein",
        "personal loan chahiye",
        "mujhe loan chahiye",
        "loan apply karna hai",
    ]

    CONFUSED_KEYWORDS = [
        "confused",
        "don't understand",
        "not clear",
        "can you repeat",
        "explain again",
        "didn't understand",
        "समझ नहीं आया",
        "फिर से बताइए",
        "समझाइए",
        "samajh nahi aya",
        "samajh nahi aaya",
    ]

    ANGRY_KEYWORDS = [
        "angry",
        "stop calling",
        "irritated",
        "don't call",
        "not interested",
        "remove my number",
        "कॉल मत करो",
        "परेशान",
        "गुस्सा",
        "मुझे कॉल मत करो",
        "call mat karo",
        "pareshan mat karo",
        "number hatao",
        "remove number",
        "interest nahi hai",
        "dobara call mat karna",
        "faltu call",
        "do not call",
        "do not keep calling",
        "keep calling",
        "calling repeatedly",
        "irritating",
        "annoying",
        "frustrating",
        "stop calling me",
    ]

    HIGH_TICKET_KEYWORDS = [
        "large amount",
        "high amount",
        "big loan",
        "loan above",
        "50 lakh",
        "1 crore",
        "business loan",
        "बड़ा लोन",
        "पचास लाख",
        "एक करोड़",
        "bada loan",
        "high amount loan",
    ]

    SPAM_KEYWORDS = [
        "wrong number",
        "spam",
        "scam",
        "fake call",
        "गलत नंबर",
        "स्पैम",
        "galat number",
    ]

    CALLBACK_KEYWORDS = [
        "call later",
        "callback",
        "busy now",
        "call tomorrow",
        "call me later",
        "call me back",
        "busy right now",
        "please call later",
        "please call me later",
        "call me tomorrow",
        "बाद में कॉल करना",
        "अभी बिजी हूं",
        "कल कॉल करना",
        "अभी मैं busy हूं",
        "कल call करना", 
        "कल बात करते हैं"
        "baad mein call karo",
        "abhi busy hoon",
        "busy hoon",
        "call karna",
        "later call",
        "kal call",
        "kal baat karte hain",
        "call later karo",
        "thodi der baad call karo",
    ]

    EMI_KEYWORDS = [
        "emi",
        "monthly emi",
        "monthly payment",
        "monthly installment",
        "interest rate",
        "installment",
        "loan emi",
        "ईएमआई",
        "मासिक भुगतान",
        "ब्याज दर",
        "emi kitni",
        "monthly emi kya",
        "emi kya hogi",
    ]

    DOCUMENT_KEYWORDS = [
        "documents",
        "document",
        "aadhaar",
        "aadhar",
        "pan",
        "pan card",
        "salary slip",
        "bank statement",
        "kyc",
        "papers required",
        "दस्तावेज",
        "आधार",
        "पैन कार्ड",
        "documents kya lagenge",
        "aadhaar card",
        "pan card chahiye",
    ]
    
    ESCALATION_KEYWORDS = [
    "human agent",
    "senior agent",
    "talk to manager",
    "real person",
    "connect me",
    "agent से connect",
    "senior agent",
    "manager से बात",
    "human se baat",
]
    
    CALL_END_KEYWORDS = [
    "thank you",
    "thanks",
    "okay thank you",
    "bye",
    "goodbye",
    "see you",
    "talk later",
    "have a nice day",
    "धन्यवाद",
    "ठीक है धन्यवाद",
    "thankyou",
]

    @staticmethod
    def normalize_text(text: str):

        return (
            text.lower()
            .strip()
            .replace(".", "")
            .replace(",", "")
            .replace("?", "")
            .replace("!", "")
        )

    @staticmethod
    def contains_keyword(
        text: str,
        keywords: list
    ):

        return any(
            keyword in text
            for keyword in keywords
        )

    @classmethod
    def detect_intent(
    cls,
    transcript: str
    ):

        text = cls.normalize_text(transcript)

        if cls.contains_keyword(
            text,
            cls.SPAM_KEYWORDS
        ):
            return IntentType.SPAM

        if cls.contains_keyword(
            text,
            cls.ANGRY_KEYWORDS
        ):
            return IntentType.ANGRY

        if cls.contains_keyword(
            text,
            cls.CALL_END_KEYWORDS
        ):
            return IntentType.CALL_END

        if cls.contains_keyword(
            text,
            cls.ESCALATION_KEYWORDS
        ):
            return IntentType.ESCALATION_REQUEST

        if cls.contains_keyword(
            text,
            cls.HIGH_TICKET_KEYWORDS
        ):
            return IntentType.HIGH_TICKET

        if cls.contains_keyword(
            text,
            cls.CALLBACK_KEYWORDS
        ):
            return IntentType.CALLBACK

        if cls.contains_keyword(
            text,
            cls.CONFUSED_KEYWORDS
        ):
            return IntentType.CONFUSED

        if cls.contains_keyword(
            text,
            cls.EMI_KEYWORDS
        ):
            return IntentType.EMI_QUERY

        if cls.contains_keyword(
            text,
            cls.DOCUMENT_KEYWORDS
        ):
            return IntentType.DOCUMENT_QUERY

        if cls.contains_keyword(
            text,
            cls.INTERESTED_KEYWORDS
        ):
            return IntentType.INTERESTED

        return IntentType.UNKNOWN