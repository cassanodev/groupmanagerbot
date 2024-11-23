"""
Utility Functions Module

This module provides various utility functions used throughout the bot including:
- Cryptographic operations (HMAC signatures)
- Payment transaction handling
- Email validation
- General helper functions

The utilities in this module support core bot functionality and external integrations.
"""

import aiohttp
import re
import hmac
import hashlib
import urllib.parse
from typing import Any

from config import Config

def generate_hmac_signature(raw_data) -> str:
    """
    Generate HMAC signature for data verification.

    Args:
        raw_data: The data to sign

    Returns:
        str: Hexadecimal representation of the HMAC signature
    """
    secret_bytes = Config["SECRET_KEY"].encode("utf-8")
    data_bytes = raw_data.encode("utf-8")
    signature = hmac.new(
        secret_bytes, 
        data_bytes, 
        hashlib.sha512
    ).hexdigest()
    return signature

async def create_transaction(buyer_name: str, buyer_email: str, currency: str) -> str:
    """
    Create a new payment transaction.

    This function interfaces with the payment provider's API to create
    a new transaction for subscription payment.

    Args:
        buyer_name (str): Name of the buyer
        buyer_email (str): Email of the buyer
        currency (str): Currency code for the transaction

    Returns:
        str: Transaction details if successful, None if failed
    """
    params: dict = {}
    params['version'] = "1"
    params['key'] = Config["PUBLIC_KEY"]
    params['cmd'] = "create_transaction"
    params['amount'] = Config["subscription_price"]
    params['currency1'] = "USD"
    params['currency2'] = currency
    params['buyer_name'] = buyer_name
    params['buyer_email'] = buyer_email

    encoded_params: str = urllib.parse.urlencode(params)
    hmac_sign: str = generate_hmac_signature(encoded_params)

    headers: dict = {
        'HMAC': hmac_sign,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://www.coinpayments.net/api.php", headers=headers, data=encoded_params) as response:
            if response.status == 200:
                data: Any = await response.json()
                if data['error'] == 'ok':
                    result: str = data['result']
                    return result
                
    return None

def is_email(email: str) -> bool:
    """
    Validate an email address using regex.

    Args:
        email (str): Email address to validate

    Returns:
        bool: True if email is valid, False otherwise
    """
    rgx = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
    return re.match(rgx, email) is not None
