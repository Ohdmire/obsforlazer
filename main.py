import aiohttp
import asyncio

import json

from obswebsocket import obsws, requests

'''
配置文件详解

url: gosu开放的websocket地址
interval: 间隔时间，默认每隔0.2s请求一次状态

scene1: obs的场景1的名称
case1: 切换场景1所对应的gosu的状态
上面两项可以自行添加，不过需要注意顺序要一一对应，一个scene可以对应多个case
可以添加多个场景和状态，只需要在后面加上2，3，4...即可
如scene3，scene4，case3，case4

关于osu状态目前有以下几种
0: 默认状态（在主界面中）
1: 在编辑器中
2: 在游戏中
3: osu!stable只会在退出时进入这个状态，lazer无法进入这个状态
4: osu!stable中切换到编辑器的歌曲选择时会进入此状态，lazer无法进入这个状态
5: 单人游戏歌曲选择
7: 结算界面
11: 在多人游戏大厅中
12: 在多人游戏房间中或正在创建多人游戏房间

obshost: obs的ip地址
obsport: obs的端口
obspasswd: obs的密码
'''

# 读取配置文件
now_scene=None
newdata={}
namelist=[]
caselist=[]

try:
    with open ("config.json","r",encoding="utf8") as f:
        data=json.load(f)
        url=data['url']
        for key in data:
            if "scene" in key:
                namelist.append(data[key])
            if "case" in key:
                caselist.append(data[key])
        newdata=dict(zip(namelist,caselist))

        interval=data['interval']
        
        obshost=data['obshost']
        obsport=data['obsport']
        obspasswd=data['obspasswd']

except:
    input("请先配置")
    exit()

async def get_info(url=url):
    session=aiohttp.ClientSession()
    try:
        async with session.ws_connect(url) as ws:
            data=await ws.receive_json()
            await session.close()
            await asyncio.sleep(interval)
            return data['menu']['state']
    except:
        await session.close()
        await asyncio.sleep(interval)
        return None

def change_scene(scene):
    ows = obsws(obshost, obsport, obspasswd)
    ows.connect()
    ows.call(requests.SetCurrentProgramScene(sceneName=scene))
    ows.disconnect()
        
if __name__ == '__main__':
    print("start")
    while True:
        info=asyncio.run(get_info())
        if now_scene != info:
            for i in newdata:
                if info in newdata[i]:
                    change_scene(i)
                    print(f'切换到{i}')
                    now_scene=info
                    break
        else:
            pass