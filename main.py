from fastapi import FastAPI, Header, HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from queue import Queue
import re
import os

app = FastAPI()
sms_queue = Queue()

API_KEY = os.getenv("API_KEY")

class SMSPayload(BaseModel):
    from_number: str
    message: str

@app.post("/sms-webhook")
async def sms_webhook(
    payload: SMSPayload,
    authorization: str = Header(None)
):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(401, "Invalid API key")
    m = re.search(r"\b(\d{6})\b", payload.message)
    if not m:
        raise HTTPException(400, "No code in message")
    sms_queue.put(m.group(1))
    return {"status": "ok"}

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Booking Bot is live!"}

# TODO: здесь будет логика проверки слотов и планировщик 08:00–10:00
