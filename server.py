import asyncio
import websockets

async def handle_websocket(websocket, path):
    async for message in websocket:
        print("Gelen Veri: ", message)

start_server = websockets.serve(handle_websocket, "192.168.16.103", 8077)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
