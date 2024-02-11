from datetime import datetime

from aiocache import caches

caches.set_config({
    'default': {
        'cache': "aiocache.SimpleMemoryCache",
        'serializer': {
            'class': "aiocache.serializers.PickleSerializer"
        },
        'ttl': 3600
    }
})
cache = caches.get('default')


async def get_and_save_cache_messages(
        chat_id,
        message_text=None,
        user_a_username=None,
        send_message_to=None,
        for_send_messages=False,
        for_get_messages=False
):
    cache_key = f"chat_{chat_id}_messages"
    cached_messages = await cache.get(cache_key)

    if for_get_messages:
        return cached_messages, cache_key, cache

    if for_send_messages:
        if cached_messages is None:
            cached_messages = []

        cached_messages.insert(
            0,
            {
                "message": message_text,
                "from": user_a_username,
                "to": send_message_to,
                "send_in": datetime.now()
            }
        )

        await cache.set(cache_key, cached_messages)
