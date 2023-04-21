import threading

class HeartbeatTimer():
    def __init__(self, task):
        self.task = task
        time_period = 8
        self.timer = threading.Timer(time_period, self.task)

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.cancel()
    
    def refresh(self):
        self.stop()
        time_period = 8
        self.timer = threading.Timer(time_period, self.task)
        self.start()
