from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()


@router.post("/voice")
async def voice():

    twiml = """
    <Response>
        <Say>Hello, this is AI Loan Assistant.</Say>
    </Response>
    """

    return Response(
        content=twiml,
        media_type="application/xml"
    )