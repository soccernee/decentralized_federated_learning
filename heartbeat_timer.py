import threading

# number of heartbeats that can be missed
EXPIRATION = 3

class HeartbeatTimer():
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count +=1 

    def refresh(self):
        self.count = 0 
    
    def expired(self):
        return self.count >= EXPIRATION