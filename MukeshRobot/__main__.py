import importlib
import re
import time
import asyncio
from platform import python_version as y
from sys import argv
from pyrogram import __version__ as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

import MukeshRobot.modules.no_sql.users_db as sql
from MukeshRobot import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)
from MukeshRobot.modules import ALL_MODULES
from MukeshRobot.modules.helper_funcs.chat_status import is_user_admin
from MukeshRobot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time
PM_START_TEX = """
ʜᴇʟʟᴏ `{}`, Aᴘᴀ ᴋᴀʙᴀʀᴍᴜ \nᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ ᴋᴀᴡᴀɴ . . . 
"""


PM_START_TEXT = """ 
*ʜᴇʏ* {} , ❣️
*๏ sᴀʏᴀ {} ᴅɪ sɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀɴᴛᴜ ᴀɴᴅᴀ ᴍᴇɴɢᴇʟᴏʟᴀ ɢʀᴜᴘ ᴀɴᴅᴀ!
 ᴛᴇᴋᴀɴ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴛᴀʜᴜɪ ʟᴇʙɪʜ ʟᴀɴᴊᴜᴛ ᴛᴇɴᴛᴀɴɢ ᴄᴀʀᴀ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ sᴀʏᴀ sᴇᴄᴀʀᴀ ᴍᴀᴋsɪᴍᴀʟ!*
 ➻ *ᴍᴀɴᴀᴊᴇᴍᴇɴ ɢʀᴜᴘ ᴛᴇʟᴇɢʀᴀᴍ ᴘᴀʟɪɴɢ ᴋᴜᴀᴛ ➕ ʙᴏᴛ ᴍᴀɴᴀᴊᴇᴍᴇɴ ᴍᴜsɪᴋ ᴅᴀɴ sᴀʏᴀ ᴍᴇᴍɪʟɪᴋɪ ʙᴇʙᴇʀᴀᴘᴀ ғɪᴛᴜʀ ʟᴜᴀʀ ʙɪᴀsᴀ ᴅᴀɴ ʙᴇʀɢᴜɴᴀ.*
─────────────────
   *➻ ᴜsᴇʀs »* {}
   *➻ ᴄʜᴀᴛs »* {}
─────────────────
"""

