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

    @app.post("/")
    async def line_webhook(payload: dict):
        body: LineWebhook = payload
        event = body["events"][0]

        if event["message"]["type"] == "text":
            # start loading
            await loading(chat_id=event["source"]["userId"])
            # ai question and answer
            question = event["message"]["text"]
            chat_id = event["source"]["userId"]
            result = langchain_chat(chat_id, question)
            # send reply to line oa
            if result is not None:
                await reply(
                    reply_token=event["replyToken"],
                    payload=[
                        {
                            "type": "text",
                            "text": result
                        }
                    ]
                )
            else:
                await reply(
                    reply_token=event["replyToken"],
                    payload=[
                        {
                            "type": "text",
                            "text": 'สามารถตอบกลับได้ กรุณาลองใหม่อีกครั้ง'
                        }
                    ]
                )
            
        return {"message": "OK"}
