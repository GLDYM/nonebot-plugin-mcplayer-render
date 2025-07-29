<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://raw.githubusercontent.com/fllesser/nonebot-plugin-template/refs/heads/resource/.docs/NoneBotPlugin.svg" width="310" alt="logo"></a>

# nonebot-plugin-mcplayer-render

_✨ 正版玩家信息查询与皮肤渲染 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/GLDYM/nonebot-plugin-mcplayer-render.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-mcplayer-render">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-mcplayer-render.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-mcplayer-render

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-mcplayer-render
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-mcplayer-render
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-mcplayer-render
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-mcplayer-render
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_mcplayer_render"]

</details>

## 使用方法
- /player \<ID or UUID\> 查询对应玩家的信息和皮肤预览图
- /player \<ID or UUID\> \<type\> 查询对应玩家的 UUID 与指定的皮肤预览图
  - 可用参数: raw, body, avatar, default, marching, walking, crouching, crossed, criss_cross, ultimate, isometric, cheering, relaxing, trudging, cowering, pointing, lunging, dungeons, facepalm, sleeping, dead, archer, kicking, mojavatar, reading
