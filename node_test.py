import unittest

from node import Node

class TestNode(unittest.TestCase):
    
    def test_init(self):
        node = Node(id=1, ip_addr='127.0.0.1', port=5000, alive=True)
        self.assertEqual(node.id, 1)
        self.assertEqual(node.ip_addr, '127.0.0.1')
        self.assertEqual(node.port, 5000)
        self.assertTrue(node.get_alive())
        self.assertFalse(node.get_new_leader_flag())
        
    def test_set_id(self):
        node = Node(id=1, ip_addr='127.0.0.1', port=5000, alive=True)
        node.set_id(2)
        self.assertEqual(node.id, 2)
        
    def test_set_ip_addr(self):
        node = Node(id=1, ip_addr='127.0.0.1', port=5000, alive=True)
        node.set_ip_addr('192.168.0.1')
        self.assertEqual(node.ip_addr, '192.168.0.1')
        
    def test_set_port(self):
        node = Node(id=1, ip_addr='127.0.0.1', port=5000, alive=True)
        node.set_port(8080)
        self.assertEqual(node.port, 8080)
        
    def test_set_leader_flag(self):
        node = Node(id=1, ip_addr='127.0.0.1', port=5000, alive=True)
        node.set_leader_flag(True)
        self.assertTrue(node.get_new_leader_flag())
        
    def test_set_alive(self):
        node = Node(id=1, ip_addr='127.0.0.1', port=5000, alive=False)
        node.set_alive(True)
        self.assertTrue(node.get_alive())

if __name__ == '__main__':
    unittest.main()