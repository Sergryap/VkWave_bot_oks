import string
import json
from vkwave.bots import BotEvent
from vkwave.bots.core.dispatching.filters import base, get_text


class MatFilter(base.BaseFilter):

    async def check(self, event: BotEvent) -> base.FilterResult:

        text = get_text(event)
        if text is None:
            return FilterResult(False)
        set_msg = {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in text.split(' ')}
        set_cenz = set(json.load(open('cenz.json')))
        verify = bool(set_msg.intersection(set_cenz) == set())
        if not verify:
            return base.FilterResult(False)
        return base.FilterResult(True)

