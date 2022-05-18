import time
import requests
from pyrogram import Client
from pyrogram import filters
from datas import find_between, get_data, get_response
from random_address import real_random_address


from log import log
from plugins.shi_def import *
from rand_user import random_user_api





@Client.on_message(filters.command("sho",prefixes=['.','/','!','?'],case_sensitive=False) & filters.text)
async def start(_, message):
    try:
        start_time = int(time.time())
        xx = await message.reply("Checking...", quote = True)
        message.text = message.reply_to_message.text if message.reply_to_message is not None else message.text
        data = get_data(message.text)
        assert isinstance(data, tuple), data.format(
            message.from_user.id, message.from_user.first_name)
        cc, mes, ano,cvv = data
        r =  requests.Session()
        rand_user = random_user_api().get_random_user_info()
        a = sho_one(r, rand_user)
        assert a, "Error On First requests"
        auth_token,checkout_url, payment_gateway = a
        # await xx.edit("First Requests Completed")
        g = sho_two(r,rand_user, cc,mes,ano,cvv, payment_gateway,checkout_url, auth_token)
        assert g, "Error On Last Requests"
        # await xx.edit("Last Requests Completed")
        r_text1,r_logo,r_respo,r_text = get_response_sho_br(g)
        mess = f"""
Card: `{cc}|{mes}|{ano}|{cvv}`
Response: {r_respo} {r_logo}
Message: {r_text}
Res: {r_text1}
Took: {int(time.time()) -  start_time}
"""
        await xx.edit(mess)
    except AssertionError as e:
        await xx.edit(e)
    except Exception as e:
        print(e)
        

