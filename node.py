class Node():
    def __init__(self, id, ip_addr, port, alive=False):
        self._id = id
        self._ip_addr = ip_addr
        self._port = port
        self._alive = alive
        self.new_leader_flag = False

    @property
    def id(self):
        return self._id
    
    def set_id(self, id):
        self._id = id

    @property
    def ip_addr(self):
        return self._ip_addr
    
    def set_ip_addr(self, ip_addr):
        self._ip_addr = ip_addr

    @property
    def port(self):
        return self._port
    
    def set_port(self, port):
        self._port = port

    def get_new_leader_flag(self):
        return self.new_leader_flag
    
    def set_leader_flag(self, val):
        self.new_leader_flag = val

    def get_alive(self):
        return self._alive
    
    def set_alive(self, new_state):
        self._alive = new_state