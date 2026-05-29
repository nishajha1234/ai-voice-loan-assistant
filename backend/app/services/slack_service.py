import os
import requests


class SlackService:

    @staticmethod
    def send_alert(message: str):

        webhook_url = os.getenv(
            "SLACK_WEBHOOK_URL"
        )

        if not webhook_url:
            return

        try:

            requests.post(
                webhook_url,
                json={
                    "text": message
                },
                timeout=5
            )

        except Exception as e:

            print(
                f"Slack alert failed: {e}"
            )