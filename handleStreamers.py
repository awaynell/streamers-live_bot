from dataclasses import dataclass
from typing import List

from settings import getVKLiveStreamers, setVKLiveStreamers
from api import getIsVKLiveStreamerOnline
import asyncio


@dataclass
class VkStreamer:
    isLive: bool
    name: str
    lastCheck: int
    isSendNotification: bool


async def add_vk_streamer(update, context):
    args = " ".join(context.args)  # Получаем аргументы команды

    if not args:
        await update.message.reply_text("❌ Укажите никнеймы стримеров через запятую.")
        return

    vklivestreamers: List[VkStreamer] = getVKLiveStreamers(
        context=context)  # Загружаем текущий список

    # Добавляем стримеров в список
    new_list = [s.strip() for s in args.split(",") if s.strip()]

    added_streamers = []

    for name in new_list:
        # Проверяем, нет ли уже такого
        if not any(s.name == name for s in vklivestreamers):
            streamer = VkStreamer(
                isLive=False,
                name=name,
                lastCheck=0,
                isSendNotification=False
            )
            vklivestreamers.append(streamer)
            added_streamers.append(streamer)

    setVKLiveStreamers(vklivestreamers, context=context)

    if added_streamers:
        await update.message.reply_text(f"✅ Добавлены стримеры: {', '.join([s.name for s in added_streamers])}")
    else:
        await update.message.reply_text("❌ Все указанные стримеры уже есть в списке.")

    await check_vk_streamers(context, update.effective_chat.id)


async def get_my_vk_streamers(update, context):
    streamers = getVKLiveStreamers(context=context)
    for streamer in streamers:
        await update.message.reply_text(f"{streamer.name} - {streamer.isLive}")


async def check_vk_streamers(context, chat_id):
    while True:
        await asyncio.sleep(600)
        vklivestreamers: List[VkStreamer] = getVKLiveStreamers(context=context)
        updated_streamers = []

        for streamer in vklivestreamers:
            old_status = streamer.isLive
            new_status = await getIsVKLiveStreamerOnline(streamer.name)

            if old_status != new_status:
                if new_status and not streamer.isSendNotification:
                    await context.application.bot.send_message(
                        chat_id=chat_id,
                        text=f"🟢 {streamer.name} начал стрим!"
                    )
                    streamer.isSendNotification = True
                elif not new_status and streamer.isSendNotification:
                    await context.application.bot.send_message(
                        chat_id=chat_id,
                        text=f"⚪ {streamer.name} закончил стрим."
                    )
                    streamer.isSendNotification = False

            streamer.isLive = new_status
            updated_streamers.append(streamer)

        setVKLiveStreamers(updated_streamers, context=context)


async def start_checking(update, context):
    chat_id = update.message.chat_id
    asyncio.create_task(check_vk_streamers(context, chat_id))
    await update.message.reply_text("✅ Запущен мониторинг стримеров.")
