# (c) gautamajay52
# 
# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)


import os
import shutil
import asyncio
import subprocess
import requests
from tobrot.helper_funcs.upload_to_tg import upload_to_tg, upload_to_gdrive
from tobrot import (
    DOWNLOAD_LOCATION
)


async def yt_playlist_downg(message, i_m_sefg):
    url = message.text
    usr = message.from_user.id
    messa_ge = i_m_sefg.reply_to_message
    fol_der = f"{usr}youtube"
    print(url)
    print(usr)
    print(messa_ge)
    print(fol_der)
    try:
        os.mkdir(fol_der)
    except:
        pass
    cmd = ["youtube-dl", "--geo-bypass-country", "IT", "-i", "-f", "best[height<=720][ext=mp4]+bestaudio[ext=m4a]/mp4", "-o", f"{fol_der}/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s", f"{url}"]
    gau_tam = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    gau, tam = await gau_tam.communicate()
    LOGGER.info(gau.decode('utf-8'))
    LOGGER.info(tam.decode('utf-8'))
    e_response = tam.decode().strip()
    ad_string_to_replace = "please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output."
    if e_response and ad_string_to_replace in e_response:
        error_message = e_response.replace(ad_string_to_replace, "")
        await i_m_sefg.edit_text(
            error_message
        )
        return False, None
    if os.path.exists(f'blame_{usr}_knowledge_again.txt'):
        get_g = os.listdir(fol_der)
        print(get_g)
        for ga_u in get_g:
            print(ga_u)
            ta_m = os.path.join(fol_der, ga_u)
            print(ta_m)
            shutil.move(ta_m, './')
            await upload_to_gdrive(ga_u, i_m_sefg, messa_ge, usr)
    else:
        final_response = await upload_to_tg(i_m_sefg, fol_der, usr, {})
        print(final_response)
    try:
        shutil.rmtree(fol_der)
        os.remove(f'blame_{usr}_knowledge_again.txt')
    except:
        pass
