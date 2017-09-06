#!/usr/bin/python3

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from datetime import datetime

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-52a9ab50-291b-11e5-baaa-0619f8945a4f'

path='/bflog/FX-'

C_FX_SNAPSHOT = 'lightning_board_snapshot_FX_BTC_JPY'
C_FX_BOARD    = 'lightning_board_FX_BTC_JPY'
C_FX_EXECUTE  = 'lightning_executions_FX_BTC_JPY'

class LogListener(SubscribeCallback):
    def writeMessage(self, Key, message):
        with open(path + datetime.now().date().strftime("%Y-%m-%d") + ".log", "a") as file:
            line = Key + " " + "{0:%Y-%m-%d %H:%M:%S}".format(datetime.now()) + " "+ str(message) + "\n";
            file.write(line);

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pubnub.reconnect()
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            pass
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
        elif status.category == PNStatusCategory.PNTimeoutCategory:
            # do some magic and call reconnect when ready
            pubnub.reconnect()


    def message(self, pubnumb, message):
        if message.channel == C_FX_SNAPSHOT:
            type = 'S'
        elif message.channel == C_FX_BOARD:
            type = 'D'
        elif message.channel == C_FX_EXECUTE:
            type = 'E'
            pass

        self.writeMessage(type, message.message);
        pass;

pubnub = PubNub(pnconfig)
pubnub.add_listener(LogListener());
pubnub.subscribe().channels([C_FX_SNAPSHOT, C_FX_BOARD, C_FX_EXECUTE]).execute();


