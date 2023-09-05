from random import randint

from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)

from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler
)

import sys
sys.path.append('D:/GitHub/')

from mysecrets.pztg.passcodes import TOKEN, BOT_USERNAME

""" import pyzagi as pz
print(pz.version)
raise ValueError('Stop') """

kbuttons = [
    [KeyboardButton("🎇 Create request")],
    [KeyboardButton("🍰 Create cake")],
]
YNBUTTONS = [
    [InlineKeyboardButton('Yes', callback_data="y"), 
     InlineKeyboardButton('No', callback_data="n")]
]

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text("Yo! Let's start!",
                                    reply_markup = ReplyKeyboardMarkup(kbuttons))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands: \n /getcases")

async def getcases_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('cases!')

async def getprocesses_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # text = pz.getprocesses(pz.headers)
    text='empty///'
    await update.message.reply_text(text)

# Responses
class CaseCreationWrapper():
    CASECREATIONRID = 'CASECREATION'
    CaseCreationWelcome = "You are going to create a request in the BPM system."

def handle_resp(text: str)->str:
    processed: str = text.lower()
    if 'beez' in processed:
        return 'BEEEEEEEZZ'
    elif 'create' in processed:
        if 'request' in processed:            
            return CaseCreationWrapper.CASECREATIONRID
        elif 'cake' in processed:
            """ Portal GLADOS Quotes
            """
            cake_resp = ['The cake is a lie.',                         
                         'Quit now and cake will be served immediately.',
                         'Cake and grief counseling will be available at the conclusion of the test.',
                         'Enrichment Center regulations require both hands to be empty before any cake can be served.',
                         'Uh oh. Somebody cut the cake. I told them to wait for you, but they did it anyway. There is still some left, though, if you hurry back.',
                         "Who's gonna make the cake when I'm gone? You?"]
            cakeid = randint(0,len(cake_resp)-1)
            print(cakeid)
            return cake_resp[cakeid]
        else:
            return 'I am not sure about this...'
    return "somethin' wrong, can you feel it?"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # talking in group or private
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_resp(new_text)
        else:
            return
    else:
        response: str = handle_resp(text)
    
    print('Bot', response)

    if response == CaseCreationWrapper.CASECREATIONRID:
        await handle_createrequest(update)
    else:
        await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


async def handle_createrequest(update):
    await update.message.reply_text(CaseCreationWrapper.CaseCreationWelcome)
    await update.message.reply_text("Please select a start date: ")
    await update.message.reply_text("Please select an end date: ")
    await update.message.reply_text("Do you want to provide a commentary?",
                                    reply_markup=create_YNIK())

def create_YNIK():
    """Create Yes/No Inline Keyboard"""
    return InlineKeyboardMarkup(YNBUTTONS)

async def handle_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    print("\n => query:")
    print(query)
    print()
    if query.data == 'n':
        resp = 'Ok. Sending the request...'
    elif query.data == 'y':
        resp = 'Please write a comment:'

    await query.edit_message_text(text=resp)




def main() -> None:
    print('starting...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('getcases', getcases_command))
    app.add_handler(CommandHandler('getprocesses', getprocesses_command))

    app.add_handler(CallbackQueryHandler(handle_inline))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)

    # checks every 3 seconds for new messages
    print('start polling\n')
    app.run_polling(poll_interval=3)

if __name__ == '__main__':
    main()

    """
    Notes
    https://docs.python-telegram-bot.org/en/stable/telegram.inlinekeyboardmarkup.html#inlinekeyboardmarkup
    https://github.com/unmonoqueteclea/calendar-telegram
    
    """