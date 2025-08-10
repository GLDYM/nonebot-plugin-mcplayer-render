from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="MC玩家皮肤渲染",
    description="正版玩家信息查询与皮肤渲染",
    homepage="https://github.com/GLDYM/nonebot-plugin-mcplayer-render/",
    usage="""用法：
1. /player <ID or UUID>
查询对应玩家的信息和皮肤预览图
2. /player <ID or UUID> <type>
查询对应玩家的 UUID 与指定的皮肤预览图
可用参数: raw, body, avatar, default, marching, walking, crouching, crossed, criss_cross, ultimate, isometric, cheering, relaxing, trudging, cowering, pointing, lunging, dungeons, facepalm, sleeping, dead, archer, kicking, mojavatar, reading
""",
    type="application",
    supported_adapters={"~onebot.v11"},
    extra={"author": "Polaris_Light", "version": "1.0.3", "priority": 1},
)

import base64
import json
import shlex

from aiohttp import ClientSession, ClientTimeout
from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageSegment,
)
from nonebot.params import CommandArg


mc_player = on_command(
    "mcplayer",
    aliases={"mc_player", "MC_Player", "玩家查询"},
    force_whitespace=True,
    priority=1,
    block=True,
)


help_message = """用法：
1. /mcplayer <ID or UUID>
查询对应玩家的信息和皮肤预览图
2. /mcplayer <ID or UUID> <type>
查询对应玩家的 UUID 与指定的皮肤预览图
可用参数: raw, body, avatar, default, marching, walking, crouching, crossed, criss_cross, ultimate, isometric, cheering, relaxing, trudging, cowering, pointing, lunging, dungeons, facepalm, sleeping, dead, archer, kicking, mojavatar, reading
"""

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"
}


async def get_profile(location: str) -> dict | None:
    async with ClientSession(headers=headers) as session:
        if len(location) <= 16:
            profile = await (
                await session.get(
                    f"https://api.mojang.com/users/profiles/minecraft/{location}",
                )
            ).json()
        else:
            profile = await (
                await session.get(
                    f"hhttps://api.minecraftservices.com/minecraft/profile/lookup/{location}",
                )
            ).json()
        return profile


async def get_avatar_or_body(uuid: str, avatar: bool = True) -> MessageSegment:
    async with ClientSession(headers=headers) as session:
        try:
            url = (
                f"https://crafatar.com/avatars/{uuid}?size=512&overlay"
                if avatar
                else f"https://crafatar.com/renders/body/{uuid}?overlay"
            )
            message = MessageSegment.image(
                await (
                    await session.get(
                        url,
                        timeout=ClientTimeout(total=5),
                    )
                ).read()
            )
        except Exception:
            message = MessageSegment.text("获取皮肤图片失败。")
    return message


async def get_skin(uuid: str) -> MessageSegment:
    async with ClientSession(headers=headers) as session:
        try:
            skin_dict = await (
                await session.get(
                    f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}",
                    headers=headers,
                )
            ).json()
            unbase = base64.b64decode(skin_dict["properties"][0]["value"])
            SKIN_LAST = json.loads(unbase)
            message = MessageSegment.image(
                await (await session.get(SKIN_LAST["textures"]["SKIN"]["url"])).read()
            )
        except Exception:
            message = MessageSegment.text("获取皮肤图片失败。")
    return message


async def get_action(uuid: str, action: str) -> MessageSegment:
    async with ClientSession(headers=headers) as session:
        try:
            response = await (
                await session.get(
                    f"https://starlightskins.lunareclipse.studio/render/{action}/{uuid}/full",
                    timeout=ClientTimeout(total=5),
                )
            ).read()
            if len(response) < 100:
                message = MessageSegment.text("参数不合法。")
            else:
                message = MessageSegment.image(response)
        except Exception:
            message = MessageSegment.text("获取皮肤图片失败。")
    return message


@mc_player.handle()
async def _(arg: Message = CommandArg()) -> None:
    result: MessageSegment = MessageSegment.text("查询结果：\n")

    args: str = shlex.split(arg.extract_plain_text())
    # logger.info(f'参数解析结果：{args}')

    if len(args) < 1:
        await mc_player.finish(help_message)

    profile: dict = await get_profile(location=args[0])

    if not profile or profile.get("id") is None or profile.get("name") is None:
        await mc_player.finish("没有这个玩家！")

    name = profile["name"]
    uuid = profile["id"]

    result += MessageSegment.text(f"玩家名: {name}\n")
    result += MessageSegment.text(f"UUID: {uuid}\n")

    action = args[1] if len(args) >= 2 else "default"

    match action:
        case "raw":
            result += await get_skin(uuid)
        case "avatar":
            result += await get_avatar_or_body(uuid, avatar=True)
        case "body":
            result += await get_avatar_or_body(uuid, avatar=False)
        case _:
            result += await get_action(uuid, action)

    await mc_player.finish(result)
