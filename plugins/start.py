import asyncio
from pyrogram import Client
from pyrogram import filters

from log import log





@Client.on_message(filters.command("start",prefixes=['.','/','!','?'],case_sensitive=False) & filters.text)
async def start(_, message):
    caption = 'Hola [{}](tg://user?id={}) Gracias por usarme pendejo\nHit /cmds Los comandos son los siguientes'.format(message.from_user.first_name,message.from_user.id)
    await message.reply_text(caption, quote=True)



@Client.on_message(filters.command("cmds",prefixes=['.','/','!','?'],case_sensitive=False) & filters.text)
async def cmds(_, message):
    mess = f"""
/chk - Shopify $10 Checker
/sho - Shopify b3 Checker
/chi - Auth Checker
/gen - Generar CC
"""
    await message.reply(mess, quote=True)
   



