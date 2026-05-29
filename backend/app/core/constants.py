from enum import Enum


# ============================================
# INTENT TYPES
# ============================================

class IntentType(str, Enum):

    # Customer is interested
    INTERESTED = "INTERESTED"

    # Customer is confused / asking clarification
    CONFUSED = "CONFUSED"

    # Customer is angry / frustrated
    ANGRY = "ANGRY"

    # Spam / invalid / wrong number
    SPAM = "SPAM"

    # High value customer
    HIGH_TICKET = "HIGH_TICKET"

    # Customer requested callback
    CALLBACK = "CALLBACK"

    # EMI related queries
    EMI_QUERY = "EMI_QUERY"

    # Document related queries
    DOCUMENT_QUERY = "DOCUMENT_QUERY"

    # Fallback intent
    UNKNOWN = "UNKNOWN"
    
    ESCALATION_REQUEST = "ESCALATION_REQUEST"
    
    CALL_END = "CALL_END"


# ============================================
# CONVERSATION STATES
# ============================================

class ConversationState(str, Enum):

    # Initial greeting state
    GREETING = "GREETING"

    # Loan eligibility discussion
    ELIGIBILITY = "ELIGIBILITY"

    # EMI / payment related discussion
    EMI_QUERY = "EMI_QUERY"

    # Document collection / reminders
    DOCUMENT_REMINDER = "DOCUMENT_REMINDER"

    # Objection handling state
    OBJECTION_HANDLING = "OBJECTION_HANDLING"

    # Callback scheduling state
    CALLBACK_BOOKING = "CALLBACK_BOOKING"

    # Escalate to human agent
    ESCALATION = "ESCALATION"

    # Conversation termination
    CALL_END = "CALL_END"
    


# ============================================
# AUDIO STREAM CONFIG
# ============================================

MIN_AUDIO_CHUNK_SIZE = 100

AUDIO_LOG_INTERVAL = 200

DEBUG_AUDIO_ACKS = False