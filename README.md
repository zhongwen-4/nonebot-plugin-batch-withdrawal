# _✨欢迎使用批量撤回插件✨_
本插件主要用于批量撤回消息

## 💿如何安装
<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-batch-withdrawal

</details>

<details open>
<summary>使用 pip 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

如果你启用了 **虚拟环境** 且 **nonebot没有加载本插件** 则需要进入.\.venv\Scripts下运行命令行,将pip.exe拖入命令行中再运行以下命令

    pip install nonebot-plugin-batch-withdrawal

</details>

## 🎉指令列表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| delete | 主人/群管理 | 否 | 群聊 | delete 1代表撤回一条消息, delete @被撤回人 1代表撤回一条该成员的消息 |