import os
import requests

from app.utils.logger import logger


class NotificationService:

    @staticmethod
    def send_hot_lead_alert(
        transcript,
        intent
    ):

        webhook_url = os.getenv(
            "SLACK_WEBHOOK_URL"
        )

        if not webhook_url:
            return

        payload = {
            "text":
                f"🔥 Hot Lead Detected\n\n"
                f"Intent: {intent}\n"
                f"Transcript: {transcript}"
        }

        try:

            requests.post(
                webhook_url,
                json=payload,
                timeout=5
            )

        except Exception as e:

            logger.error(
                f"Slack alert failed: {e}"
            )