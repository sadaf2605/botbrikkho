class Element:
    def __init__(self, title, subtitle, payload, image_url,action,url, buttons=[] ):
        self.title= title
        self.subtitle= subtitle
        self.payload= payload
        self.image_url = image_url
        self.action = action
        self.buttons = buttons
        self.url = url


    def __json__(self):
        buttons_json=[]
        for b in self.buttons:
            buttons_json.append(b.__json__())


        return {
                    "title": self.title,
                    "image_url": self.image_url,
                    "subtitle": self.subtitle,
                    "default_action": {
                        "type": "web_url",
                        "url": self.url,
                        "messenger_extensions": True,
                        "webview_height_ratio": "tall",
                        "fallback_url": self.url
                    },
                    "buttons": buttons_json
                }


class QuickReply:
    def __init__(self, title, payload, image_url=None ):
        self.title = title
        self.payload = payload
        if image_url: self.image_url = image_url

    def __json__(self):
        return {
            "content_type": "text",
            "title": self.title,
            "payload": self.payload
        }

class QuickReplies:
    def __init__(self,text, quick_replies=[]):
        self.text = text
        self.quick_replies= quick_replies

    def __json__(self):
        qrs_json=[]
        for qr in self.quick_replies:
            qrs_json.append(qr.__json__())

        return {
            "text": self.text,
            "quick_replies": qrs_json
          }

class Button:
    def __init__(self, title,type, payload):
        self.title = title
        self.type = type
        self.payload = payload

    def __json__(self):
        return {
                   "type": self.type,
                    "payload": self.payload,
                    "title": self.title
                }

class Custom:
    def __init__(self,dic):
        self.dic = dic

    def __json__(self):
        return self.dic

class Template:
    def __init__(self, type, elements=[],):
        self.type= type
        self.elements = elements

    def __json__(self):
        elements_json= []

        for e in self.elements:
            elements_json.append(e.__json__())
        return {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": self.type,
                    "elements": elements_json
                }
            }
        }
