from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Dict, Any, Awaitable
import app.orm as db
import os

class WhitelistMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        is_not_access = await db.is_in_white_list(user.id)
        if not is_not_access and user.id != int(os.getenv('ADMIN_ID')):
            if event.message:
                await event.message.answer("У вас нет доступа к этому боту.")
            elif event.callback_query:
                await event.callback_query.answer("У вас нет доступа.", show_alert=True)
            return

        return await handler(event, data)