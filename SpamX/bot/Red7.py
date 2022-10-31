import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from PhoenixScanner import Phoenix
from .. import pbot as RedSeven 


RED = Phoenix(os.getenv("RED7_TOKEN"))


def is_admin(group_id: int, user_id: int):
    try:
        user_data = bot.get_chat_member(group_id, user_id)
        if user_data.status == 'administrator' or user_data.status == 'creator':
            return True
        else:
            return False
    except:
        return False

@RedSeven.on_callback_query(call_back_filter("ban"))
def ban_callback(_, query: CallbackQuery):
  user = query.data.split(":")[2]
  if is_admin(query.message.chat.id, query.from_user.id) and query.data.split(":")[1] == "ban":
      await bot.ban_chat_member(query.message.chat.id, user)
      await query.answer('Banned Successfully')
      await query.message.edit( f'Banned User [{user}](tg://user?id={user})\n Admin User [{query.from_user.id}](tg://user?id={query.from_user.id})', parse_mode='markdown')
 
  else: 
     await query.answer('You are not admin!')


@RedSeven.on_message(filters.new_chat_members)
async def botrm(bot: RedSeven, m: Message): 
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
      await m.reply_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Ban", callback_data=f"ban:ban:{user}")]]))
  else:
     pass
