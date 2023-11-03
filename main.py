import asyncio
import websockets
import json

async def connect(token):
    async with websockets.connect("wss://gateway.discord.gg/?v=10&encoding=json", max_size=None) as ws:
        async for message in ws:
            data = json.loads(message)
            if data['op'] == 10:
                interval = data['d']['heartbeat_interval'] / 1000
                await ws.send(json.dumps({
                    'op': 2,
                    'd': {
                        'token': token,
                        'properties': {
                            '$os': 'Android',
                            '$browser': 'firefox',
                            '$device': 'my_bot'
                        }
                    }
                }))
            elif data['op'] == 11:
                pass

async def main(tokens):
    tasks = [connect(token) for token in tokens]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    with open("./tokens.txt", "r") as f:
        TOKENS = f.read().split()
    
    asyncio.get_event_loop().run_until_complete(main(TOKENS))
    print("Online now")
