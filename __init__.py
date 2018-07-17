from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler
from IOTBit_library_auto import Modem
import math


class CheckSignal(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.sigstr = "None"        # Human value
        
    @intent_file_handler('signal.check.intent')
    def handle_signal_check(self, message):
        # Set up modem, request signal value
        APN = 'everywhere'          # YOUR APN HERE
        _4G = Modem(APN,'4G')
        _4G.sendATcmd('AT+CSQ',1000)

        # Set numeric value - sometimes one digit.
        if _4G.response[9].isdigit():
            self.sig = int(_4G.response[8:9])
        else:
            self.sig = int(_4G.response[8])
        # Get human-friendly value
        if self.sig > 98:
            self.sigstr = "none."
        elif self.sig < 2:
            self.sigstr = "Error: 0."
        elif self.sig < 10:
            self.sigstr = "marginal."
        elif self.sig < 15:
            self.sigstr = "OK."
        elif self.sig < 20:
            self.sigstr = "good."
        elif self.sig > 19:
            self.sigstr = "excellent."
        else:
            self.sigstr = "Error: 1."
            
        self.speak_dialog('signal.check', data={"sigstr": self.sigstr})


def create_skill():
    return CheckSignal()


