import unittest

from model import Model

class TestModel(unittest.TestCase):
    def test_initialization(self):
        model = Model()
        self.assertIsNone(model.x_data)
        self.assertIsNone(model.y_data)
        self.assertIsNone(model.model_weights)
        self.assertTrue(model.new_data)
        self.assertEqual(model.version, 0)
        self.assertEqual(model.num_model_data_points, 0)

    def test_update_model(self):
        model = Model()
        model_weights = [1, 2, 3]
        num_data_points = 100
        model.update_model(model_weights, num_data_points)
        self.assertEqual(model.model_weights, model_weights)
        self.assertEqual(model.num_model_data_points, num_data_points)
        self.assertEqual(model.version, 1)
        self.assertTrue(model.new_data)

    def test_set_new_data(self):
        model = Model()
        model.set_new_data(False)
        self.assertFalse(model.new_data)
        model.set_new_data(True)
        self.assertTrue(model.new_data)

    def test_get_model(self):
        model = Model()
        model_weights = [1, 2, 3]
        num_data_points = 100
        model.update_model(model_weights, num_data_points)
        returned_weights, returned_num_data_points = model.get_model()
        self.assertEqual(returned_weights, model_weights)
        self.assertEqual(returned_num_data_points, num_data_points)

    def test_add_data(self):
        model = Model()
        x_data = [1, 2, 3]
        y_data = [4, 5, 6]
        model.add_data((x_data, y_data))
        self.assertEqual(model.x_data, x_data)
        self.assertEqual(model.y_data, y_data)

if __name__ == '__main__':
    unittest.main()