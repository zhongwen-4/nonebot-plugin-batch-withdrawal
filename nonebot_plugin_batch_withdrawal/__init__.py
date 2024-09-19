import sqlite3

from nonebot import on_message, get_driver, require, logger
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER

require("nonebot_plugin_localstore")
require("nonebot_plugin_alconna")
import nonebot_plugin_localstore as localstore

path = localstore.get_plugin_data_dir()
write_message_id = on_message()
driver = get_driver()

from nonebot_plugin_alconna import on_alconna, Alconna, Args, Arparma, At, Match
delete = on_alconna(Alconna("delete", Args["qq?", At]["num", int]), permission= SUPERUSER | GROUP_ADMIN | GROUP_OWNER)

@driver.on_startup
async def _():
    global conn, cursur
    conn = sqlite3.connect(f"{path}/message_id.db")
    logger.debug("[message_id] 数据库连接成功")
    logger.info(f"获取数据目录成功 -> {path}")
    cursur = conn.cursor()

@driver.on_shutdown
async def shutdown_handle():
    logger.debug("[message_id] 数据库关闭")
    conn.commit()
    conn.close()

@write_message_id.handle()
async def write_message_id_handle(bot: Bot, event: GroupMessageEvent):
    cursur.execute(f"CREATE TABLE IF NOT EXISTS _{event.group_id}(id INTEGER PRIMARY KEY AUTOINCREMENT, message_id INTEGER, user_id INTEGER)")
    conn.commit()

    role = await bot.get_group_member_info(group_id=event.group_id, user_id= event.self_id)

    if "admin" not in role["role"] and "owner" not in role["role"]:
        logger.debug("需要机器人账号是群主/管理员")
        await write_message_id.finish()

    if role["role"] == "owner":
        if event.sender.role == "member" or "admin":
            cursur.execute(f"INSERT INTO _{event.group_id}(message_id, user_id) VALUES(?,?)", (event.message_id, event.user_id))
            conn.commit()
            logger.debug(f"数据库 [message_id] | _{event.group_id} 写入 -> 消息ID: {event.message_id}")
        else:
            logger.debug("消息对象是群主, 跳过写入")
    
    else:
        if event.sender.role == "member":
            cursur.execute(f"INSERT INTO _{event.group_id}(message_id, user_id) VALUES(?,?)", (event.message_id, event.user_id))
            conn.commit()
            logger.debug(f"数据库 [message_id] | _{event.group_id} 写入 -> 消息ID: {event.message_id}")
        else:
            logger.debug("消息对象是管理员/群主, 跳过写入")

@delete.handle()
async def delete_handle(bot: Bot, event: GroupMessageEvent, rum: Arparma, qq: Match[At | int]):
    role = await bot.get_group_member_info(group_id=event.group_id, user_id= event.self_id)
    if role["role"] != "owner" and role["role"] != "admin":
        await delete.finish("权限不足, 需要机器人账号是群主/管理员", reply_message = True)

    if qq.available:
        if isinstance(qq.result, At):
            user_id = qq.result.target
            cursur.execute(f"SELECT message_id FROM _{event.group_id} WHERE user_id= ? ORDER BY message_id DESC LIMIT ?", (user_id, rum.all_matched_args["num"]))
            result = cursur.fetchall()
            for i in result:
                await bot.delete_msg(message_id= i[0])
                cursur.execute(f"DELETE FROM _{event.group_id} WHERE message_id = ?", (i[0],))
                conn.commit()
                logger.debug(f"数据库 [message_id] | _{event.group_id} 删除 -> 消息ID: {i[0]}")
            await delete.finish(f"成功撤回{user_id} 的 {rum.all_matched_args['num']} 条消息", reply_message = True)
    
    else:
        cursur.execute(f"SELECT message_id FROM _{event.group_id} ORDER BY id DESC LIMIT ?", (rum.all_matched_args["num"],))
        result = cursur.fetchall()
        for i in result:
            await bot.delete_msg(message_id=i[0])
            cursur.execute(f"DELETE FROM _{event.group_id} WHERE message_id = ?", (i[0],))
            conn.commit()
            logger.debug(f"数据库 [message_id] | _{event.group_id} 删除 -> 消息ID: {i[0]}")
        await delete.finish(f"成功撤回 {rum.all_matched_args['num']} 条消息", reply_message = True)