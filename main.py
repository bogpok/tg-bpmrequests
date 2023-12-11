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

# Those are personal values. Replace it
from mysecrets.pztg.passcodes import (
    TOKEN, BOT_USERNAME,
    baseURL,
    clientid,
    clientsecret)
# sys.path.append('D:/GitHub/pyzagi/src')
from pyzagi import (
    ConnectionBPM,
    Process
)

import re

def use_regex(input_text):
    pattern = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", re.IGNORECASE)
    return pattern.match(input_text)

kbuttons = [
    [KeyboardButton("🎇 Create request")],
    [KeyboardButton("🍰 Create cake")],
]
YNBUTTONS = [
    [InlineKeyboardButton('Yes', callback_data="y"), 
     InlineKeyboardButton('No', callback_data="n")]
]

def create_YNIK():
    """Create Yes/No Inline Keyboard"""
    return InlineKeyboardMarkup(YNBUTTONS)


STARTDATE, ENDDATE, PRECOMMENTARY, COMMENTARY, DATEVALID = range(5)
ALLSTATES = [STARTDATE, ENDDATE, PRECOMMENTARY, COMMENTARY, DATEVALID]


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    await update.message.reply_text("Yo! Let's start!",
                                    reply_markup = ReplyKeyboardMarkup(kbuttons))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Available commands:"
    message+="\n/help"    
    message+="\n/start"
    message+="\n/getcases"    
    message+="\n/create_request"
    await update.message.reply_text(message)

async def getcases_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('cases!')

async def getprocesses_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # text = pz.getprocesses(pz.headers)
    text='empty///'
    await update.message.reply_text(text)

# Responses
class CaseCreationWrapper:
    CASECREATIONRID = 'CASECREATION'
    messages = {
        'WELCOME':"You are going to create a request in the BPM system.",
        'LOST':"Seems you kinda lost. Please initiate request creation again."
    }
    async def lost_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text(CaseCreationWrapper.messages['LOST'])
        return ConversationHandler.END


    class SimpleRequest:
        def __init__(self):
            self.startdate = ''
            self.enddate = ''
            self.commentary = 'No comments'      

            bizagibpm = ConnectionBPM(
                baseURL,
                clientid,
                clientsecret
            )
            self.simpleRequest = Process(
            processid = 'a88c3aab-a94b-49c5-b83b-5b845d721d86',
            connection = bizagibpm,
            startstructure = [
                "Simplerequest.Requestdata.Startdate",
                "Simplerequest.Requestdata.Enddate",
                "Simplerequest.Requestdata.Commentary",
            ]) 
                
            self.currstate = STARTDATE

        async def _sendrequest(self, update: Update):
            self._printdetails()
            resp = self.details + "\nSending the request..."
            await update.message.reply_text(resp)
            self.simpleRequest.start([
                self.startdate,
                self.enddate,
                self.commentary
            ])  

            
        async def start(self, update: Update):
            await update.message.reply_text(CaseCreationWrapper.messages['WELCOME'])
            await update.message.reply_text("Please select a start date: ")
        # async def date_validation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        #     print("date_validation")
        #     self.startdate = update.message.text
        #     if use_regex(update.message.text):
                
        #         return ALLSTATES[self.currstate+1]
        #     else:
        #         await update.message.reply_text("The date should be in the following format: yyyy-mm-dd\nTry again:")
        #         return self.currstate
            
        # async def handle_startdate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:          
        #     print("...start date")  

        #     self.startdate = update.message.text           
            
        #     return DATEVALID
        
        # async def handle_enddate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        #     print("...end date")  
        #     await update.message.reply_text("Please select an end date: ")
        #     self.currstate = ENDDATE           
        #     self.enddate = update.message.text
        #     return DATEVALID
        #     await update.message.reply_text("Do you want to provide a commentary?",
        #                                 reply_markup=create_YNIK())

        async def handle_startdate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            print("...start date")
            startdate = update.message.text
            
            if use_regex(startdate):
                request_obj.startdate = startdate
                await update.message.reply_text("Please select an end date:")
                return ENDDATE
            else:
                await update.message.reply_text("The date should be in the following format: yyyy-mm-dd. Try again:")
                return STARTDATE

        async def handle_enddate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            print("...end date")
            enddate = update.message.text
            
            if use_regex(enddate):
                request_obj.enddate = enddate
                await update.message.reply_text("Do you want to provide a commentary?", reply_markup=create_YNIK())
                return PRECOMMENTARY
            else:
                await update.message.reply_text("The date should be in the following format: yyyy-mm-dd. Try again:")
                return ENDDATE

        async def date_validation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            print("date_validation")
            return DATEVALID
        
        
        async def handle_precommentary(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            print("...precommentary") 
            self.currstate = PRECOMMENTARY
            query = update.callback_query
            await query.answer()   
            if query.data == 'n':
                resp = 'You dont want to provide any comments.'
                await query.edit_message_text(text=resp)
                await self._sendrequest(update)
                return ConversationHandler.END
        
            elif query.data == 'y':
                resp = 'Please write a comment:'  
                await query.edit_message_text(text=resp)                
                return COMMENTARY
            
        async def handle_commentary(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            print("...commentary") 
            self.currstate = COMMENTARY
            self.commentary = update.message.text
            
            await self._sendrequest(update)
            return ConversationHandler.END
            

            
        def _formdetails(self):
            self.details = "Request details:\n"
            self.details += str(self.startdate) + "\n"
            self.details += str(self.enddate) + "\n"
            self.details += str(self.commentary) + "\n"

        def _printdetails(self):
            print()
            self._formdetails()            
            print(self.details)
        
        


def handle_resp(text: str)->str:
    processed: str = text.lower()
    if 'beez' in processed:
        return 'BEEEEEEEZZ'
    elif 'create' in processed:
        """ if 'request' in processed:            
            return CaseCreationWrapper.CASECREATIONRID """
        if 'cake' in processed:
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
    await update.message.reply_text(response)
    """ if response == CaseCreationWrapper.CASECREATIONRID:
        await handle_createrequest(update)
    else:
         """

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')






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

global request_obj
request_obj = CaseCreationWrapper.SimpleRequest()

async def start_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await request_obj.start(update)
    return STARTDATE
    


def main() -> None:
    print('\n=========================\nstarting...')
    app = Application.builder().token(TOKEN).build()

    # Commands    
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    """     
    app.add_handler(CommandHandler('getcases', getcases_command))
    app.add_handler(CommandHandler('getprocesses', getprocesses_command))

    app.add_handler(CallbackQueryHandler(handle_inline))
    """
    # Messages
    # app.add_handler(MessageHandler(filters.TEXT, handle_message)) 

    createRequest_ch = ConversationHandler(
        entry_points=[CommandHandler("create_request", start_request)],
        states={
            STARTDATE: [MessageHandler(filters.TEXT, request_obj.handle_startdate)],
            ENDDATE: [MessageHandler(filters.TEXT, request_obj.handle_enddate)],
            PRECOMMENTARY: [CallbackQueryHandler(request_obj.handle_precommentary)],
            COMMENTARY: [MessageHandler(filters.TEXT, request_obj.handle_commentary)],
            DATEVALID: [MessageHandler(filters.TEXT, request_obj.date_validation)]
        },
        fallbacks=[CommandHandler("lost", CaseCreationWrapper.lost_end)],
    )
    """ START_ROUTES: [
                CallbackQueryHandler(one, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(two, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(three, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(four, pattern="^" + str(FOUR) + "$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
            ], """
    # ConversationHandler
    app.add_handler(createRequest_ch)
    
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