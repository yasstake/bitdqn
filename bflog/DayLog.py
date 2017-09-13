import numpy as np
import json
import datetime
from scipy.sparse import lil_matrix

class Board:
    def __init__(self):
        pass


class DayLog:
    def __init__(self):
        self.bid_snapshot = {}
        self.ask_snapshot = {}
        self.mid_price_snapshot = 0
        size = (24*60*60, 1000000)
        self.bid_board = lil_matrix(size)
        self.ask_board = lil_matrix(size)
        self.ask = lil_matrix(size)
        self.bid = lil_matrix(size)
        self.buy = lil_matrix(size)
        self.sell = lil_matrix(size)
        self.mid_price  = lil_matrix((24*60*60, 1))
        self.last_sec = -1

        pass

    def loadfile(self, file):
        with open(file) as f:
            for line in f:
                key = line[0]
                time_s = line[2:21]
                time = datetime.datetime.strptime(time_s, '%Y-%m-%d %H:%M:%S')

                board = line[21:]
                b2 = board.replace("\'", '\"').replace('u', '')
                js = json.loads(b2)

                self.loadline(key, time, js)

    def loadline(self, key, time, js):
        sec = self.time2sec(time)

        if(key == 'D'):
            self.loadDelta(sec, js)
        elif(key == 'S'):
            self.loadSnapShot(sec, js)
        elif(key == 'E'):
            self.loadExec(sec, js)

    def replace_snapshot(self, side, snapshot, price, size):

        pass


    def copy_snapshot(self, sec):
        for key in self.bid_snapshot:
            self.bid_board[self.last_sec, key] = self.bid_snapshot[key]

        for key in self.ask_snapshot:
            self.ask_board[self.last_sec, key] = self.ask_snapshot[key]

        self.mid_price[sec] = self.mid_price_snapshot
        self.last_sec = sec

    def loadDelta(self, sec, js):
        if(self.last_sec == -1):
            self.last_sec = sec
        elif (self.last_sec +1 == sec):
            self.copy_snapshot(self.last_sec)
        elif(self.last_sec +2 == sec):
            self.copy_snapshot(self.last_sec)
            self.copy_snapshot(self.last_sec + 1)
        elif(self.last_sec +3 == sec):
            self.copy_snapshot(self.last_sec)
            self.copy_snapshot(self.last_sec + 1)
            self.copy_snapshot(self.last_sec + 2)
        elif(self.last_sec != sec):
            print(sec)
            pass


        mid_price = js['mid_price']
        self.mid_price_snapshot = mid_price

        for b in js['bids']:
            price = b['price']
            size =  b['size']
            self.bid_snapshot[price] = size

        for b in js['asks']:
            price = b['price']
            size =  b['size']
            self.ask_snapshot[price] = size


    def loadSnapShot(self, sec, js):
        self.last_sec = sec
        self.bid_snapshot = {}
        self.ask_snapshot= {}

        mid_price = js['mid_price']
        self.mid_price[sec] = mid_price
        self.mid_price_snapshot = mid_price

        for b in js['bids']:
            price = b['price']
            size =  b['size']
            self.bid_snapshot[price] = size

        for b in js['asks']:
            price = b['price']
            size =  b['size']
            self.ask_snapshot[price] = size


    def loadExec(self, sec, js):
        for e in js:
            price = e['price']
            side = e['side']
            size = e['size']
            if(side == 'BUY'):
                self.buy[sec, price] += size
                pass
            elif(side == 'SELL'):
                self.sell[sec, price] += size
                pass
            else:
                pass

    def time2sec(self, time):
        t = time.hour * 3600 + time.minute * 60 + time.second
        return t



