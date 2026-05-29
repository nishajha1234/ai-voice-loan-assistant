class SentimentService:

    POSITIVE_KEYWORDS = [

        "interested",
        "good",
        "great",
        "yes",
        "okay",
        "loan",
        "apply",
        "interested in loan",
        "want loan",
        "need loan",
        "thank you"
    ]

    NEGATIVE_KEYWORDS = [

        "angry",
        "stop calling",
        "don't call",
        "not interested",
        "irritating",
        "spam",
        "fraud",
        "scam",
        "wrong number"
    ]

    @classmethod
    def detect_sentiment(
        cls,
        transcript: str
    ):

        text = transcript.lower()

        if any(
            word in text
            for word in cls.NEGATIVE_KEYWORDS
        ):
            return "NEGATIVE"

        if any(
            word in text
            for word in cls.POSITIVE_KEYWORDS
        ):
            return "POSITIVE"

        return "NEUTRAL"