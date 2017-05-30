import os
import json
import requests

class Conversation(object):
    convs=[]
##        {
#            "reply_option": {
#                "view": {
#                    "template": "quick_reply|generic|",
#                    "def_action": default_action,
#                    "buttons":[
#                        button_json(url="")
#                    ]
#                },
#                "prcessor": processor(LeadneConversation.func, True),
#            }
#            ,
#            "quick_reply": [
#                quick_reply_json(title="national"),
#                quick_reply_json(title="international"),
#            ],
#            "prcessor": processor(LeadneConversation.func, True),
#            "reply_type": {}
#        },
#
#    ]

    def __init__(self):
        self.access_token = os.environ["PAGE_ACCESS_TOKEN"]

    def get_user_name(self, user_id):
        params = {
            "access_token": self.access_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            'fields' : 'first_name,last_name'
        })
        r = requests.get("https://graph.facebook.com/v2.6/"+user_id, params=params, headers=headers, data=data)



        
        return r.json().get("first_name",""), r.json().get("last_name","")


    def get(self, id):

        return self.convs[int(id)]

    def get_bot_conv(self,id):
        return get(id)["text"]["bot"]


    def processor(self, func, input=False):
        doc={}
        doc["process_with"] = func.__name__
        doc["wait_for_input"] = input

        return doc

    def quick_reply_json(self, type="text", title=None, payload=None):
        doc = {}

        doc["content_type"] = type
        if title: doc["title"] = title
        if payload: doc["payload"] = payload

        return payload

    def send_message(self, recipient_id, message):

        # log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

        params = {
            "access_token": self.access_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": message
        })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            log("this is non 200 status from facebook")
            log(r.status_code)
            log(r.text)

    def send_plain_message(self, sender_id, message_text):
        message = {
            "text": message_text
        }

        self.send_message(sender_id, message)


def log(t):
    print t