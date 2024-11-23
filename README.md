# Group Manager Bot

A basic Telegram bot built with Python that manages group memberships, handles subscriptions, and provides multi-language support. The bot automates group access control through a subscription-based system with cryptocurrency payment integration.

## Features

- **Subscription Management**
  - Automated subscription handling
  - Configurable subscription durations
  - Cryptocurrency payment integration via CoinPayments
  - Automatic membership expiration checks

- **Group Access Control**
  - Automatic member removal on subscription expiration
  - Single-use invite link generation
  - Admin privilege management
  - Member status verification

- **Multi-language Support**
  - Supports 14 languages out of the box
  - Easy to add new language translations
  - Language files in JSON format
  - Automatic language detection

- **Admin Features**
  - Add/modify user subscriptions
  - Monitor group membership
  - Manage user access
  - View subscription status

- **Payment System**
  - Multiple cryptocurrency support
  - Secure payment verification
  - Automated transaction handling
  - Payment status notifications

## Tech Stack

- Python 3.x
- FastAPI for API endpoints
- SQLAlchemy for database management
- Telebot for Telegram integration
- MySQL for data storage
- CoinPayments for crypto transactions

## Requirements

```
aiohappyeyeballs==2.4.3
aiohttp==3.11.2
aiomysql==0.2.0
fastapi==0.115.5
PyMySQL==1.1.1
pyTelegramBotAPI==4.24.0
python-dotenv==1.0.1
SQLAlchemy==2.0.36
telebot==0.0.5
uvicorn==0.32.0
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/groupmanagerbot.git
cd groupmanagerbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the bot:
   - Copy `config.py` and set your configuration:
     - `BOT_TOKEN`: Your Telegram bot token from @BotFather
     - `GROUP_CHAT_ID`: Your group's chat ID
     - `DB_CONNECTION_STRING`: MySQL database connection string
     - `PUBLIC_KEY` and `SECRET_KEY`: Your CoinPayments API keys
     - Other settings like subscription duration and pricing

4. Set up the database:
   - Create a MySQL database
   - The tables will be automatically created on first run

5. Run the FastAPI Server:
```bash
uvicorn api.api:app --reload
```

6. Run the bot:
```bash
python main.py
```

## Project Structure

```
├── api/
│   └── api.py                # FastAPI endpoints for payment processing
├── bot/
│   ├── admin.py             # Admin command handlers
│   ├── handlers.py          # Main bot command handlers
│   ├── instance.py          # Bot initialization
│   ├── members_checker.py   # Subscription verification
│   └── middlewares.py       # Request processing middleware
├── classes/
│   ├── GroupManager.py      # Group management functionality
│   └── User.py             # User management functionality
├── database/
│   ├── main.py             # Database initialization
│   ├── models.py           # SQLAlchemy models
│   └── MySQL.py            # Database operations
├── locales/                # Language translation files
├── utils/
│   ├── logger.py           # Logging configuration
│   ├── user.py            # User utility functions
│   └── utils.py           # General utilities
├── config.py               # Bot configuration
├── main.py                # Application entry point
└── requirements.txt       # Project dependencies
```

## Configuration

The `config.py` file contains all necessary settings:

```python
Config = {
    "BOT_TOKEN": "",                # Telegram Bot Token
    "GROUP_CHAT_ID": "",            # Group Chat ID
    "DB_CONNECTION_STRING": "",     # Database Connection String
    "PUBLIC_KEY": "",               # CoinPayments Public Key
    "SECRET_KEY": "",               # CoinPayments Secret Key
    "DEFAULT_LANGUAGE": "en",       # Default Bot Language
    "subscription_days": 7,         # Subscription Duration
    "subscription_price": 20,       # Subscription Price
    "coins": [                      # Supported Cryptocurrencies
        {"name": "BTC", "network": "BITCOIN", "coin_ref": "BTC"},
        {"name": "ETH", "network": "ERC20", "coin_ref": "ETH"},
        # ... etc
    ]
}
```

## Security

- All payment processing is handled securely through CoinPayments
- HMAC signature verification for payment webhooks
- Single-use invite links for group access
- Automatic member verification and removal

## Support

I do NOT provide support for this project. If you need help, please refer to the official Telegram Bot documentation.