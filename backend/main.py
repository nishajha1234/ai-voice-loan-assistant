from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "AI Voice Loan Assistant Running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}