buttons = [
    [
        InlineKeyboardButton(text="🏡", callback_data="mukesh_back"),
        InlineKeyboardButton(text="🛡️", callback_data="mukesh_"),
        InlineKeyboardButton(text="💳", callback_data="source_"),
        InlineKeyboardButton(text="🧑‍💻", url=f"tg://user?id={OWNER_ID}"),
        InlineKeyboardButton(text="🖥️", callback_data="Main_help"),
     ],
    [
        InlineKeyboardButton(
            text="ᴛᴀᴍʙᴀʜᴋᴀɴ sᴀʏᴀ ᴋᴇ ɢʀᴜᴘ ᴀɴᴅᴀ",
            url=f"https://t.me/{dispatcher.bot.username}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="⚙️ ʙᴀɴᴛᴜᴀɴ ᴅᴀɴ ᴘᴇʀɪɴᴛᴀʜ", callback_data="Main_help"),
    ],
    

]

HELP_STRINGS = f"""
» *{BOT_NAME}  ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪ ʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ᴘᴇɴᴊᴇʟᴀsᴀɴ ᴛᴇɴᴛᴀɴɢ sᴘᴇsɪғɪᴋ ᴍᴇᴍᴇʀɪɴᴛᴀʜ*"""

DONATE_STRING = f"""ʜᴀɪ sᴀʏᴀɴɢ,
  sᴇɴᴀɴɢ ᴍᴇɴᴅᴇɴɢᴀʀ ʙᴀʜᴡᴀ ᴀɴᴅᴀ ɪɴɢɪɴ ʙᴇʀᴅᴏɴᴀsɪ.

ᴀɴᴅᴀ ᴅᴀᴘᴀᴛ ʟᴀɴɢsᴜɴɢ ᴍᴇɴɢʜᴜʙᴜɴɢɪ ᴘᴇɴɢᴇᴍʙᴀɴɢ sᴀʏᴀ @Bee\_Domp ᴜɴᴛᴜᴋ ʙᴇʀᴅᴏɴᴀsɪ ᴀᴛᴀᴜ ᴀɴᴅᴀ ᴅᴀᴘᴀᴛ ᴍᴇɴɢᴜɴᴊᴜɴɢɪ ᴏʙʀᴏʟᴀɴ ᴅᴜᴋᴜɴɢᴀɴ sᴀʏᴀ @cari\_kawanindonesia ᴅᴀɴ ʙᴇʀᴛᴀɴʏᴀ ᴅɪ sᴀɴᴀ ᴛᴇɴᴛᴀɴɢ sᴜᴍʙᴀɴɢᴀɴ."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("MukeshRobot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Tidak dapat memiliki dua modul dengan nama yang sama! Silakan ubah satu")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_photo(
        chat_id=chat_id,
        photo=START_IMG,
        caption=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard,
    )

def start(update: Update, context: CallbackContext):
    args = context.args
    global uptime
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                    ),
                )
            elif args[0].lower() == "markdownhelp":
                IMPORTED["exᴛʀᴀs"].markdown_help_sender(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rᴜʟᴇs" in IMPORTED:
                IMPORTED["rᴜʟᴇs"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            
            x=update.effective_message.reply_sticker(
                "CAACAgUAAxkBAAECdA1l1DPC-oEv3Lu0Aqn1svSSQfB34gACVgwAAlza6VUWUsP4pDar1TQE")
            x.delete()
            usr = update.effective_user
            lol = update.effective_message.reply_text(
                PM_START_TEX.format(usr.first_name), parse_mode=ParseMode.MARKDOWN
            )
            time.sleep(0.4)
            lol.edit_text("ʜᴀɪ")
            time.sleep(0.4)
            lol.edit_text("ᴋᴀᴍᴜ")
            time.sleep(0.4)
            lol.edit_text("ꜱᴛᴀʀᴛɪɴɢ... ")
            time.sleep(0.5)
            lol.delete()
            
            update.effective_message.reply_photo(START_IMG,PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME,sql.num_users(),sql.num_chats()),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            START_IMG,
            caption="ᴀᴋᴜ ᴍᴀsɪʜ ʜɪᴅᴜᴘ sᴀʏᴀɴɢ  !\n<b>sᴀʏᴀ ᴛɪᴅᴀᴋ ᴛɪᴅᴜʀ ʜɪɴɢɢᴀ​:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """Catat kesalahannya dan kirim pesan telegram untuk memberi tahu pengembang."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Pengecualian saat menangani pembaruan:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "Pengecualian muncul saat menangani pembaruan\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "» *ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ ᴛᴇʀsᴇᴅɪᴀ ᴜɴᴛᴜᴋ​​* *{}* :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_caption(text,
                parse_mode=ParseMode.MARKDOWN,
                
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_caption(HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


def Mukesh_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "mukesh_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_caption(f"*ʜᴇʏ,*❣️\n  *ɪɴɪ ᴀᴅᴀʟᴀʜ {dispatcher.bot.first_name}*"
            "\n*ᴍᴀɴᴀᴊᴇᴍᴇɴ ᴍᴜsɪᴋ ➕ ᴍᴀɴᴀᴊᴇᴍᴇɴ ɢʀᴜᴘ ᴄᴀɴɢɢɪʜ ʏᴀɴɢ ᴅɪʙᴜᴀᴛ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀɴᴛᴜ Aɴᴅᴀ ᴍᴇɴɢᴇʟᴏʟᴀ ɢʀᴜᴘ ᴅᴇɴɢᴀɴ ᴍᴜᴅᴀʜ ᴅᴀɴ ᴍᴇʟɪɴᴅᴜɴɢɪ ɢʀᴜᴘ Aɴᴅᴀ ᴅᴀʀɪ ᴘᴇɴɪᴘᴜ ᴅᴀɴ ᴘᴇɴɢɪʀɪᴍ sᴘᴀᴍ.*"
            "\n*ᴅɪᴛᴜʟɪs ᴅᴇɴɢᴀɴ ᴘʏᴛʜᴏɴ ᴅᴇɴɢᴀɴ sϙʟᴀʟᴄʜᴇᴍʏ ᴅᴀɴ ᴍᴏɴɢᴏᴅʙ sᴇʙᴀɢᴀɪ ᴅᴀᴛᴀʙᴀsᴇ.*"
            "\n\n────────────────────"
            f"\n*➻ ᴜᴩᴛɪᴍᴇ »* {uptime}"
            f"\n*➻ ᴜsᴇʀs »* {sql.num_users()}"
            f"\n*➻ ᴄʜᴀᴛs »* {sql.num_chats()}"
            "\n────────────────────"
            "\n\n➲  sᴀʏᴀ ᴅᴀᴘᴀᴛ ᴍᴇᴍʙᴀᴛᴀsɪ ᴘᴇɴɢɢᴜɴᴀ."
            "\n➲  ᴀᴋᴜ ᴘᴜɴʏᴀ sɪsᴛᴇᴍ ᴀɴᴛɪ ʙᴀɴᴊɪʀ ʏᴀɴɢ ᴄᴀɴɢɢɪʜ."
            "\n➲  sᴀʏᴀ ᴅᴀᴘᴀᴛ ᴍᴇɴʏᴀᴘᴀ ᴘᴇɴɢɢᴜɴᴀ ᴅᴇɴɢᴀɴ ᴘᴇsᴀɴ sᴇʟᴀᴍᴀᴛ ᴅᴀᴛᴀɴɢ ʏᴀɴɢ ᴅᴀᴘᴀᴛ ᴅɪsᴇsᴜᴀɪᴋᴀɴ ᴅᴀɴ ʙᴀʜᴋᴀɴ ᴍᴇɴᴇᴛᴀᴘᴋᴀɴ ᴀᴛᴜʀᴀɴ ɢʀᴜᴘ."
            "\n➲  sᴀʏᴀ ᴅᴀᴘᴀᴛ ᴍᴇᴍᴘᴇʀɪɴɢᴀᴛᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ sᴀᴍᴘᴀɪ ᴍᴇʀᴇᴋᴀ ᴍᴇɴᴄᴀᴘᴀɪ ᴍᴀᴋsɪᴍᴀʟ ᴘᴇʀɪɴɢᴀᴛᴀɴ, ᴅᴇɴɢᴀɴ sᴇᴛɪᴀᴘ ᴛɪɴᴅᴀᴋᴀɴ ʏᴀɴɢ ᴛᴇʟᴀʜ ᴅɪᴛᴇɴᴛᴜᴋᴀɴ sᴇᴘᴇʀᴛɪ ʙᴀɴ, ᴍᴜᴛᴇ, ᴋɪᴄᴋ, ᴅʟʟ."
            "\n➲  sᴀʏᴀ ᴍᴇᴍɪʟɪᴋɪ sɪsᴛᴇᴍ ᴘᴇɴᴄᴀᴛᴀᴛᴀɴ, ᴅᴀғᴛᴀʀ ʜɪᴛᴀᴍ, ᴅᴀɴ ʙᴀʜᴋᴀɴ ʙᴀʟᴀsᴀɴ ʏᴀɴɢ ᴛᴇʟᴀʜ ᴅɪᴛᴇɴᴛᴜᴋᴀɴ ᴘᴀᴅᴀ ᴋᴀᴛᴀ ᴋᴜɴᴄɪ ᴛᴇʀᴛᴇɴᴛᴜ."
            f"\n\n➻ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ʏᴀɴɢ ᴅɪʙᴇʀɪᴋᴀɴ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ʙᴀɴᴛᴜᴀɴ ᴅᴀɴ ɪɴғᴏʀᴍᴀsɪ ᴅᴀsᴀʀ ᴛᴇɴᴛᴀɴɢ {dispatcher.bot.first_name}.",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
        InlineKeyboardButton(text="🏡", callback_data="mukesh_back"),
        InlineKeyboardButton(text="🛡️", callback_data="mukesh_"),
        InlineKeyboardButton(text="💳", callback_data="source_"),
        InlineKeyboardButton(text="🧑‍💻", url=f"tg://user?id={OWNER_ID}"),
        InlineKeyboardButton(text="🖥️", callback_data="Main_help"),
     ],
                    [
                        InlineKeyboardButton(
                            text="🚩sᴜᴩᴩᴏʀᴛ", callback_data="mukesh_support"
                        ),
                        InlineKeyboardButton(
                            text="ᴄᴏᴍᴍᴀɴᴅs 💁", callback_data="Main_help"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="👨‍💻ᴅᴇᴠᴇʟᴏᴩᴇʀ", url=f"tg://user?id={OWNER_ID}"
                        ),
                        InlineKeyboardButton(
                            text="🥀sᴏᴜʀᴄᴇ",
                            callback_data="source_",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="◁", callback_data="mukesh_back"),
                    ],
                ]
            ),
        )
    elif query.data == "mukesh_support":
        query.message.edit_caption("**๏ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ʏᴀɴɢ ᴅɪʙᴇʀɪᴋᴀɴ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ʙᴀɴᴛᴜᴀɴ ᴅᴀɴ ɪɴғᴏʀᴍᴀsɪ ʟᴇʙɪʜ ʟᴀɴJᴜᴛ**"
            f"\n\nJɪᴋᴀ ᴀɴᴅᴀ ᴍᴇɴᴇᴍᴜᴋᴀɴ ʙᴜɢ ᴅɪ {dispatcher.bot.first_name} ᴀᴛᴀᴜ Jɪᴋᴀ ᴀɴᴅᴀ ɪɴɢɪɴ ᴍᴇᴍʙᴇʀɪᴋᴀɴ ᴛᴀɴɢɢᴀᴘᴀɴ ᴛᴇɴᴛᴀɴɢ {dispatcher.bot.first_name}, sɪʟᴀᴋᴀɴ ʟᴀᴘᴏʀᴋᴀɴ ᴅɪ ɢʀᴜᴘ sᴜᴘᴘᴏʀᴛ.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
        InlineKeyboardButton(text="🏡", callback_data="mukesh_back"),
        InlineKeyboardButton(text="🛡️", callback_data="mukesh_"),
        InlineKeyboardButton(text="💳", callback_data="source_"),
        InlineKeyboardButton(text="🧑‍💻", url=f"tg://user?id={OWNER_ID}"),
        InlineKeyboardButton(text="🖥️", callback_data="Main_help"),
     ],
                    [
                        InlineKeyboardButton(
                            text="🏡 sᴜᴩᴩᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"
                        ),
                        InlineKeyboardButton(
                            text="ᴜᴩᴅᴀᴛᴇs 🍷", url=f"\x68\x74\x74\x70\x73\x3A\x2F\x2F\x74\x2E\x6D\x65\x2F\x6D\x75\x6B\x65\x73\x68\x62\x6F\x74\x7A\x6F\x6E\x65"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="🥀 ᴅᴇᴠᴇʟᴏᴩᴇʀ", url=f"tg://user?id={OWNER_ID}"
                        ),
                        InlineKeyboardButton(
                            text="ɢɪᴛʜᴜʙ 🍹", url="\x68\x74\x74\x70\x73\x3A\x2F\x2F\x67\x69\x74\x68\x75\x62\x2E\x63\x6F\x6D\x2F\x6E\x6F\x6F\x62\x2D\x6D\x75\x6B\x65\x73\x68"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="◁", callback_data="mukesh_"),
                    ],
                ]
            ),
        )
    elif query.data == "mukesh_back":
        first_name = update.effective_user.first_name 
        query.message.edit_caption(PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME,sql.num_users(),sql.num_chats()),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
        )
