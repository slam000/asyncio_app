# api_server.py
# Description: This file contains the code for the API server.

from aiohttp import web
import asyncio

async def handle(request):
    await asyncio.sleep(2) # Simula un delay de 2 segundos
    return web.json_response({"message": "Hola desde el servidor API"})

app = web.Application()
app.router.add_get('/', handle)

if __name__ == '__main__':
    web.run_app(app, port=8080)
    
