from typing import Callable, Awaitable,Any,Dict
from dotenv import load_dotenv
import os
load_dotenv()

from aiogram import BaseMiddleware
from aiogram.types import Message, Update


class UserMiddleware(BaseMiddleware):

    OWNER_ID = int(os.environ.get('OWNER_ID'))

    async def __call__(
            self,
            handler: Callable[[Update,Dict[str,Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str,Any]):
        user_id = getattr(event.from_user,'id',None)
        print(user_id)
        if user_id == self.OWNER_ID:
            return await handler(event,data)
        print('ЧТО ЗА НОУНЕЙМ???')
        return None