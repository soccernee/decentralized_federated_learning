from concurrent import futures
import _thread
import time
import sys

import config
import grpc
import messages_pb2 as pb2
import messages_pb2_grpc as pb2_grpc
import signal


class ModelExchange(pb2_grpc.ModelExchange):
    def __init__(self, ip_addr, port):
        self.nodes = []
        self.ip_addr = ip_addr
        self.port = port

    def RegisterNode(self, request, context):
        print("Register Node!")
        
        node_ip_addr = request.ip_addr
        node_port = request.port

        self.nodes.append({
            'ip_addr': node_ip_addr,
            'port': node_port,
        })
        print("nodes = ", self.nodes)

        response = pb2.NodeResponse(response_code=200,leader_ip_addr=self.ip_addr,leader_port=self.port)
        return response

    def PingLeader(self, request, context):
        print("Ping Leader!")

        response = pb2.NetworkResponse(response_code=200, model_version=3)
        return response

class Node():
    def __init__(self):
        self.is_leader = False

        if len(sys.argv) > 1:
            data = str(sys.argv[1])
            if data == "leader":
                self.is_leader = True

        #Logic to handle SIGINT
        self.SIGINT = False
        signal.signal(signal.SIGINT, self.signal_handler)

        if self.is_leader:
            print("is leader!")
            self.ip_addr = config.LEADER_HOST
            self.port = config.LEADER_PORT
            self.listen()
        else:
            print("not a leader!")
            self.set_defaults()
            self.connect_to_leader()

        self.main()

    def is_leader(self):
        return False

    def set_defaults(self):
        print("Node set_defaults")
        self.ip_addr = 'localhost'
        self.port = 6188
        self.is_leader = False
        self.leader_host = config.LEADER_HOST
        self.leader_port = config.LEADER_PORT

    def listen(self):
        print("setting up listening port")
        str_port = str(self.port)

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_ModelExchangeServicer_to_server(ModelExchange(self.ip_addr, self.port), server)
        server.add_insecure_port('[::]:' + str_port)
        server.start()
        print("Server started, listening on " + str_port)
        server.wait_for_termination()
        
    def connect_to_leader(self):
        print("Connect to Leader")
        # register with the leader
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.leader_host, self.leader_port))
        
        self.leader_stub = pb2_grpc.ModelExchangeStub(self.channel)

    def register(self):
        print("register")
        response = self.leader_stub.RegisterNode(pb2.NodeRequest(ip_addr=self.ip_addr, port=self.port))
        print(response)
        if response.response_code == 200:
            _thread.start_new_thread(self.start_leader_polling, ())
        elif response.response_code == 404:
            print("Error : ", response.response_text)

    def start_leader_polling(self):
        while True:
            self.ping_leader()

            #How long we wait to poll the server for new messages  
            time.sleep(1)
        return

    def ping_leader(self):
        response = self.leader_stub.PingLeader(pb2.NetworkRequest(ip_addr=self.ip_addr, port=self.port))
        if response.response_code == 200:
            print("Ping Leader Response: ", response)
        return response
    
    def should_retrain_model(self):
        return False
    
    def end_session(self):
        pass

    def signal_handler(self, signal, frame):
        print('You quit the program!')
        self.end_session()
        self.SIGINT = True
        sys.exit(0)

    def main(self):
        print("Starting...")
        self.register()

        try:
            while True:
               print("in loop!")
               time.sleep(2)
               if self.should_retrain_model():
                   print("should retrain model!")

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")



node = Node()