from concurrent import futures
import grpc
import random
import _thread
import time
import signal
import sys
import uuid

import config
import leader_pb2
import leader_pb2_grpc
import node_pb2
import node_pb2_grpc

from server import LeaderExchange, NodeExchange 

class ActiveNodes():
    def __init__(self):
        self.active_nodes = {}
        self.recent_additions = []
        self.recent_deletions = []
    
    def get_node(self, id):
        return self.active_nodes.get(id)
    
    def get_ids(self):
        return self.active_nodes.keys()
    
    def get_nodes(self):
        return self.active_nodes.values()
    
    def add_node(self, node_id, node_request):
        self.active_nodes[node_id] = node_request
        self.recent_additions.append(node_id)

    def remove_node(self, node_id):
        self.active_nodes.pop(node_id)
        self.recent_deletions.append(node_id)

    def new_nodes(self):
        return self.recent_additions
    
    def reset_new_nodes(self):
        self.recent_additions = []
    
    def removed_nodes(self):
        return self.recent_deletions
    
    def reset_removed_nodes(self):
        self.recent_deletions = []

class Node():
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
        leader_pb2_grpc.add_LeaderExchangeServicer_to_server(LeaderExchange(self.active_nodes), server)
        server.add_insecure_port('[::]:' + str_port)
        server.start()
        print("Servers started, listening... ")
        server.wait_for_termination()
        
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
    
    def update_node_connections(self):
        print("update_node_connections")
        if len(self.active_nodes.new_nodes()):
            print("new node found!")

            # connect to any new nodes
            for node_id in self.active_nodes.new_nodes():
                if not (node_id in self.stubs):
                    node = self.active_nodes.get_node(node_id)
                    print("adding new stub! where node = ", node)
                    ip_addr = node.ip_addr 
                    print("ip_addr = ", ip_addr)
                    port = node.port

                    new_channel = grpc.insecure_channel('{}:{}'.format(ip_addr, port))
                    new_stub = leader_pb2_grpc.LeaderExchangeStub(new_channel)
                    self.stubs[node_id] = new_stub

        # remove new nodes from list
        self.active_nodes.reset_new_nodes()

        # TODO: remove any old nodes
        
    def send_heartbeat(self):
        print("function: send_heartbeat")
        for node_id in self.active_nodes.get_ids():
            stub = self.stubs[node_id]
            print("sending heartbeat to node = ", node_id)
            response = stub.Heartbeat(leader_pb2.HeartbeatRequest(nodes=self.active_nodes.get_nodes()))
            if response.received != True:
                print("received bad response from node = ", node_id)

    def should_retrain_model(self):
        return False
    
    def end_session(self):
        self.deregister()

    def signal_handler(self, signal, frame):
        print('You quit the program!')
        self.end_session()
        self.SIGINT = True
        sys.exit(0)

    def main(self):
        print("Starting...")

        # try:
        while True:
            print("in loop!")
            time.sleep(5)
            
            if self.is_leader:
                self.update_node_connections()
                self.send_heartbeat()
            if self.should_retrain_model():
                print("should retrain model!")

        # except Exception as err:
        #     print(f"Unexpected {err=}, {type(err)=}")



node = Node()