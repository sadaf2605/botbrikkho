#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BotBrikkhoIntel(object):
    def find_a_reply(self, text):
        return False, text



from wit import Wit
class WitIntel(BotBrikkhoIntel):

    def __init__(self):
        access_token = "W6WRVRJQV4AL5PH3VA4ZU7O3EATUXOZF"
        actions = {
            #'send_news_cat': send_news_cat
        }

        self.wit_intel = Wit(access_token=access_token, actions=actions)


    def find_a_reply(self, session, text):

        def param_tuple(dic):
            params={}
            for d,v in dic.items():
                params[d]=v[0]["value"]

            return params




        self.wit_intel.message(text)

        resp = {}
        while True:
            resp = self.wit_intel.converse(session, text, {})
            if resp.get("type") != "stop":
                break

        #print(str(text))
        print(str(resp))

        if resp.get("type")=="msg":
            return True, False, resp.get("msg")
        elif resp.get("type")=="action":
            return True, resp.get("action"), param_tuple(resp.get("entities"))
        else:
            return False, False, text
