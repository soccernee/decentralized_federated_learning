from concurrent import futures
import grpc
import random
import _thread
import time
import socket
import signal
import sys
import uuid

import config
from model import Model
from model_train import MachineLearning
import node_pb2
import node_pb2_grpc

from node import Node
from server import NodeExchange 
from active_nodes import ActiveNodes
from heartbeat_timer import HeartbeatTimer

class NodeServer():
    #
    # Initialization functions
    #

    def __init__(self):
        random.seed()

        self.is_leader = False
        self.node = None # this node's information
        self.leader = None

        self.id = str(uuid.uuid4())
        self.leader_stub = None
        self.stubs = {}
        self.active_nodes = ActiveNodes()
        self.machine_learning = MachineLearning()
        self.model = Model()
        self.heartbeat_timer = HeartbeatTimer()

        if len(sys.argv) > 1:
            data = str(sys.argv[1])
            if data == "leader":
                self.is_leader = True
            elif data == "1" or data == "2" or data == "3" or data == "4" or data == "5":
                node_info = config.LEADERS[int(data)] 
                self.ip_addr = node_info[0]
                self.port = node_info[1]
            else:
                sys.exit("Please specify if this node is a leader or not")
        else:
            sys.exit("Please specify if this node is a leader or not")

        # Logic to handle SIGINT
        self.SIGINT = False
        signal.signal(signal.SIGINT, self.signal_handler)

        if self.is_leader:
            leader = config.LEADERS[0]
            self.ip_addr = leader[0]
            self.port = leader[1]

            print(f'Is the leader! {self.ip_addr}:{self.port}')

            self.node = Node(self.id, self.ip_addr, self.port, True)
            self.leader = self.node
            self.machine_learning.leader_train(self.model)
        else:
            print("not a leader!")
            self.set_defaults()
            self.model.add_data(self.machine_learning.get_data_for_node(int(data)))
            self.connect_to_leader()
            time.sleep(2)
            self.register()

        _thread.start_new_thread(self.listen, ())
        self.main()

    def set_defaults(self):
        self.is_leader = False
        self.node = Node(self.id, self.ip_addr, self.port, True)

    def listen(self):
        str_port = str(self.port)
        print(f'listening at {self.ip_addr}:{str_port}')

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        node_pb2_grpc.add_NodeExchangeServicer_to_server(
            NodeExchange(self.node, self.active_nodes, self.heartbeat_timer, self.leader, self.model), server)
        server.add_insecure_port('[::]:' + str_port)
        server.start()
        print("Servers started, listening... ")
        server.wait_for_termination()

    #
    # Functions to perform when the node is not the leader
    #
    
    def check_if_open(self, host, port):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location = (host, port)
        result_of_check = a_socket.connect_ex(location)

        if result_of_check == 0:
            print("Port is open")
        else:
            print("Port is not open")
        a_socket.close()
        return result_of_check

    def connect_to_leader(self):
        print("Connect to Leader")

        need_leader = True
        node_count = -1
        while need_leader and node_count < len(config.LEADERS):
            node_count += 1
            host = config.LEADERS[node_count][0]
            port = config.LEADERS[node_count][1]
            print(f'Trying to connect to node: {host}:{port}')
            need_leader = self.check_if_open(host, port)

        #connect with alive node and ask who the leader is
        new_channel = grpc.insecure_channel('{}:{}'.format(host, port))
        temp_stub = node_pb2_grpc.NodeExchangeStub(new_channel)
        response = temp_stub.AskForLeader(node_pb2.NodeRequest(id=self.id, ip_addr=self.ip_addr, port=self.port))
        if response.response_code == 200:
            print("Found the leader: ", response)
            self.leader = Node('0', response.leader_ip_addr, response.leader_port, False)
        else:
            print("Uh Oh, trouble with the Leader. Response = ", response)

        # connect with the leader
        channel = grpc.insecure_channel(
            '{}:{}'.format(self.leader.ip_addr, self.leader.port))
        self.leader_stub = node_pb2_grpc.NodeExchangeStub(channel)

    def register(self):
        print("register")
        response = self.leader_stub.RegisterNode(node_pb2.NodeRequest(id=self.id, ip_addr=self.ip_addr, port=self.port))
        self.leader.set_alive(True)

    def deregister(self):
        print("deregister")
        if not self.is_leader:
            self.leader_stub.DeregisterNode(node_pb2.NodeRequest(id=self.id, ip_addr=self.ip_addr, port=self.port))

    def heartbeat_expired(self):
        print("heartbeat_expired!!!!!!!!!!")
        self.leader.set_alive(False)
    
        highest_id = True
        for id in self.active_nodes.get_ids():
            if id == self.id:
                continue
            if self.id < id:
                highest_id = False

        # bug fix: if only one node in network, it should become the leader
        if len(self.active_nodes.get_ids()) == 1:
            print("I am the only one")
            highest_id = True

        if highest_id:
            self.declare_leadership()
        else:
            time.sleep(4)

    #
    # Functions to perform when the Node is a leader
    #
    def send_heartbeat(self):
        active_ids = list(self.active_nodes.get_ids()).copy()
        active_nodes_version = self.active_nodes.get_version()
        print("function: send_heartbeat to nodes: ", active_ids)

        model_weights, num_data_points = self.model.get_model()
        model_request = node_pb2.ModelRequest(model_version=self.model.version, num_data_points=num_data_points, modelWeights=model_weights)
        heartbeat_request = node_pb2.HeartbeatRequest(active_nodes_version=active_nodes_version, model=model_request)
        for node_id in active_ids:
            node = self.active_nodes.get_node(node_id)
            if node is None:
                continue
            heartbeat_request.nodes.append(node_pb2.NodeRequest(id=node.id, ip_addr=node.ip_addr, port=node.port))

        for node_id in active_ids:
            if node_id in self.stubs:
                stub = self.stubs[node_id]
                print("sending heartbeat to node = ", node_id)
                response = stub.Heartbeat(heartbeat_request)
                if response.received != True:
                    print("received bad response from node = ", node_id)

    #
    # Functions all nodes perform
    #

    def declare_leadership(self):
        count_nodes = 0
        count_yes = 0
        for node_id in self.active_nodes.get_ids():
            if node_id == self.id:
                continue
            count_nodes += 1
            stub = self.stubs[node_id]
            print("declaring leadership to node = ", node_id)
            response = stub.DeclareLeadership(node_pb2.NodeRequest(id=self.id, ip_addr=self.ip_addr, port=self.port))
            print("response! = ", response)

            if response.response_code == 200:
                count_yes += 1

        if count_yes > (count_nodes / 2) or count_nodes == 0:
            print("I AM THE LEADER")
            self.is_leader = True
            self.leader_stub = None

            self.leader.set_id(self.id)
            self.leader.set_ip_addr(self.ip_addr)
            self.leader.set_port(self.port)
            self.leader.set_alive(True)

            print("self.leader.port = ", self.leader.port)
            self.active_nodes.remove_node(self.id)
            
    def recognize_new_leadership(self):
        print("recognize new leadership")
        self.leader_stub = self.stubs[self.leader.id]
        self.stubs.pop(self.leader.id)
        self.leader.set_leader_flag(False) # reset to False

    def update_node_connections(self):
        # connect to any new nodes
        for node_id in self.active_nodes.new_nodes():
            if node_id != self.id and not (node_id in self.stubs):
                node = self.active_nodes.get_node(node_id)
                if node is None:
                    continue
                ip_addr = node.ip_addr
                port = node.port

                new_channel = grpc.insecure_channel('{}:{}'.format(ip_addr, port))
                new_stub = node_pb2_grpc.NodeExchangeStub(new_channel)
                self.stubs[node_id] = new_stub

        # remove new nodes from new additions list
        self.active_nodes.reset_new_nodes()

        # remove any old nodes
        for node_id in self.active_nodes.removed_nodes():
            if node_id != self.id and (node_id in self.stubs):
                self.stubs.pop(node_id)

        # remove removed nodes from removed additions list
        self.active_nodes.reset_removed_nodes()

    def signal_handler(self, signal, frame):
        print('\nYou quit the program!')
        self.end_session()
        self.SIGINT = True
        sys.exit(0)
    
    def end_session(self):
        self.deregister()

    def retrain_model(self):
        print("retrain model!")
        self.machine_learning.train_for_node(self.model)
        if self.leader_stub:
            weights, num_model_data_points  = self.model.get_model()
            print(weights)

            try:
                response = self.leader_stub.DistributeModelWeights(
                    node_pb2.ModelRequest(model_version=0, num_data_points=num_model_data_points, modelWeights=weights))
            except grpc.RpcError as e:
                if isinstance(e, grpc._channel._InactiveRpcError):
                    print("Connect with Leader closed unexpectedly! error = ", e)
                    return
                else:
                    # Handle other gRPC errors here
                    print("some other gRPC error:", e)
                    return

            print("response sending updated weights = ", response)
        else:
            print("Failed to send updated model to leader")

    def main(self):
        print(f'[node_id: {self.id}] Starting...')

        while True:
            time.sleep(4)

            if self.leader.get_new_leader_flag():
                self.recognize_new_leadership()

            self.update_node_connections()

            if self.is_leader:
                self.send_heartbeat()
            else:
                if random.randint(0, 100) < 20:
                    self.retrain_model()

                self.heartbeat_timer.increment()
                if self.heartbeat_timer.expired():
                    self.heartbeat_expired()

node = NodeServer()