import os
import httpx
from typing import TypedDict, List

headers = {
    "Content-Type": "application/json",
    "Authorization": f'Bearer {os.getenv("LINE_CHANNEL_ACCESS_TOKEN")}'
}

async def loading(chat_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                'https://api.line.me/v2/bot/chat/loading/start',
                headers=headers,
                json={
                    "chatId": chat_id,
                    "loadingSeconds": 30,
                }
            )
            return True
        except Exception as e:
            return False

class ReplyPayload(TypedDict):
    type: str
    text: str

async def reply(reply_token: str, payload: List[ReplyPayload]) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(
                'https://api.line.me/v2/bot/message/reply',
                headers=headers,
                json={
                    "replyToken": reply_token,
                    "messages": payload,
                }
            )
            return True
        except Exception as e:
            return False