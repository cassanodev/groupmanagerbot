"""
API Module

This module implements FastAPI endpoints for handling external integrations, primarily:
- Payment processing webhooks
- Subscription management
- User notifications

The API provides secure endpoints with HMAC signature verification for payment processing
and subscription management.
"""

from fastapi import FastAPI, Header, Request, HTTPException
from typing import Optional
from config import Config
from database import MySQL
from datetime import datetime, timedelta
import hmac 
import hashlib
from utils.user import GetUser
from telebot.util import quick_markup
from classes.GroupManager import GroupManager as GM

app = FastAPI()

@app.post("/payment_handler")
async def ipn_handler(
    request: Request,
    HMAC: Optional[str] = Header(None)
):
    """
    Payment notification handler endpoint.

    This endpoint processes Instant Payment Notifications (IPN) from the payment provider.
    It verifies the payment signature, updates user subscription status, and sends
    notifications to users.

    Args:
        request (Request): The incoming webhook request
        HMAC (str, optional): HMAC signature for request verification

    Returns:
        dict: Status response

    Raises:
        HTTPException: If HMAC header is missing or invalid
    """
    if not HMAC:
        raise HTTPException(status_code=400, detail="Missing HMAC header")
    
    raw_body = await request.body()
    
    # Verify HMAC signature
    computed_hmac = hmac.new(
        Config["SECRET_KEY"].encode(),
        raw_body,
        hashlib.sha512
    ).hexdigest()

    if HMAC != computed_hmac:
        raise HTTPException(status_code=403, detail="Invalid HMAC signature")

    # Process payment notification
    form_data = await request.form()
    ipn_data = {key: value for key, value in form_data.items()}

    status = int(ipn_data.get("status", 0))
    buyer_email = ipn_data.get("email")

    # Handle successful payment
    if status >= 100:
        GroupManager = GM()
        user_data = await MySQL.GetUserByField("email", buyer_email)
        User = await GetUser(user_data.user_id)

        # Calculate subscription expiration
        current_date = datetime.now()
        expiration_date = current_date + timedelta(days=Config["subscription_days"])

        # Update user subscription data
        await MySQL.UpdateFieldForUser(user_data.user_id, "subscription_data", {
            'expiration_date': expiration_date.timestamp()
        })

        # Generate group invite link and send to user
        invite_link = await GroupManager.CreateInviteLink(user_data.user_id)
        markup = quick_markup({
            User.locales['joinGroup']: {'url': invite_link},
        }, row_width=1)

        # Send confirmation message to user
        await User.SendMessage(
            User.locales['subscription:started'].format(days=Config["subscription_days"]),
            reply_markup=markup,
            protect_content=True
        )

    return {"status": "ok"}
