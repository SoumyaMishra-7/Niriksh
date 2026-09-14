import asyncio,os
from niriksh_edge.events.client import NirikshEventClient
async def main():
    client=NirikshEventClient(os.getenv('NIRIKSH_BACKEND_URL','http://localhost:8000'))
    async with __import__('httpx').AsyncClient(timeout=5) as http:await client.flush(http)
    print(f'pending metadata events: {client.buffer.count()}')
if __name__=='__main__':asyncio.run(main())