def MukeshRobot_Main_Callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Main_help":
        query.message.edit_caption(f"""
 ʜᴇʀᴇ ɪꜱ ʜᴇʟᴘ ᴍᴇɴᴜ ꜰᴏʀ {BOT_NAME}
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="📕 Mᴀɴᴀɢᴇ", callback_data="help_back"),
                        InlineKeyboardButton(text="Mᴜsɪᴄ 🎶", callback_data="Music_")
                    ],
                    [
                        InlineKeyboardButton(text="💁 Bᴀsɪᴄ ", callback_data="basic_help"),
                        InlineKeyboardButton(text="Exᴘᴇʀᴛ 👮", callback_data="expert_help")
                    ],
                    [
                        InlineKeyboardButton(text="🍹 Aᴅᴠᴀɴᴄᴇ", callback_data="advance_help"),
                        InlineKeyboardButton(text="Dᴏɴᴀᴛɪᴏɴ 🎉", callback_data="donation_help") 
                    ],
                    [InlineKeyboardButton(text="• Hᴏᴍᴇ •", callback_data="mukesh_back")]
                ]
            ),
        )
    elif query.data=="basic_help":
        query.message.edit_caption("""ᴘᴇʀɪɴᴛᴀʜ ᴅᴀsᴀʀ.
👮🏻ᴛᴇʀsᴇᴅɪᴀ ᴜɴᴛᴜᴋ ᴀᴅᴍɪɴ ᴅᴀɴ ᴍᴏᴅᴇʀᴀᴛᴏʀ.
🕵🏻ᴛᴇʀsᴇᴅɪᴀ ᴜɴᴛᴜᴋ ᴀᴅᴍɪɴ.

👮🏻 /reload ᴍᴇᴍᴘᴇʀʙᴀʀᴜɪ ᴅᴀғᴛᴀʀ ᴀᴅᴍɪɴ.
🕵🏻 /settings ᴍᴇɴɢᴇʟᴏʟᴀ ᴅᴀɴ ᴘᴇɴɢᴀᴛᴜʀᴀɴ ʙᴏᴛ ᴅᴀʟᴀᴍ ɢʀᴜᴘ.
👮🏻 /ban ᴍᴇᴍᴜɴɢᴋɪɴᴋᴀɴ ᴀɴᴅᴀ ᴍᴇɴᴄᴇᴋᴀʟ ᴘᴇɴɢɢᴜɴᴀ ᴅᴀʀɪ ɢʀᴜᴘ ᴛᴀɴᴘᴀ ᴍᴇᴍʙᴇʀɪɴʏᴀ ᴋᴇᴍᴜɴɢᴋɪɴᴀɴ ᴜɴᴛᴜᴋ ʙᴇʀɢᴀʙᴜɴɢ ʟᴀɢɪ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ᴛᴀᴜᴛᴀɴ ɢʀᴜᴘ.
👮🏻 /mute ᴍᴇɴᴇᴍᴘᴀᴛᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴅᴀʟᴀᴍ ᴍᴏᴅᴇ ʜᴀɴʏᴀ ʙᴀᴄᴀ. ᴅɪᴀ ʙɪsᴀ ᴍᴇᴍʙᴀᴄᴀ ᴛᴀᴘɪ ᴅɪᴀ ᴛɪᴅᴀᴋ ʙɪsᴀ ᴍᴇɴɢɪʀɪᴍ ᴘᴇsᴀɴ ᴀᴘᴀ ᴘᴜɴ.
👮🏻 /kick ᴍᴇʟᴀʀᴀɴɢ ᴘᴇɴɢɢᴜɴᴀ ᴅᴀʀɪ ɢʀᴜᴘ, ᴍᴇᴍʙᴇʀɪɴʏᴀ ᴋᴇᴍᴜɴɢᴋɪɴᴀɴ ᴜɴᴛᴜᴋ ʙᴇʀɢᴀʙᴜɴɢ ʟᴀɢɪ ᴅᴇɴɢᴀɴ ᴛᴀᴜᴛᴀɴ ɢʀᴜᴘ.
👮🏻 /unban ᴍᴇᴍᴜɴɢᴋɪɴᴋᴀɴ ᴀɴᴅᴀ ᴍᴇɴɢʜᴀᴘᴜs ᴘᴇɴɢɢᴜɴᴀ ᴅᴀʀɪ ᴅᴀғᴛᴀʀ ʜɪᴛᴀᴍ ɢʀᴜᴘ, ᴍᴇᴍʙᴇʀɪ ᴍᴇʀᴇᴋᴀ ᴋᴇᴍᴜɴɢᴋɪɴᴀɴ ᴜɴᴛᴜᴋ ʙᴇʀɢᴀʙᴜɴɢ ʟᴀɢɪ ᴅᴇɴɢᴀɴ ᴛᴀᴜᴛᴀɴ ɢʀᴜᴘ.
👮🏻 /info ᴍᴇᴍʙᴇʀɪᴋᴀɴ ɪɴғᴏʀᴍᴀsɪ ᴛᴇɴᴛᴀɴɢ ᴘᴇɴɢɢᴜɴᴀ.

◽️ /staff ᴍᴇᴍʙᴇʀɪᴋᴀɴ ᴅᴀғᴛᴀʀ ʟᴇɴɢᴋᴀᴘ sᴛᴀғ ɢʀᴜᴘ!.""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="Main_help"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="mukesh_support")
                    ]
                ]
            ),
            )
    elif query.data=="mukesh_back":
        query.message.edit_caption("""ᴘᴇʀɪɴᴛᴀʜ ᴀʜʟɪ

👥 ᴛᴇʀsᴇᴅɪᴀ ᴜɴᴛᴜᴋ sᴇᴍᴜᴀ ᴘᴇɴɢɢᴜɴᴀ.
👮🏻 ᴛᴇʀsᴇᴅɪᴀ ᴜɴᴛᴜᴋ ᴀᴅᴍɪɴ ᴅᴀɴ ᴍᴏᴅᴇʀᴀᴛᴏʀ.
🕵🏻 ᴛᴇʀsᴇᴅɪᴀ ᴜɴᴛᴜᴋ ᴀᴅᴍɪɴ.

🕵🏻  /unbanall ᴀɴɢɢᴏᴛᴀ ᴅᴀʀɪ ɢʀᴜᴘ ᴀɴᴅᴀ
👮🏻  /unmuteall sᴜᴀʀᴀᴋᴀɴ sᴇᴍᴜᴀ ᴅᴀʀɪ ɢʀᴜᴘ ᴀɴᴅᴀ

ᴘᴇsᴀɴ sᴇᴍᴀᴛᴀɴ
🕵🏻  /pin [ᴘᴇsᴀɴ] ᴍᴇɴɢɪʀɪᴍ ᴘᴇsᴀɴ ᴍᴇʟᴀʟᴜɪ ʙᴏᴛ ᴅᴀɴ ᴍᴇɴʏᴇᴍᴀᴛᴋᴀɴɴʏᴀ.
🕵🏻  /pin ᴍᴇɴʏᴇᴍᴀᴛᴋᴀɴ ᴘᴇsᴀɴ sᴇʙᴀɢᴀɪ ʙᴀʟᴀsᴀɴ
🕵🏻  /unpin ʜᴀᴘᴜs ᴘᴇsᴀɴ ʏᴀɴɢ ᴅɪsᴇᴍᴀᴛᴋᴀɴ.
🕵🏻  /adminlist ᴅᴀғᴛᴀʀ sᴇᴍᴜᴀ ᴘᴇʀᴀɴ ᴋʜᴜsᴜs ʏᴀɴɢ ᴅɪʙᴇʀɪᴋᴀɴ ᴋᴇᴘᴀᴅᴀ ᴘᴇɴɢɢᴜɴᴀ.

◽️ /bug: (ᴘᴇsᴀɴ) ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍ ᴘᴇsᴀɴ ᴅᴀɴ ᴋᴇsᴀʟᴀʜᴀɴ ʏᴀɴɢ ᴀɴᴅᴀ ʜᴀᴅᴀᴘɪ 
ᴇx: /bug ʜᴇɪ ᴀᴅᴀ sᴇsᴜᴀᴛᴜ ʏᴀɴɢ ᴇʀʀᴏʀ @Username ᴏʙʀᴏʟᴀɴ! .""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="Main_help"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="mukesh_support")
                    ]
                ]
            ),
            )                                        
    elif query.data=="advance_help":
        query.message.edit_caption("""ᴘᴇʀɪɴᴛᴀʜ ʟᴀɴJᴜᴛᴀɴ

👮🏻ᴛᴇʀsᴇᴅɪᴀ ᴜɴᴛᴜᴋ ᴀᴅᴍɪɴ ᴅᴀɴ ᴍᴏᴅᴇʀᴀᴛᴏʀ.
🕵🏻ᴛᴇʀsᴇᴅɪᴀ ᴜɴᴛᴜᴋ ᴀᴅᴍɪɴ.
🛃 ᴛᴇʀsᴇᴅɪᴀ ᴜɴᴛᴜᴋ ᴀᴅᴍɪɴ & ᴘᴇᴍʙᴇʀsɪʜ

ᴍᴇᴍᴘᴇʀɪɴɢᴀᴛᴋᴀɴ ᴍᴀɴᴀJᴇᴍᴇɴ
👮🏻  /warn ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ᴘᴇʀɪɴɢᴀᴛᴀɴ ᴋᴇᴘᴀᴅᴀ ᴘᴇɴɢɢᴜɴᴀ
👮🏻  /unwarn ʜᴀᴘᴜs ᴘᴇʀɪɴɢᴀᴛᴀɴ ᴋᴇᴘᴀᴅᴀ ᴘᴇɴɢɢᴜɴᴀ
👮🏻  /warns ᴍᴇᴍᴜɴɢᴋɪɴᴋᴀɴ ᴀɴᴅᴀ ᴍᴇʟɪʜᴀᴛ ᴅᴀɴ ᴍᴇɴɢᴇʟᴏʟᴀ ᴘᴇʀɪɴɢᴀᴛᴀɴ ᴘᴇɴɢɢᴜɴᴀ

🛃  /del ᴍᴇɴɢʜᴀᴘᴜs ᴘᴇsᴀɴ
🛃  /purge ᴍᴇɴɢʜᴀᴘᴜs ᴅᴀʀɪ ᴘᴇsᴀɴ ʏᴀɴɢ ᴅɪᴘɪʟɪʜ.""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="Main_help"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="mukesh_support")
                    ]
                ]
            ),
            )
    elif query.data=="expert_help":
        query.message.edit_caption(f"""━━━━━━━━━━━━━━━━━━━━
Jᴀᴅɪᴋᴀɴ ɢʀᴜᴘ ᴀɴᴅᴀ ᴇғᴇᴋᴛɪғ sᴇᴋᴀʀᴀɴɢ :
🎉 ᴄᴏɴɢʀᴀɢᴜʟᴀᴛɪᴏɴꜱ 🎉
[{BOT_NAME}]("https://t.me/{BOT_USERNAME}") sᴇᴋᴀʀᴀɴɢ sɪᴀᴘ ᴜɴᴛᴜᴋ
ᴍᴇɴɢᴇʟᴏʟᴀ ɢʀᴜᴘ ᴀɴᴅᴀ.

ᴀʟᴀᴛ ᴀᴅᴍɪɴ :
ᴀʟᴀᴛ ᴀᴅᴍɪɴ ᴅᴀsᴀʀ ᴍᴇᴍʙᴀɴᴛᴜ ᴀɴᴅᴀ
ᴍᴇʟɪɴᴅᴜɴɢɪ & ᴍᴇᴍᴘᴇʀᴋᴜᴀᴛ ɢʀᴜᴘ ᴀɴᴅᴀ.
ᴀɴᴅᴀ ᴅᴀᴘᴀᴛ ᴍᴇʟᴀʀᴀɴɢ, ᴍᴇɴᴇɴᴅᴀɴɢ, ᴍᴇᴍᴘʀᴏᴍᴏsɪᴋᴀɴ
ᴀɴɢɢᴏᴛᴀ sᴇʙᴀɢᴀɪ ᴀᴅᴍɪɴ ᴍᴇʟᴀʟᴜɪ ʙᴏᴛ.

sᴀʟᴀᴍ :
ᴍᴀʀɪ ᴀᴛᴜʀ ᴘᴇsᴀɴ sᴇʟᴀᴍᴀᴛ ᴅᴀᴛᴀɴɢ
ᴜɴᴛᴜᴋ ᴍᴇɴʏᴀᴍʙᴜᴛ ᴘᴇɴɢɢᴜɴᴀ ʙᴀʀᴜ
ʏᴀɴɢ ᴅᴀᴛᴀɴɢ ᴋᴇ ɢʀᴜᴘ ᴀɴᴅᴀ.
ᴋɪʀɪᴍ /setwelcome ᴘᴇsᴀɴ ᴜɴᴛᴜᴋ 
ᴍᴇɴɢᴀᴛᴜʀ ᴘᴇsᴀɴ sᴇʟᴀᴍᴀᴛ ᴅᴀᴛᴀɴɢ!""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="Main_help"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="mukesh_support")
                    ]
                ]
            ),
            )
    elif query.data=="donation_help":
        query.message.edit_caption("""ᴀᴘᴀᴋᴀʜ ᴀɴᴅᴀ ᴛᴇʀᴛᴀʀɪᴋ ᴍᴇᴍʙᴀɴᴛᴜ ᴘᴇɴᴄɪᴘᴛᴀ sᴀʏᴀ ᴅᴇɴɢᴀɴ ᴜᴘᴀʏᴀɴʏᴀ ᴀɢᴀʀ sᴀʏᴀ ᴛᴇᴛᴀᴘ ᴀᴋᴛɪғ ʙᴇʀᴋᴇᴍʙᴀɴɢ? Jɪᴋᴀ ʏᴀ, ᴀɴᴅᴀ ʙᴇʀᴀᴅᴀ ᴅɪ ᴛᴇᴍᴘᴀᴛ ʏᴀɴɢ ᴛᴇᴘᴀᴛ. 

ᴋᴀᴍɪ ᴍᴇɴᴇᴋᴀɴᴋᴀɴ ᴘᴇɴᴛɪɴɢɴʏᴀ ᴋᴇʙᴜᴛᴜʜᴀɴ ᴅᴀɴᴀ ᴜɴᴛᴜᴋ ᴍᴇɴJᴀɢᴀ BᴇᴇSᴘᴏᴛɪғʏ ᴅᴀʟᴀᴍ ᴘᴇɴɢᴇᴍʙᴀɴɢᴀɴ ᴀᴋᴛɪғ, sᴜᴍʙᴀɴɢᴀɴ ᴀɴᴅᴀ ᴅᴀʟᴀᴍ Jᴜᴍʟᴀʜ ʙᴇʀᴀᴘᴀ ᴘᴜɴ ᴋᴇ sᴇʀᴠᴇʀ BᴇᴇSᴘᴏᴛɪғʏ ᴅᴀɴ ᴜᴛɪʟɪᴛᴀs ʟᴀɪɴɴʏᴀ ᴀᴋᴀɴ ᴍᴇᴍᴜɴɢᴋɪɴᴋᴀɴ ᴋᴀᴍɪ ᴍᴇᴍᴘᴇʀᴛᴀʜᴀɴᴋᴀɴ ᴜᴍᴜʀ ᴅᴀʟᴀᴍ Jᴀɴɢᴋᴀ ᴘᴀɴJᴀɴɢ. ᴋᴀᴍɪ ᴀᴋᴀɴ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ sᴇᴍᴜᴀ ᴅᴏɴᴀsɪ ᴜɴᴛᴜᴋ ᴍᴇɴᴜᴛᴜᴘɪ ᴘᴇɴɢᴇʟᴜᴀʀᴀɴ ᴅɪ ᴍᴀsᴀ ᴅᴇᴘᴀɴ ᴅᴀɴ ʙɪᴀʏᴀ ᴘᴇɴɪɴɢᴋᴀᴛᴀɴ sᴇʀᴠᴇʀ. Jɪᴋᴀ ᴀɴᴅᴀ ᴍᴇᴍɪʟɪᴋɪ ᴜᴀɴɢ ᴄᴀᴅᴀɴɢᴀɴ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀɴᴛᴜ PBB ᴅᴀʟᴀᴍ ᴜᴘᴀʏᴀ ɪɴɪ, sɪʟᴀᴋᴀɴ ʟᴀᴋᴜᴋᴀɴ ɪᴛᴜ ᴅᴀɴ ᴅᴏɴᴀsɪ ᴀɴᴅᴀ Jᴜɢᴀ ᴅᴀᴘᴀᴛ ᴍᴇᴍᴏᴛɪᴠᴀsɪ ᴋᴀᴍɪ ᴜɴᴛᴜᴋ ᴛᴇʀᴜs ᴍᴇᴍʙᴇʀɪᴋᴀɴ ʙᴀɴᴛᴜᴀɴ ʙᴀʀᴜ.

ᴀɴᴅᴀ ᴅᴀᴘᴀᴛ ᴍᴇᴍʙᴀɴᴛᴜ ᴘᴇɴɢᴇᴍʙᴀɴɢᴀɴ ᴅᴇɴɢᴀɴ ᴅᴏɴᴀsɪ""",parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [ [
        InlineKeyboardButton(text="🏡", callback_data="mukesh_back"),
        InlineKeyboardButton(text="🛡️", callback_data="mukesh_"),
        InlineKeyboardButton(text="💳", callback_data="source_"),
        InlineKeyboardButton(text="🧑‍💻", url=f"tg://user?id={OWNER_ID}"),
        InlineKeyboardButton(text="🖥️", callback_data="Main_help"),
     ],
                    [
                        InlineKeyboardButton(text="• Dᴏɴᴀᴛᴇ •", url="https://t.me/mukeshbotzone/7"),InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", callback_data="mukesh_support")
                    ]
                ]
            ),
            )  
def Source_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_caption(
            f"""
*ʜᴇʏ,
 ɪɴɪ {BOT_NAME},
ʙᴏᴛ ᴍᴀɴᴀJᴇᴍᴇɴ ɢʀᴜᴘ ᴛᴇʟᴇɢʀᴀᴍ sᴜᴍʙᴇʀ ᴛᴇʀʙᴜᴋᴀ.*

ᴅɪᴛᴜʟɪs ᴅᴇɴɢᴀɴ ᴘʏᴛʜᴏɴ ᴅᴇɴɢᴀɴ ʙᴀɴᴛᴜᴀɴ : [ᴛᴇʟᴇᴛʜᴏɴ](https://github.com/LonamiWebs/Telethon)
[ᴩʏʀᴏɢʀᴀᴍ](https://github.com/pyrogram/pyrogram)
[ᴩʏᴛʜᴏɴ-ᴛᴇʟᴇɢʀᴀᴍ-ʙᴏᴛ](https://github.com/python-telegram-bot/python-telegram-bot)
ᴅᴀɴ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ [sǫʟᴀʟᴄʜᴇᴍʏ](https://www.sqlalchemy.org) ᴅᴀɴ [ᴍᴏɴɢᴏ](https://cloud.mongodb.com) sᴇʙᴀɢᴀɪ ᴅᴀᴛᴀʙᴀsᴇ.


*ᴅɪsɪɴɪ ᴀᴅᴀʟᴀʜ sᴜᴍʙᴇʀ ᴋᴏᴅᴇ sᴀʏᴀ :* [ɢɪᴛʜᴜʙ](\x68\x74\x74\x70\x73\x3A\x2F\x2F\x67\x69\x74\x68\x75\x62\x2E\x63\x6F\x6D\x2F\x4E\x6F\x6F\x62\x2D\x4D\x75\x6B\x65\x73\x68\x2F\x4D\x75\x6B\x65\x73\x68\x52\x6F\x62\x6F\x74)


{BOT_NAME} ʙᴇʀʟɪsᴇɴsɪ ᴅɪ ʙᴀᴡᴀʜ [ᴍɪᴛ ʟɪᴄᴇɴsᴇ](\x68\x74\x74\x70\x73\x3A\x2F\x2F\x67\x69\x74\x68\x75\x62\x2E\x63\x6F\x6D\x2F\x4E\x6F\x6F\x62\x2D\x4D\x75\x6B\x65\x73\x68\x2F\x4D\x75\x6B\x65\x73\x68\x52\x6F\x62\x6F\x74/blob/main/LICENSE).
© 2023 - 2024 | [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ](https://t.me/{SUPPORT_CHAT}), sᴇʟᴜʀᴜʜ ʜᴀᴋ ᴄɪᴘᴛᴀ.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [[
        InlineKeyboardButton(text="sᴏᴜʀᴄᴇ", url="\x68\x74\x74\x70\x73\x3A\x2F\x2F\x67\x69\x74\x68\x75\x62\x2E\x63\x6F\x6D\x2F\x4E\x6F\x6F\x62\x2D\x4D\x75\x6B\x65\x73\x68\x2F\x4D\x75\x6B\x65\x73\x68\x52\x6F\x62\x6F\x74")
                ],
                 [
        InlineKeyboardButton(text="🏡", callback_data="mukesh_back"),
        InlineKeyboardButton(text="🛡️", callback_data="mukesh_"),
        InlineKeyboardButton(text="💳", callback_data="source_"),
        InlineKeyboardButton(text="🧑‍💻", url=f"tg://user?id={OWNER_ID}"),
        InlineKeyboardButton(text="🖥️", callback_data="Main_help"),
     ],[InlineKeyboardButton(text="◁", callback_data="source_back")]]
            ),
        )
    elif query.data == "source_back":
        first_name = update.effective_user.first_name
        query.message.edit_caption(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME,sql.num_users(),sql.num_chats()),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            
        )

        
def Music_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Music_":
        query.message.edit_caption(f"""
  ᴅɪsɪɴɪ ᴀᴅᴀʟᴀʜ ᴍᴇɴᴜ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴍᴜsɪᴋ
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
        InlineKeyboardButton(text="🏡", callback_data="mukesh_back"),
        InlineKeyboardButton(text="🛡️", callback_data="mukesh_"),
        InlineKeyboardButton(text="💳", callback_data="source_"),
        InlineKeyboardButton(text="🧑‍💻", url=f"tg://user?id={OWNER_ID}"),
        InlineKeyboardButton(text="🖥️", callback_data="Main_help"),
     ],
                    [
                        InlineKeyboardButton(
                            text="⍟ ᴀᴅᴍɪɴ ⍟", callback_data="Music_admin"
                        ),
                        InlineKeyboardButton(
                            text="⍟ ᴘʟᴀʏ ⍟", callback_data="Music_play"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="⍟ ʙᴏᴛ ⍟", callback_data="Music_bot"),
                        InlineKeyboardButton(
                            text="⍟ ᴇxᴛʀᴀ ⍟",
                            callback_data="Music_extra",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="Main_help")
                    ],
                ]
            ),
        )
    elif query.data == "Music_admin":
        query.message.edit_caption(f"*» ᴘᴇʀɪɴᴛᴀʜ ᴀᴅᴍɪɴ «*"
            f"""
ᴛᴀᴍʙᴀʜᴋᴀɴ sᴀᴊᴀ *ᴄ* ᴅɪ ᴀᴡᴀʟ ᴘᴇʀɪɴᴛᴀʜ ᴜɴᴛᴜᴋ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ sᴀʟᴜʀᴀɴ.

/pause : ᴊᴇᴅᴀ sᴛʀᴇᴀᴍɪɴɢ ʏᴀɴɢ sᴇᴅᴀɴɢ ᴅɪ ᴘᴜᴛᴀʀ.

/resume : ᴍᴇʟᴀɴᴊᴜᴛᴋᴀɴ sᴛʀᴇᴀᴍɪɴɢ ʏᴀɴɢ ᴅɪ ᴊᴇᴅᴀ.

/skip : ᴍᴇʟᴇᴡᴀᴛɪ ʟᴀɢᴜ ʏᴀɴɢ sᴜᴅᴀʜ ᴅɪ ᴘᴜᴛᴀʀ.

/end ᴏʀ /stop : ᴍᴇᴍᴀᴛɪᴋᴀɴ ᴅᴀɴ ᴍᴇᴍʙᴇʀʜᴇɴᴛɪᴋᴀɴ ʟᴀɢᴜ ʏᴀɴɢ sᴜᴅᴀʜ ᴅɪ ᴘᴜᴛᴀʀ.

/player : ᴅᴀᴘᴀᴛᴋᴀɴ ᴘᴀɴᴇʟ ᴘᴇᴍᴜᴛᴀʀ ɪɴᴛᴇʀᴀᴋᴛɪғ.

/queue : ᴍᴇɴᴀᴍᴘɪʟᴋᴀɴ ᴅᴀғᴛᴀʀ ʟᴀɢᴜ ʏᴀɴɢ ᴅɪ ᴀɴᴛʀɪ.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" ʙᴀᴄᴋ ", callback_data="Music_"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_play":
        query.message.edit_caption(f"*» ᴘᴇʀɪɴᴛᴀʜ ᴘʟᴀʏ «*"
            f"""
/play or /vplay or /cplay  - ᴍᴇᴍᴜᴛᴀʀ ʟᴀɢᴜ ʏᴀɴɢ ᴅɪ ᴍɪɴᴛᴀ.

/playforce or /vplayforce or /cplayforce -  ғᴏʀᴄᴇ ᴘʟᴀʏ ᴍᴇɴɢʜᴇɴᴛɪᴋᴀɴ ᴛʀᴇᴋ ʏᴀɴɢ sᴇᴅᴀɴɢ ᴅɪᴘᴜᴛᴀʀ ᴅɪ ᴏʙʀᴏʟᴀɴ sᴜᴀʀᴀ ᴅᴀɴ ᴍᴜʟᴀɪ ᴍᴇᴍᴜᴛᴀʀ ᴛʀᴇᴋ ʏᴀɴɢ ᴅɪᴄᴀʀɪ sᴇᴄᴀʀᴀ ɪɴsᴛᴀɴ ᴛᴀɴᴘᴀ ᴍᴇɴɢɢᴀɴɢɢᴜ/ᴍᴇɴɢʜᴀᴘᴜs ᴀɴᴛʀɪᴀɴ.

/channelplay [ᴄʜᴀᴛ ᴜꜱᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ] ᴏʀ [ᴅɪꜱᴀʙʟᴇ] - sᴀᴍʙᴜɴɢᴋᴀɴ sᴀʟᴜʀᴀɴ ᴋᴇ ɢʀᴜᴘ ᴅᴀɴ sᴛʀᴇᴀᴍɪɴɢ ᴍᴜsɪᴋ ᴅɪ sᴀʟᴜʀᴀɴ ᴏʙʀᴏʟᴀɴ sᴜᴀʀᴀ ᴅᴀʀɪ ɢʀᴜᴘ ᴀɴᴅᴀ.


*ᴘᴇʀɪɴᴛᴀʜ ʙᴏᴛ*
 ᴅᴀғᴛᴀʀ ᴘᴜᴛᴀʀ sᴇʀᴠᴇʀ ʙᴏᴛ:
/playlist  - ᴘᴇʀɪᴋsᴀ ᴅᴀғᴛᴀʀ ᴘᴜᴛᴀʀ ᴀɴᴅᴀ ʏᴀɴɢ ᴅɪsɪᴍᴘᴀɴ ᴅɪ sᴇʀᴠᴇʀ.
/deleteplaylist - ᴍᴇɴɢʜᴀᴘᴜs ᴅᴀғᴛᴀʀ ᴘᴜᴛᴀʀ ᴀɴᴅᴀ ʏᴀɴɢ ᴅɪsɪᴍᴘᴀɴ ᴅɪ sᴇʀᴠᴇʀ
/play  - ᴍᴇᴍᴜᴛᴀʀ ᴅᴀғᴛᴀʀ ᴘᴜᴛᴀʀ ʏᴀɴɢ ᴀɴᴅᴀ sɪᴍᴘᴀɴ ᴅɪ sᴇʀᴠᴇʀ.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="Music_"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_bot":
        query.message.edit_caption(f"*» ᴘᴇʀɪɴᴛᴀʜ ʙᴏᴛ «*"
            f"""
/stats - ᴅᴀᴘᴀᴛᴋᴀɴ 𝟷𝟶 ʟᴀɢᴜ ᴛᴇʀᴀᴛᴀs sᴛᴀᴛɪsᴛɪᴋ ɢʟᴏʙᴀʟ, 𝟷𝟶 ᴘᴇɴɢɢᴜɴᴀ ʙᴏᴛ ᴛᴇʀᴀᴛᴀs, 𝟷𝟶 ᴏʙʀᴏʟᴀɴ ᴛᴇʀᴀᴛᴀs ᴅɪ ʙᴏᴛ, 𝟷𝟶 ᴛᴇʀᴀᴛᴀs ᴅɪᴘᴜᴛᴀʀ ᴅᴀʟᴀᴍ ᴏʙʀᴏʟᴀɴ, ᴅʟʟ.

/sudolist - ᴘᴇʀɪᴋsᴀ sᴜᴅᴏ ᴘᴇɴɢɢᴜɴᴀ ʙᴏᴛ ᴀʙɢ.

/lyrics [ɴᴀᴍᴀ ᴍᴜsɪᴄ] - ᴍᴇɴᴄᴀʀɪ ʟɪʀɪᴋ ᴜɴᴛᴜᴋ ᴍᴜsɪᴋ ᴛᴇʀᴛᴇɴᴛᴜ ᴅɪ ᴡᴇʙ.

/song [ɴᴀᴍᴀ ᴛʀᴀᴄᴋ] or [ʏᴛ ʟɪɴᴋ] - ᴜɴᴅᴜʜ ʟᴀɢᴜ ᴀᴘᴀ ᴘᴜɴ ᴅᴀʀɪ ʏᴏᴜᴛᴜʙᴇ ᴅᴀʟᴀᴍ ғᴏʀᴍᴀᴛ ᴍᴘ𝟹 ᴀᴛᴀᴜ ᴍᴘ𝟺.

/player -  ᴅᴀᴘᴀᴛᴋᴀɴ ᴘᴀɴᴇʟ ʙᴇʀᴍᴀɪɴ ɪɴᴛᴇʀᴀᴋᴛɪғ.

c sɪɴɢᴋᴀᴛᴀɴ ᴅᴀʀɪ ᴘᴇᴍᴜᴛᴀʀᴀɴ sᴀʟᴜʀᴀɴ.

/queue ᴏʀ /cqueue- ᴘᴇʀɪᴋsᴀ ᴅᴀғᴛᴀʀ ᴀɴᴛʀɪᴀɴ ᴍᴜsɪᴋ.
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" ʙᴀᴄᴋ ", callback_data="Music_"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_extra":
        query.message.edit_caption(f"*» ᴘᴇʀɪɴᴛᴀʜ ᴛᴀᴍʙᴀʜᴀɴ «*"
            f"""
/mstart - ᴍᴇᴍᴜʟᴀɪ ᴍᴜsɪᴋ ʙᴏᴛ.
/mhelp  - ᴅᴀᴘᴀᴛᴋᴀɴ ᴍᴇɴᴜ ᴘᴇᴍʙᴀɴᴛᴜ ᴘᴇʀɪɴᴛᴀʜ ᴅᴇɴɢᴀɴ ᴘᴇɴJᴇʟᴀsᴀɴ ʀɪɴᴄɪ ᴛᴇɴᴛᴀɴɢ ᴘᴇʀɪɴᴛᴀʜ.
/ping- ᴘɪɴɢ ʙᴏᴛ ᴅᴀɴ ᴘᴇʀɪᴋsᴀ sᴛᴀᴛɪsᴛɪᴋ ʀᴀᴍ, ᴄᴘᴜ ᴅʟʟ ᴅᴀʀɪ ʙᴏᴛ.

*ᴘᴇɴɢᴀᴛᴜʀᴀɴ ɢʀᴜᴘ:*
/settings - ᴅᴀᴘᴀᴛᴋᴀɴ ᴘᴇɴɢᴀᴛᴜʀᴀɴ ɢʀᴜᴘ ɪɴʟɪɴᴇ ᴅʟʟ
""",
            parse_mode=ParseMode.MARKDOWN,
            
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=" ʙᴀᴄᴋ ", callback_data="Music_"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support")
                    ]
                ]
            ),
        )
    elif query.data == "Music_back":
        first_name = update.effective_user.first_name
        query.message.edit_caption(PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,

        )


