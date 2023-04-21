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
    
    @property
    def alive(self):
        return self._alive
    
    def set_alive(self, alive):
        self._alive = alive