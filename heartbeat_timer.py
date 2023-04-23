import threading

# class HeartbeatTimer():
#     def __init__(self, task):
#         self.task = task
#         time_period = 8
#         self.timer = threading.Timer(time_period, self.task)

#     def start(self):
#         self.timer.start()

#     def stop(self):
#         self.timer.cancel()
    
#     def refresh(self):
#         self.stop()
#         time_period = 8
#         self.timer = threading.Timer(time_period, self.task)
#         self.start()

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