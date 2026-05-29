from fastapi import APIRouter
from pathlib import Path

router = APIRouter()

RECORDINGS_DIR = Path("recordings")


@router.get("/dashboard/recordings")
def get_recordings():
    customer_recordings = []

    ai_recordings = []

    for file in RECORDINGS_DIR.glob("*.wav"):

        if "_ai_" in file.name:

            ai_recordings.append(
                {
                    "name": file.name,
                    "url": f"/recordings/{file.name}"
                }
            )

        else:

            customer_recordings.append(
                {
                    "name": file.name,
                    "url": f"/recordings/{file.name}"
                }
            )

    return {
        "customer": customer_recordings,
        "ai": ai_recordings
    }