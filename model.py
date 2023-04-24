class Model():
    def __init__(self) -> None:
        self.x_data = None
        self.y_data = None
        self.model_weights = None
        self.new_data = True
        self._version = 0
        self.num_model_data_points = 0

    @property
    def version(self):
        return self._version

    def update_model(self, model_weights, num_data_points):
        self.model_weights = model_weights
        self.num_model_data_points = num_data_points
        self._version += 1
        self.new_data = True

    def set_new_data(self, new_data):
        self.new_data = new_data

    def get_model(self):
        return self.model_weights, self.num_model_data_points
    
    def add_data(self, data):
        self.x_data = data[0]
        self.y_data = data[1]
    
