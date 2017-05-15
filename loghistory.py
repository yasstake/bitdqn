from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from datetime import datetime

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-52a9ab50-291b-11e5-baaa-0619f8945a4f'


class MySubscribeCallback(SubscribeCallback):
    def writeMessage(self, Key, message):
        with open(datetime.now().date().strftime("%Y-%m-%d") + ".log", "a") as file:
            line = Key + " " + "{0:%Y-%m-%d %H:%M:%S}".format(datetime.now()+ " ") + str(message) + "\n";
            file.write(line);

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
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

    def message(self, pubnub, message):
        pass;


class SnapShotListener(MySubscribeCallback):
    def message(self, pubnumb, message):
        self.writeMessage("S", message.message);
        pass;


pubnub = PubNub(pnconfig)
pubnub.add_listener(SnapShotListener());
pubnub.subscribe().channels('lightning_board_snapshot_BTC_JPY').execute();


class BoardDiffListener(MySubscribeCallback):
    def message(self, pubnumb, message):
        self.writeMessage("D", message.message);
        pass

pubnub2 = PubNub(pnconfig);
pubnub2.add_listener(BoardDiffListener());
pubnub2.subscribe().channels('lightning_board_BTC_JPY').execute();


class ExecutionListener(MySubscribeCallback):
    def message(self, pubnumb, message):
        self.writeMessage("E", message.message);
        pass;


pubnub3 = PubNub(pnconfig);
pubnub3.add_listener(ExecutionListener());
pubnub3.subscribe().channels('lightning_executions_BTC_JPY').execute();

