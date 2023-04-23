class Model():
    def __init__(self) -> None:
        self.x_data = None
        self.y_data = None
        self.model_weights = None
        self.num_model_data_points = 0
    
    def update_model(self, model_weights, num_data_points):
        self.model_weights = model_weights
        self.num_model_data_points = num_data_points

    def get_model(self):
        return self.model_weights, self.num_model_data_points
    
    def add_data(self, data):
        self.x_data = data[0]
        self.y_data = data[1]
    
