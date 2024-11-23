Config = {}

# ======================================

Config["BOT_TOKEN"] = ''                # The token obtained from the @BotFather on Telegram.
Config["GROUP_CHAT_ID"] = ''            # The ID of the group chat where the bot will be active.

# The connection string for the database.
# Format: 'mysql+aiomysql://username:password@host:port/database-name'
Config["DB_CONNECTION_STRING"] = 'mysql+aiomysql://root:@localhost:3306/database-name'

# The coinpayments public and secret key used for encryption.
Config["PUBLIC_KEY"] = ''
Config["SECRET_KEY"] = ''

Config["DEFAULT_LANGUAGE"] = 'en' # The default language of the bot.

# Subscription Settings
Config["subscription_days"] = 7  # The number of days of the subscription.
Config["subscription_price"] = 20  # The price of the subscription.

# Supported Coins
# ---------------
# The list of supported coins for payment.
# Refer to https://www.coinpayments.net/supported-coins-all to see supported coins
# Also note that you must enable these coins in your CoinPayments account
# Each coin is represented by a dictionary with the following keys:
# - name: The name of the coin.
# - network: The network used by the coin.
# - coin_ref: The reference used by the coin.
Config["coins"] = [
    {"name": "BTC", "network": "BITCOIN", "coin_ref": "BTC", },
    {"name": "ETH", "network": "ERC20", "coin_ref": "ETH", },
    {"name": "SOL", "network": "SOL", "coin_ref": "SOL", },
    {"name": "BNB", "network": "BSC", "coin_ref": "BNB.BSC", },
    {"name": "USDT", "network": "TRC20", "coin_ref": "USDT.TRC20", },
    {"name": "USDC", "network": "TRC20", "coin_ref": "USDC.TRC20", },
    {"name": "TRX", "network": "TRC20", "coin_ref": "TRX", }
]


# DON'T TOUCH UNLESS YOU KNOW WHAT YOU'RE DOING
# ==============================================

# The storage used by the bot to store its state.
# In production, switch to redis for better performance.
from telebot.asyncio_storage import StateMemoryStorage
state_storage = StateMemoryStorage()

# Bot Instance
# ------------
# The instance of the bot.
from telebot.async_telebot import AsyncTeleBot
bot = AsyncTeleBot(Config["BOT_TOKEN"], state_storage=state_storage)