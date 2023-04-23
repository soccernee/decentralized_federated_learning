class Model():
    def __init__(self) -> None:
        self.model_weights = None
        self.model_version = 1
        self.num_model_data_points = 0

    
    def update_model(self, model_weights, version, num_data_points):
        self.model_weights = model_weights
        self.model_version = version
        self.num_model_data_points = num_data_points

    def get_model(self):
        return self.model_weights, self.model_version, self.num_model_data_points
    
