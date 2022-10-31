import os
from pyrogram import filters, Client as bot
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from PhoenixScanner import Phoenix 


RED = Phoenix(os.getenv("RED7_TOKEN"))

def call_back_filter(data):
    return filters.create(lambda flt, _, query: flt.data in query.data,
                          data=data)

def is_admin(group_id: int, user_id: int):
    try:
        user_data = bot.get_chat_member(group_id, user_id)
        if user_data.status == 'administrator' or user_data.status == 'creator':
            return True
        else:
            return False
    except:
        return False

@bot.on_callback_query(call_back_filter("kick"))
def kick_callback(_, query):
    user = query.data.split(":")[2]
    if is_admin(query.message.chat.id,
                query.from_user.id) and query.data.split(":")[1] == "kick":
        bot.ban_chat_member(query.message.chat.id, user)
        bot.unban_chat_member(query.message.chat.id, user)
        query.answer('Kicked!')
        query.message.edit(
            f'Kick User [{user}](tg://user?id={user})\n Admin User [{query.from_user.id}](tg://user?id={query.from_user.id})',
            parse_mode='markdown')
    else:
        message.reply('You are not admin!')


@bot.on_callback_query(call_back_filter("ban"))
def ban_callback(_, query):
    user = query.data.split(":")[2]
    if is_admin(query.message.chat.id,
                query.from_user.id) and query.data.split(":")[1] == "ban":
        bot.ban_chat_member(query.message.chat.id, user)
        query.answer('Banned')
        query.message.edit(
            f'Banned User [{user}](tg://user?id={user})\n Admin User [{query.from_user.id}](tg://user?id={query.from_user.id})',
            parse_mode='markdown')
    else:
        message.reply('You are not admin!')


@bot.on_callback_query(call_back_filter("mute"))
def mute_callback(_, query):
    user = query.data.split(":")[2]
    if is_admin(query.from_user.id,
                query.message.chat.id) and query.data.split(":")[1] == "mute":
        bot.restrict_chat_member(
            query.message.chat.id,
            user,
            ChatPermissions(can_send_messages=False),
        )
        query.answer('Muted!')
        query.message.edit(
            f'Muted User [{user}](tg://user?id={user})\n Admin User [{query.from_user.id}](tg://user?id={query.from_user.id})',
            parse_mode='markdown')
    else:
        message.reply('You are not admin!')


@bot.on_message(filters.new_chat_members)
async def botrm(bot: bot, m: Message): 
  user = m.from_user.id
  check = RED.check(user)
  if check["is_gban"]:
    try:
      x = await bot.get_users(user)
      title = x.first_name
    except:
      title = m.from_user.first_name
      msg = f"""
 Alert ⚠️
User [{title}](tg://user?id={user}) is officially
Scanned by Team Red7 | Phoenix API ;)

Appeal [Here](https://t.me/Red7WatchSupport) | 

(Press on below button to remove this shit.Else it may put your groups, Chat in danger)
"""
      await m.reply_text(msg, 
                reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Ban",
                                         callback_data=f"ban:ban:{user}"),
                    InlineKeyboardButton("Kick",
                                         callback_data=f"kick:kick:{user}"),
                    InlineKeyboardButton("Mute",
                                         callback_data=f"mute:mute:{user}")
                ],
            ]))
  else:
     pass
