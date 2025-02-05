from typing import TypedDict, List
from llm_langchain.api import langchain_chat
from line.utils import loading, reply


class LineWebhookSource(TypedDict):
    userId: str
class LineWebhookMessage(TypedDict):
    type: str
    text: str
    id: str
class LineWebhookEvent(TypedDict):
    replyToken: str
    message: LineWebhookMessage
    source: LineWebhookSource
class LineWebhook(TypedDict):
    destination: str
    events: List[LineWebhookEvent]

def line_api(app):
    @app.post("/line/webhook")
    async def line_webhook(payload: dict):
        body: LineWebhook = payload

        if(len(body['events']) == 0):
            return {"message": "Verify Success"}

        event = body["events"][0]
        if event["message"]["type"] == "text":
            try:
                 # start loading
                await loading(chat_id=event["source"]["userId"])
                # ai question and answer
                question = event["message"]["text"]
                chat_id = event["source"]["userId"]
                result = langchain_chat(chat_id, question)
                # send reply to line oa
                await reply(
                    reply_token=event["replyToken"],
                    payload=[
                        {
                            "type": "text",
                            "text": result
                        }
                    ]
                )
            except Exception as e:
                # send reply when error
                print(e)
                await reply(
                    reply_token=event["replyToken"],
                    payload=[
                        {
                            "type": "text",
                            "text": 'ไม่สามารถตอบกลับได้ กรุณาลองใหม่อีกครั้ง'
                        }
                    ]
                )  
        else:
            # send reply when message type is not text
            await reply(
                reply_token=event["replyToken"],
                payload=[
                    {
                        "type": "text",
                        "text": 'ระบบ ถาม-ตอบ ได้เฉพาะข้อความเท่านั้นครับ'
                    }
                ]
            )
        return {"message": "Reply Success"}
