import unittest
import time

from heartbeat_timer import HeartbeatTimer

class TestHeartbeatTimer(unittest.TestCase):
    def setUp(self):
        self.timer = HeartbeatTimer()
    
    def test_increment(self):
        self.assertEqual(self.timer.count, 0)
        self.timer.increment()
        self.assertEqual(self.timer.count, 1)
    
    def test_refresh(self):
        self.timer.count = 2
        self.timer.refresh()
        self.assertEqual(self.timer.count, 0)
    
    def test_expired(self):
        self.assertFalse(self.timer.expired())
        self.timer.count = 3
        self.assertTrue(self.timer.expired())
        self.timer.count = 4
        self.assertTrue(self.timer.expired())
    
    def test_timer_resets_on_refresh(self):
        self.timer.count = 2
        self.assertFalse(self.timer.expired())
        self.timer.refresh()
        self.assertFalse(self.timer.expired())
    
    def test_timer_expiration(self):
        self.assertFalse(self.timer.expired())
        for i in range(3):
            self.timer.increment()
            time.sleep(1)
        self.assertTrue(self.timer.expired())

if __name__ == '__main__':
    unittest.main()
    