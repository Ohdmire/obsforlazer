# This example requires the 'message_content' intent.

import discord
import aiohttp
import json

# 读取配置文件
try:
    with open ("old_config.json","r",encoding="utf8") as f:
        data=json.load(f)
        userid=data['userid']
        bottoken=data['token']
        host=data['host']
        port=int(data['port'])
        url=f'http://{host}:{port}/ws'
except:
    input("请先配置用户名和token和url")
    exit()

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    user= await client.fetch_user(userid)
    print(user.name)

@client.event
async def on_presence_update(before,after):
    session=aiohttp.ClientSession()
    now_state=after.activity.state
    async with session.ws_connect(url) as ws:
        print(now_state)
        await ws.send_json(now_state)
        await session.close()

client.run(bottoken)

