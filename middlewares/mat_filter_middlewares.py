import string
import json
from vkwave.bots import BaseMiddleware, SimpleBotEvent, MiddlewareResult, BotEvent
from vkwave.bots.core.dispatching.filters import get_text


class MatFilterMiddleware(BaseMiddleware):
    async def pre_process_event(self, event: BotEvent) -> MiddlewareResult:
        text = get_text(event)
        set_msg = {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in text.split(' ')}
        set_cenz = set(json.load(open('cenz.json')))
        verify = bool(set_msg.intersection(set_cenz) != set())
        if verify:
            return MiddlewareResult(False)
        return MiddlewareResult(True)