def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_photo(START_IMG,
                f"Hubungi saya di PM untuk mendapatkan bantuan {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=" ʜᴇʟᴘ ​",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_photo(START_IMG,"» ᴅɪᴍᴀɴᴀ ᴀɴᴅᴀ ɪɴɢɪɴ ᴍᴇᴍʙᴜᴋᴀ ᴍᴇɴᴜ ᴘᴇɴɢᴀᴛᴜʀᴀɴ?.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="👤 ᴩʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ",
                            url="https://t.me/{}?start=help".format(context.bot.username),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="👥 ʙᴜᴋᴀ ᴅɪsɪɴɪ",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Berikut adalah bantuan yang tersedia untuk *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="◁", callback_data="help_back"),InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="mukesh_support")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "Ini adalah pengaturan anda saat ini:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Sepertinya tidak ada pengaturan khusus pengguna yang tersedia :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Modul mana yang ingin anda periksa {}'s pengaturan untuk?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Sepertinya tidak ada pengaturan obrolan yang tersedia :'(\nSend this "
                "dalam obrolan grup tempat anda menjadi admin untuk menemukan pengaturannya saat ini!",
                parse_mode=ParseMode.MARKDOWN,
            )


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* memiliki pengaturan berikut untuk *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="◁",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text("""Hai, yang di sana! Ada beberapa pengaturan untuk {} - silakan pilih apa "
                kamu tertarik.""".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(text=
                """Hai, yang di sana! Ada beberapa pengaturan untuk {} - silakan pilih apa 
                kamu tertarik.""".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text("""Hai, yang di sana! Ada beberapa pengaturan untuk {} - silakan pilih apa 
                kamu tertarik.""".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Pesan tidak diubah",
            "Query_id_invalid",
            "Pesan tidak dapat dihapus",
        ]:
            LOGGER.exception("Pengecualian pada tombol pengaturan. %s", str(query.data))


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "ᴋʟɪᴋ ᴅɪ sɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ᴘᴇɴɢᴀᴛᴜʀᴀɴ ᴏʙʀᴏʟᴀɴ ɪɴɪ ᴅᴀɴ Jᴜɢᴀ ᴘᴇɴɢᴀᴛᴜʀᴀɴ ᴀɴᴅᴀ"
            msg.reply_photo(START_IMG,text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ᴘᴇɴɢᴀᴛᴜʀᴀɴ",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "ᴋʟɪᴋ ᴅɪsɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴋᴀ ᴘᴇɴɢᴀᴛᴜʀᴀɴ"

    else:
        send_settings(chat.id, user.id, True)


def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 756731910:
            update.effective_message.reply_text(
                f"» ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴩᴇʀ ᴏғ {dispatcher.bot.first_name} sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ɪs [ɢɪᴛʜᴜʙ](https://github.com/BeeDomp/BeeSpotify)"
                f"\n\nᴛᴇᴛᴀᴘɪ ᴀɴᴅᴀ ᴅᴀᴘᴀᴛ ʙᴇʀᴅᴏɴᴀsɪ ᴋᴇᴘᴀᴅᴀ ᴏʀᴀɴɢ ʏᴀɴɢ sᴀᴀᴛ ɪɴɪ ᴍᴇɴJᴀʟᴀɴᴋᴀɴ sᴀʏᴀ : [ᴅɪsɪɴɪ]({DONATE_STRING})",
                parse_mode=ParseMode.MARKDOWN,
                
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                
            )

            update.effective_message.reply_text(
                "ᴀᴋᴜ sᴜᴅᴀʜ ᴍᴇɴɢɪʀɪᴍɪᴍᴜ ᴘᴇsᴀɴ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴇʀɪ sᴜᴍʙᴀɴɢᴀɴ ᴘᴀᴅᴀ ᴘᴇɴᴄɪᴘᴛᴀᴋᴜ!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "ʜᴜʙᴜɴɢɪ sᴀʏᴀ ᴅɪ ᴘᴍ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ɪɴғᴏʀᴍᴀsɪ ᴅᴏɴᴀsɪ."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Bermigrasi dari %s, ke %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Berhasil bermigrasi!")
    raise DispatcherHandlerStop


def main():
    global x
    x=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="➕ᴛᴀᴍʙᴀʜᴋᴀɴ sᴀʏᴀ ᴋᴇ ᴏʙʀᴏʟᴀɴ ᴀɴᴅᴀ➕",
                            url="https://t.me/BeeMusicSpotify_bot?startgroup=true"
                            )
                       ]
                ]
                     )
    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.send_photo(
                f"@{SUPPORT_CHAT}",
                photo=f"{START_IMG}",
                caption=f"""
🔱ㅤ{BOT_NAME} ᴍᴀsɪʜ ʜɪᴅᴜᴘ sᴀʏᴀɴɢ.
━━━━━━━━━━━━━
**ᴅɪʙᴜᴀᴛ ❤️ ᴏʟᴇʜ BᴇᴇDᴏᴍᴘ**
**ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ:** `{y()}`
**ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ:** `{telever}`
**ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ:** `{tlhver}`
**ᴩʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ:** `{pyrover}`
━━━━━━━━━━━━━
""",reply_markup=x,
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                f"Bot tidak dapat mengirim pesan ke @{SUPPORT_CHAT}, pergi dan periksa!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)
    start_handler = CommandHandler("start", start, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(
        help_button, pattern=r"help_.*", run_async=True
    )

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(
        settings_button, pattern=r"stngs_", run_async=True
    )

    about_callback_handler = CallbackQueryHandler(
        Mukesh_about_callback, pattern=r"mukesh_", run_async=True
    )
    source_callback_handler = CallbackQueryHandler(
        Source_about_callback, pattern=r"source_", run_async=True
    )
    music_callback_handler = CallbackQueryHandler(
        Music_about_callback, pattern=r"Music_",run_async=True
    )
    mukeshrobot_main_handler = CallbackQueryHandler(
        MukeshRobot_Main_Callback, pattern=r".*_help",run_async=True)
    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(music_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)
    dispatcher.add_handler(mukeshrobot_main_handler)
    dispatcher.add_error_handler(error_callback)
    dispatcher.add_handler(source_callback_handler)
    LOGGER.info("Using long polling.")
    updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Modul berhasil dimuat: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
