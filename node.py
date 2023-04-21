from concurrent import futures
import grpc
import random
import _thread
import time
import signal
import sys
import uuid

import config
import node_pb2
import node_pb2_grpc

from server import NodeExchange 
from active_nodes import ActiveNodes

class Node():
    #
    # Initialization functions
    #

    def __init__(self):
        random.seed()

        self.is_leader = False
        self.id = str(uuid.uuid4())
        self.stubs = {}
        self.active_nodes = ActiveNodes()

        if len(sys.argv) > 1:
            data = str(sys.argv[1])
            if data == "leader":
                self.is_leader = True

        # Logic to handle SIGINT
        self.SIGINT = False
        signal.signal(signal.SIGINT, self.signal_handler)

        if self.is_leader:
            print("is leader!")
            self.ip_addr = config.LEADER_HOST
            self.port = config.LEADER_PORT
        else:
            print("not a leader!")
            self.set_defaults()
            self.connect_to_leader()
            time.sleep(2)
            self.register()

        _thread.start_new_thread(self.listen, ())
        self.main()

    def set_defaults(self):
        ip_addr = 'localhost'
        print("ip_addr = ", ip_addr)

        self.ip_addr = ip_addr 
        self.port = 6188 + random.randint(0, 100)
        self.is_leader = False
        self.leader_host = config.LEADER_HOST
        self.leader_port = config.LEADER_PORT

    def listen(self):
        str_port = str(self.port)
        print("listening on port, ", str_port)

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        node_pb2_grpc.add_NodeExchangeServicer_to_server(
            NodeExchange(self.id, self.ip_addr, self.port, self.active_nodes), server)
        server.add_insecure_port('[::]:' + str_port)
        server.start()
        print("Servers started, listening... ")
        server.wait_for_termination()
        
    #
    # Functions to perform when the node is not the leader
    #

    def connect_to_leader(self):
        print("Connect to Leader")
        # register with the leader
        channel = grpc.insecure_channel(
            '{}:{}'.format(self.leader_host, self.leader_port))
        
        self.node_stub = node_pb2_grpc.NodeExchangeStub(channel)

    def register(self):
        print("register")
        print("id = ", self.id)
        response = self.node_stub.RegisterNode(node_pb2.NodeRequest(node_id=self.id, ip_addr=self.ip_addr, port=self.port))
        print(response)

    def deregister(self):
        print("deregister")
        if not self.is_leader:
            self.node_stub.DeregisterNode(node_pb2.NodeRequest(node_id=self.id, ip_addr=self.ip_addr, port=self.port))


    #
    # Functions to perform when the Node is a leader
    #

    def update_node_connections(self):
        print("update_node_connections")

        # connect to any new nodes
        for node_id in self.active_nodes.new_nodes():
            print("new node(s) found!")
            if not (node_id in self.stubs):
                node = self.active_nodes.get_node(node_id)
                ip_addr = node.ip_addr
                port = node.port

                new_channel = grpc.insecure_channel('{}:{}'.format(ip_addr, port))
                new_stub = node_pb2_grpc.NodeExchangeStub(new_channel)
                self.stubs[node_id] = new_stub

        # remove new nodes from new additions list
        self.active_nodes.reset_new_nodes()

        # remove any old nodes
        for node_id in self.active_nodes.removed_nodes():
            if (node_id in self.stubs):
                self.stubs.pop(node_id)

        # remove removed nodes from removed additions list
        self.active_nodes.reset_removed_nodes()
    
    def send_heartbeat(self):
        print("function: send_heartbeat")
        for node_id in self.active_nodes.get_ids():
            stub = self.stubs[node_id]
            print("sending heartbeat to node = ", node_id)
            response = stub.Heartbeat(node_pb2.HeartbeatRequest(nodes=self.active_nodes.get_nodes()))
            if response.received != True:
                print("received bad response from node = ", node_id)

    def should_retrain_model(self):
        return False

    #
    # Functions all nodes perform
    #

    def signal_handler(self, signal, frame):
        print('You quit the program!')
        self.end_session()
        self.SIGINT = True
        sys.exit(0)
    
    def end_session(self):
        self.deregister()

    def main(self):
        print("Starting...")

        while True:
            print("in loop!")
            time.sleep(5)
            
            if self.is_leader:
                self.update_node_connections()
                self.send_heartbeat()
            if self.should_retrain_model():
                print("should retrain model!")



node = Node()