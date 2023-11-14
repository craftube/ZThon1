import os
import asyncio
from pathlib import Path

from telethon import events
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.types import InputMessagesFilterDocument
from telethon.tl.types import Channel, InputChannel
from ..Config import Config
from ..helpers.utils import install_pip
from ..utils import load_module
from . import BOTLOG, BOTLOG_CHATID, zedub

plugin_category = "الادوات"

async def install():
    try:
        entity = await zedub.get_entity(Config.ZELZAL_Z)
        zilzal = entity.username
    except:
        zilzal = Config.ZELZAL_A
    documentss = await zedub.get_messages(zilzal, None, filter=InputMessagesFilterDocument)
    total = int(documentss.total)
    for module in range(total):
        plugin_to_install = documentss[module].id
        plugin_name = documentss[module].file.name
        if plugin_name.endswith(".py"):
            if os.path.exists(f"zira/plugins/{plugin_name}"):
                return
            downloaded_file_name = await zedub.download_media(
                await zedub.get_messages(zilzal, ids=plugin_to_install),
                "zira/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            flag = True
            check = 0
            while flag:
                try:
                    load_module(shortname.replace(".py", ""))
                    break
                except ModuleNotFoundError as e:
                    install_pip(e.name)
                    check += 1
                    if check > 5:
                        break

    zedub.loop.create_task(install())