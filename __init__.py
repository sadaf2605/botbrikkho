#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import json

import requests

from flask import Blueprint, request

bot_app = Blueprint("BOT APP",__name__)





@bot_app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            print os.environ["VERIFY_TOKEN"]
            print request.args.get("hub.verify_token") 
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


from conversation_handler import ConversationHandler


conversation_handler = ConversationHandler()


from news_api import NewsAPI
from flask import request


@bot_app.route('/users/send', methods=['GET'])
def send_all_user():
    global conversation_handler
    msg = request.args.get("msg")
    print msg
    users = NewsAPI.all_users()
    for u in users:
        conversation_handler.conversation.send_plain_message(u, msg)
    
    return "done",200

def setConversationHandler(ch):
    global conversation_handler
    conversation_handler= ch()

@bot_app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()

    #    log("this is webhook POST request from facebook")
    #    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    log(data)

    print(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message


                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    

                    message = messaging_event["message"]

                    conversation_handler.on_message(sender_id, message)


                    if message.get("text"):
                        text = messaging_event["message"]["text"]
                        conversation_handler.on_text(sender_id,text)

                    if message.get("quick_reply"):

                        quick_reply = messaging_event["message"]["quick_reply"]
                        conversation_handler.on_quick_reply(sender_id, quick_reply)

                        if quick_reply.get("payload"):
                            payload = quick_reply["payload"]
                            conversation_handler.on_payload(sender_id, payload)
                    
                    if message.get("attachments"):
                        attachments = message["attachments"]
                        conversation_handler.on_attachments(sender_id, attachments)

                        for attachment in attachments:
                            if attachment["type"] == "video":
                                conversation_handler.on_video(sender_id, attachment["payload"]["url"] )

                if messaging_event.get("postback"):
                    sender_id = messaging_event["sender"]["id"]

                    postback = messaging_event["postback"]
                    conversation_handler.on_postback(sender_id, postback)
                    if postback.get("payload"):
                        payload = postback["payload"]
                        conversation_handler.on_payload(sender_id, payload)


                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

    return "ok", 200








def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()



