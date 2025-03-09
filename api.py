import requests
import asyncio

vkLiveApiBaseUrl = "https://api.live.vkvideo.ru"


async def getIsVKLiveStreamerOnline(streamer: str) -> bool:
    return await asyncio.to_thread(lambda: requests.get(f"{vkLiveApiBaseUrl}/v1/blog/{streamer}/public_video_stream?from=layer").json().get('isOnline', False))
