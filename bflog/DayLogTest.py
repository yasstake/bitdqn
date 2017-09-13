import unittest
import DayLog
import datetime
from scipy.sparse import lil_matrix
import json

class MyTestCase(unittest.TestCase):
    def test_Init(self):
        log = DayLog.DayLog()

    def test_LoadFile(self):
        log = DayLog.DayLog()

        log.loadfile('2017-05-30.log')

    # {'mid_price': 271162.0, 'bids': [{'price': 262199.0, 'size': 0.0}], 'asks': []}
    def _test_replace_snapshot(self):
        snapshot = json.loads('{"mid_price": 271162.0, "bids": [{"price": 262199.0, "size": 0.0}], "asks": [{"price": 262199.0, "size": 0.0}]}')
        replace = json.loads('{"price": 262199.0, "size": 0.0}')

        log = DayLog.DayLog()
        log.replace_snapshot(snapshot, 'bids', 262199, 10)
        pass

    def test_ParseMatrix(self):
        matrix = lil_matrix((10, 10))
        print(matrix)
        matrix[1, 0] = 1


    def test_Datetime(self):
        log = DayLog.DayLog()

        time = datetime.datetime(2017, 9, 6, 10, 11, 12)

        sec = log.time2sec(time)
        self.assertEqual(sec, 10*3600 + 11 * 60 + 12)

    def test_LoadE(self):
        '''
E Wed May 17 23:17:03 2017E 2017-05-17 23:17:07
[{u'price': 221578.0, u'exec_date': u'2017-05-17T14:17:03.9641085Z', u'side': u'SELL', u'id': 24559921, u'sell_child_order_acceptance_id': u'JRF20170517-141657-489508', u'buy_child_order_acceptance_id': u'JRF20170517-141655-326784', u'size': 0.00177828}]                
        '''

if __name__ == '__main__':
    unittest.main()
