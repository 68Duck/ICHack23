# WS client example

import asyncio
import websockets

async def hello():
    uri = "wss://ws.tryterra.co/connect"
    async with websockets.connect(uri) as websocket:
        while True:
            greeting = await websocket.recv()
            print(greeting)
            await websocket.send("200")

asyncio.get_event_loop().run_until_complete(hello())