from aiohttp import web
from http import HTTPStatus

async def index_handler(request):
    """

    """
    return web.Response(body="hi", status=HTTPStatus.OK)

async def helthcheck_handler(request):
    """

    """
    return web.Response(body="200 OK", status=HTTPStatus.OK)

async def image_handler(request):
    """

    """
    return web.Response(body="image-good", status=HTTPStatus.OK)

def get_routes():
    return [
        web.get('/', index_handler),
        web.get('/healthcheck', helthcheck_handler),
        web.post('/image', image_handler),
    ]