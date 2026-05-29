from app.core.constants import IntentType


class IntentService:

    # ========================================
    # INTERESTED
    # ========================================

    INTERESTED_KEYWORDS = [

        # English
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

        # Hindi
        "मुझे लोन चाहिए",
        "जानकारी",
        "दिलचस्पी",
        "लोन चाहिए",
        "मुझे जानकारी चाहिए",

        # Hinglish
        "loan chahiye",
        "loan lena hai",
        "loan lena chahta",
        "loan lena chahti",
        "loan ke bare mein",
        "personal loan chahiye",
        "mujhe loan chahiye",
        "loan apply karna hai",
    ]

    # ========================================
    # CONFUSED
    # ========================================

    CONFUSED_KEYWORDS = [

        # English
        "confused",
        "don't understand",
        "not clear",
        "can you repeat",
        "explain again",
        "didn't understand",

        # Hindi
        "समझ नहीं आया",
        "फिर से बताइए",
        "समझाइए",

        # Hinglish
        "samajh nahi aya",
        "samajh nahi aaya",
    ]

    # ========================================
    # ANGRY
    # ========================================

    ANGRY_KEYWORDS = [

        # English
        "angry",
        "stop calling",
        "irritated",
        "don't call",
        "not interested",
        "remove my number",

        # Hindi
        "कॉल मत करो",
        "परेशान",
        "गुस्सा",
        "मुझे कॉल मत करो",

        # Hinglish
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

    # ========================================
    # HIGH TICKET
    # ========================================

    HIGH_TICKET_KEYWORDS = [

        # English
        "large amount",
        "high amount",
        "big loan",
        "loan above",
        "50 lakh",
        "1 crore",
        "business loan",

        # Hindi
        "बड़ा लोन",
        "पचास लाख",
        "एक करोड़",

        # Hinglish
        "bada loan",
        "high amount loan",
    ]

    # ========================================
    # SPAM
    # ========================================

    SPAM_KEYWORDS = [

        # English
        "wrong number",
        "spam",
        "scam",
        "fake call",

        # Hindi
        "गलत नंबर",
        "स्पैम",

        # Hinglish
        "galat number",
    ]

    # ========================================
    # CALLBACK
    # ========================================

    CALLBACK_KEYWORDS = [

        # English
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

        # Hindi
        "बाद में कॉल करना",
        "अभी बिजी हूं",
        "कल कॉल करना",

        # Hinglish
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

    # ========================================
    # EMI QUERY
    # ========================================

    EMI_KEYWORDS = [

        # English
        "emi",
        "monthly emi",
        "monthly payment",
        "monthly installment",
        "interest rate",
        "installment",
        "loan emi",

        # Hindi
        "ईएमआई",
        "मासिक भुगतान",
        "ब्याज दर",

        # Hinglish
        "emi kitni",
        "monthly emi kya",
        "emi kya hogi",
    ]

    # ========================================
    # DOCUMENT QUERY
    # ========================================

    DOCUMENT_KEYWORDS = [

        # English
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

        # Hindi
        "दस्तावेज",
        "आधार",
        "पैन कार्ड",

        # Hinglish
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

    # ========================================
    # NORMALIZATION
    # ========================================

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

    # ========================================
    # KEYWORD HELPER
    # ========================================

    @staticmethod
    def contains_keyword(
        text: str,
        keywords: list
    ):

        return any(
            keyword in text
            for keyword in keywords
        )

    # ========================================
    # DETECT INTENT
    # ========================================

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