import redis
r = redis.Redis('128.199.186.42')

from conversation import Conversation
from wit_integration import WitIntel


class ConversationHandler(object):
    def __init__(self):
        self.conversation = Conversation()
        self.wit_intel = WitIntel()

    def setConversation(self, conv):
        self.conversation = conv


    def on_text(self,sender_id, text):

        found_reply, func_callable, reply = self.wit_intel.find_a_reply(sender_id, text)

        if found_reply:
            self.conversation.send_plain_message(sender_id, reply)

        if func_callable:
            print reply
            try:
                eval("self.conversation."+str(func_callable)+str("( sender_id, **reply)"))
            except Exception as e:
                print e

        #if self.expecting_input(sender_id):
        #    self.process(sender_id, process_with(sender_id), text)



    def on_message(self,sender_id, message):
        pass

    def on_attachments(self, sender_id, attachment):
        pass
    
    def on_video(self, sender_id, video_url):
        pass

    def on_quick_reply(self,sender_id, quick_reply):
        pass

    def on_payload(self,sender_id, payload):
        p_m = payload.replace(" ","").split(",")
        func = p_m[0]
        params = p_m[1:]



        try:
            eval("self.conversation." + func + "(sender_id, *params)")
        except SyntaxError as e:
            print e

            print "Syntax error while processing payload",payload,"func",func,"params", params


        #if conv["processor"]["process_with"] and not conv["processor"]["expecting_input"]:
        #    print conv["processor"]["process_with"]
        #    print "args", args
        #    eval("self.conversation."+conv["processor"]["process_with"]+"(sender_id, *args)")

    def on_postback(self, sender_id, postback):
        #self.on_payload(sender_id,postback["payload"])
        pass






    def expecting_input(self, sender_id):
        return r.hget(sender_id, "expecting_input")

    def process_with(sender_id):
        return r.hget(sender_id, "process_with")

    def prcess(sender_id, process_with, args=""):
        eval("" + process_with +"(sender_id,"+ args+")")


    def add_user_processor(self, process_with, expecting_input ):

        r.hset(sender_id, 'expecting_input',expecting_input)
        r.hset(sender_id, 'process_with',process_with)