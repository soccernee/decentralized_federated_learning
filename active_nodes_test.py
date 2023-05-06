import unittest
from active_nodes import ActiveNodes

class TestActiveNodes(unittest.TestCase):
    def setUp(self):
        self.active_nodes = ActiveNodes()
    
    def test_get_node(self):
        self.assertIsNone(self.active_nodes.get_node(1))
        self.active_nodes.add_node(1, "node1")
        self.assertEqual(self.active_nodes.get_node(1), "node1")
    
    def test_get_version(self):
        self.assertEqual(self.active_nodes.get_version(), 1)
    
    def test_set_version(self):
        self.active_nodes.set_version(2)
        self.assertEqual(self.active_nodes.get_version(), 2)
    
    def test_get_ids(self):
        self.assertEqual(self.active_nodes.get_ids(), [])
        self.active_nodes.add_node(1, "node1")
        self.assertEqual(self.active_nodes.get_ids(), [1])
    
    def test_get_nodes(self):
        self.assertEqual(list(self.active_nodes.get_nodes()), [])
        self.active_nodes.add_node(1, "node1")
        self.assertEqual(list(self.active_nodes.get_nodes()), ["node1"])
    
    def test_add_node(self):
        self.active_nodes.add_node(1, "node1")
        self.assertEqual(list(self.active_nodes.get_nodes()), ["node1"])
        self.assertEqual(self.active_nodes.new_nodes(), [1])
        self.assertEqual(self.active_nodes.get_version(), 2)
    
    def test_remove_node(self):
        self.active_nodes.add_node(1, "node1")
        self.active_nodes.remove_node(1)
        self.assertIsNone(self.active_nodes.get_node(1))
        self.assertEqual(self.active_nodes.removed_nodes(), [1])
        self.assertEqual(self.active_nodes.get_version(), 3)
    
    def test_new_nodes(self):
        self.assertEqual(self.active_nodes.new_nodes(), [])
        self.active_nodes.add_node(1, "node1")
        self.assertEqual(self.active_nodes.new_nodes(), [1])
        self.active_nodes.reset_new_nodes()
        self.assertEqual(self.active_nodes.new_nodes(), [])
    
    def test_removed_nodes(self):
        self.assertEqual(self.active_nodes.removed_nodes(), [])
        self.active_nodes.add_node(1, "node1")
        self.active_nodes.remove_node(1)
        self.assertEqual(self.active_nodes.removed_nodes(), [1])
        self.active_nodes.reset_removed_nodes()
        self.assertEqual(self.active_nodes.removed_nodes(), [])


if __name__ == '__main__':
    unittest.main()