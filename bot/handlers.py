from telebot.util import quick_markup
from typing import Dict, Any, Union
from utils.utils import create_transaction
from utils.user import GetUser, check_user
from classes.User import User as UserClass
from config import Config
from utils.utils import is_email
from database import MySQL
from classes.GroupManager import GroupManager as GM
from datetime import datetime, timezone
from telebot.asyncio_handler_backends import State, StatesGroup

class HandlersStates(StatesGroup):
    """
    State definitions for bot conversations.

    This class defines the various states that a user conversation can be in.
    It inherits from StatesGroup to provide state management functionality.

    States:
        RegisterEmail: State for email registration process
    """
    RegisterEmail = State()  # State for email registration process

def setup_handlers(bot):
    @bot.message_handler(commands='start', chat_types=['private'])
    async def start(message):
        user_id = message.chat.id
        User: UserClass = await GetUser(user_id)
        subscription_data = User.user_data.subscription_data
        exp_date = str(datetime.fromtimestamp(int(subscription_data['expiration_date']), tz=timezone.utc)) if subscription_data else None
        text: str = User.locales['start:onSubscription'].format(id=user_id, exp_date=exp_date.split()[0]) if subscription_data else User.locales['start:noSubscription'].format(id=user_id)
        buttons: Dict[str, Dict[str, str]] = {}

        if User.user_data.subscription_data:
            GroupManager = GM()
            buttons[User.locales['joinGroup']] = {'url': await GroupManager.CreateInviteLink(user_id)}
        else:
            buttons[User.locales['start:buyMembership']] = {'callback_data': 'buyMembership'}

        buttons[User.locales['start:support']] = {'callback_data': 'support'}

        markup: Any = quick_markup(buttons, row_width=1)
        
        await User.EditMessage(text, reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: call.data == "buyMembership")
    async def buy_membership(call):
        message: Any = call.message
        User: UserClass = await GetUser(message.chat.id)

        text: str = User.locales["membership:buying:giveMethods"]
        markup: Any = quick_markup({
            User.locales['membership:buying:buyWithCrypto']: {'callback_data': 'buyMembership:showCoins'},
            User.locales['back']: {'callback_data': 'start'}
        }, row_width=1)
        await User.EditMessage(text, reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: call.data == "buyMembership:showCoins")
    async def buy_membership_showCoins(call):
        message: Any = call.message
        User: UserClass = await GetUser(message.chat.id)

        text: str = User.locales["membership:buying:showCoins"]
        buttons: Dict[str, Dict[str, str]] = {
            **{
                f"{coin['name']} - {coin['network']}": {'callback_data': f"pay_membership:checkPoint {coin['coin_ref']}"}
                for coin in Config["coins"]
            },
            User.locales['back']: {'callback_data': 'buyMembership'}
        }
        markup: Any = quick_markup(buttons, row_width=1)

        await User.EditMessage(text, reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: call.data.startswith("pay_membership:checkPoint"))
    async def payCheckPoint(call, state):
        message: Any = call.message
        coin_ref = call.data.split()[1]
        User: UserClass = await GetUser(message.chat.id)

        if not User.user_data.email:
            await Ask_Email(message, state)
            return 
        
        await pay_membership_givePaymentInfo(message, coin_ref)


    async def pay_membership_givePaymentInfo(message, coin_ref):
        User: UserClass = await GetUser(message.chat.id)
        coin = next((coin for coin in Config["coins"] if coin["coin_ref"] == coin_ref), None)

        text = User.locales["error_getting_data"]
        markup: Any = quick_markup({
            User.locales['back']: {'callback_data': 'buyMembership:showCoins'}
        }, row_width=1)

        result = await create_transaction(User.user_data.fullname, User.user_data.email, coin_ref)
        if result:
            timeout = int(result["timeout"])
            hours = timeout // 3600
            minutes = (timeout % 3600) // 60
            seconds = (timeout % 3600) % 60
            text = User.locales["membership:givePaymentInfo"].format(
                amount = result["amount"],
                currency = f"{coin['name']} - {coin['network']}",
                address = result["address"],
                deadline=f"{hours:02}h:{minutes:02}m:{seconds:02}s",
                status_url = result["status_url"]
            )

            await User.SendPhoto(result["qrcode_url"], text, reply_markup=markup)
            return
        
        await User.EditMessage(text, reply_markup=markup)


    async def Ask_Email(message, state):
        User: UserClass = await GetUser(message.chat.id)
        text: str = User.locales["email:ask"]
        await state.set(HandlersStates.RegisterEmail)
        await User.SendMessage(text)
    

    @bot.message_handler(state=HandlersStates.RegisterEmail)
    async def RegisterEmail(message):
        User: UserClass = await GetUser(message.chat.id)
        text: str = message.text

        if not is_email(text):
            await User.SendMessage(User.locales["email:notValid"])
            return
        
        email_exists_in_db = await MySQL.GetUserByField("email", text)
        if email_exists_in_db:
            await User.SendMessage(User.locales["email:alreadyExists"])
            return
        
        await MySQL.UpdateFieldForUser(message.chat.id, "email", text)
        await User.SendMessage(User.locales["email:successfullyLinked"])

    @bot.callback_query_handler(func=lambda call: call.data.startswith("support"))
    async def support(call):
        await bot.send_message(call.message.chat.id, "Coming soon...")


    @bot.message_handler(state="*", commands=["cancel"])
    async def clean_state(message, state):
        await state.delete()


    @bot.callback_query_handler(func=lambda call: True)
    async def handle_callback_query(call):
        try:
            funcs = {
                'start': start
            }
            message = call.message
            await funcs[call.data](message)
        except:
            pass


    @bot.chat_member_handler()
    async def chat_member_handler(update):
        user_id = update.from_user.id
        await check_user(update)