import asyncio
from pyrogram import Client
from pyrogram import filters

from log import log


apiid = 14870087
apihash = "a6affc9e4e9e3d263fde741d43b34772"
bottoken = "5152488256:AAHY5BNZ75IlCThY-z17CfU0Ly6YusWegSs" #bot token here


client = Client(
    'lana',
    apiid,
    api_hash= apihash,
    bot_token = bottoken,
    plugins=dict(root="plugins"),
    
)


client.run()