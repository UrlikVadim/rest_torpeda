import asyncio
import valkey
import valkey.client
import glide

# STOPWORD = "STOP"


# async def reader(channel: valkey.client.PubSub):
#     while True:
#         message = await channel.get_message(ignore_subscribe_messages=True, timeout=None)
#         if message is not None:
#             print(f"(Reader) Message Received: {message}")
#             if message["data"].decode() == STOPWORD:
#                 print("(Reader) STOP")
#                 break

# async def main():
#     r = await valkey.from_url("valkey://localhost")
#     async with r.pubsub() as pubsub:
#         await pubsub.psubscribe("channel:*")

#         future = asyncio.create_task(reader(pubsub))

#         await r.publish("channel:1", "Hello")
#         await r.publish("channel:2", "World")
#         await r.publish("channel:1", STOPWORD)

#         await future


def test_kek():
    assert 1==1