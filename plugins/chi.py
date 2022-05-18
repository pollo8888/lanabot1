import time
import requests
from pyrogram import Client
from pyrogram import filters
from datas import find_between, get_data, get_response
from random_address import real_random_address


from log import log
from plugins.chi_defs import *
from rand_user import random_user_api





@Client.on_message(filters.command("chi",prefixes=['.','/','!','?'],case_sensitive=False) & filters.text)
async def start(_, message):
    try:
        start_time = int(time.time())
        xx = await message.reply("Chequeando...", quote = True)
        message.text = message.reply_to_message.text if message.reply_to_message is not None else message.text
        data = get_data(message.text)
        assert isinstance(data, tuple), data.format(
            message.from_user.id, message.from_user.first_name)
        cc, mes, ano,cvv = data
        r =  requests.Session()
        crsf = au_one(r)
        assert crsf, "Error en la solicitud intenta mas tarde"
        await xx.edit("Primera Solicitud Completada")
        rand_user = random_user_api().get_random_user_info()
        addr = real_random_address()
        b = au_two(r, rand_user, crsf)
        assert b, " Error en la solicitud intenta mas tarde"
        sec, req_sec = b
        await xx.edit("Segunda solicitud completada")
        last = au_three(r, sec, req_sec, cc, mes,ano, cvv)
        assert last, "Error en la solicitud intenta mas tarde"
        # print(last)
        # await xx.edit("Last Requests Completed")
        stripeCode = None
        r_text, r_logo = None , None
        if 'status' in last and 'succeeded' in last['status']:
            r_text, r_logo, stripeCode = "Auth Live", "✅", 'CVV LIVE'
        else:
            stripeMessage = last['error']['message'].replace('_', ' ') if 'message' in last['error'] else last['error']['code'].replace('_', ' ')
            stripeCode = last['error']['code'].replace('_', ' ').title() if 'code' in last['error'] else 'Unknown'
            r_text, r_logo , r_respo = get_response_au(stripeMessage)
        mess = f"""
Card: `{cc}|{mes}|{ano}|{cvv}`
Response: {stripeCode or r_respo} {r_logo}
Message: {r_text}
Took: {int(time.time()) -  start_time}
"""
        await xx.edit(mess)
    except AssertionError as e:
        await xx.edit(e)
    except Exception as e:
        await xx.edit(e)
        

