class Node():
    def __init__(self, id, ip_addr, port, alive=False):
        self._id = id
        self._ip_addr = ip_addr
        self._port = port
        self._alive = alive

    @property
    def id(self):
        return self._id

    @property
    def ip_addr(self):
        return self._ip_addr

    @property
    def port(self):
        return self._port
    
    def get_alive(self):
        return self._alive
    
    def set_alive(self, new_state):
        self._alive = new_state