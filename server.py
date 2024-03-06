
name1="场景 1"
name2="场景 2"
blacklist=["Choosing a beatmap","In a lobby"]

import aiohttp
from aiohttp import web

from obswebsocket import obsws, requests

import json

# 读取配置文件
try:
    with open ("old_config.json","r",encoding="utf8") as f:
        data=json.load(f)
        name1=data['name1']
        name2=data['name2']
        blacklist=data['blacklist']
        host=data['host']
        port=int(data['port'])
        obshost=data['obshost']
        obsport=data['obsport']
        obspasswd=data['obspasswd']

except:
    input("请先配置name和blacklist和obs设置")
    exit()

async def hello(request):
    return web.Response(text="Server is running")
 
async def websocket_handler(request):
    # ws对象
    ws = web.WebSocketResponse()
    # 等待用户连接
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            received_message = msg.data
            print(received_message)  # 打印接收到的消息到控制台
            # 创建OBS WebSocket连接
            ows = obsws(obshost, obsport, obspasswd)
            ows.connect()
            # 切换场景
            if any(key in received_message for key in blacklist):
                ows.call(requests.SetCurrentProgramScene(sceneName=name2))
                print(f'切换到{name2}')
            else:
                ows.call(requests.SetCurrentProgramScene(sceneName=name1))
                print(f'切换到{name1}')
            # 断开OBS WebSocket连接
            ows.disconnect()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(f"WebSocket Error: {ws.exception()}")
 
if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.get('/', hello)])
    app.add_routes([web.get('/ws', websocket_handler)])
 
    web.run_app(app,host=host,port=port)