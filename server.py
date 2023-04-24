import node_pb2
import node_pb2_grpc

from node import Node

#
# This class is the receiving portion of the Node (the "server" in client-server lingo).
# For simplicity, we moved it into its own file to avoid cluttering node.py
#

class NodeExchange(node_pb2_grpc.NodeExchange):
    def __init__(self, node, active_nodes, heartbeat_timer, leader, new_leader_flag, model):
        self.id = node.id
        self.ip_addr = node.ip_addr
        self.port = node.port
        self.active_nodes = active_nodes
        self.heartbeat_timer = heartbeat_timer
        self.leader = leader
        self.new_leader_flag = new_leader_flag
        self.model = model

    def RegisterNode(self, request, context):
        print("Register Node!")
        
        new_node = Node(request.id, request.ip_addr, request.port, True)

        self.active_nodes.add_node(request.id, new_node)
        print("active_nodes = ", self.active_nodes.get_ids())

        response = node_pb2.NodeResponse(
            response_code=200,
            leader_id=self.id,
            leader_ip_addr=self.ip_addr,
            leader_port=self.port
        )
        return response

    def DeregisterNode(self, request, context):
        print("Deregister Node!")
        
        node_id = request.id
        self.active_nodes.remove_node(node_id)

        response = node_pb2.NodeResponse(response_code=200,leader_ip_addr=self.ip_addr,leader_port=self.port)
        return response
    
    def Heartbeat(self, request, context):
        print("heartbeat received")
        self.heartbeat_timer.refresh()

        # logic to add new nodes and remove old nodes to active_nodes
        if request.active_nodes_version != self.active_nodes.get_version():
            active_ids = self.active_nodes.get_ids()
            for node in request.nodes:
                if node is not None and node.id not in active_ids:
                    self.active_nodes.add_node(node.id, node)

            current_ids = list(n.id for n in request.nodes)
            for id in active_ids:
                node = self.active_nodes.get_node(id)
                if node is not None and id not in current_ids:
                    self.active_nodes.remove_node(id)

            self.active_nodes.set_version(request.active_nodes_version)
        
        # update own model with server model
        if request.model and request.model.model_version != self.model.version:
            print("new model version! time to update")
            print("modelWeights = ", request.model.modelWeights)
            self.model.update_model(request.model.modelWeights, request.model.num_data_points)        

        response = node_pb2.HeartbeatResponse(received=True)
        return response
    
    def DeclareLeadership(self, request, context):
        # accept the new leader
        print("accept the new leader! ", request.id)
        self.leader = Node(request.id, request.ip_addr, request.port, True)
        self.new_leader_flag = True

        response = node_pb2.NodeResponse(
            response_code=200,
            leader_id=self.leader.id,
            leader_ip_addr=self.leader.ip_addr,
            leader_port=self.leader.port
        )
        return response
    
    def DistributeModelWeights(self, request, context):
        print("distribute model weights!")
        
        self.model.update_model(request.modelWeights, request.num_data_points)

        response = node_pb2.ModelResponse(
            received=True,
        )

        return response
    
    def AskForLeader(self, request, context):
        print("AskForLeader")
        print("self.leader = ", self.leader)
        response = node_pb2.NodeResponse(
            response_code=200,
            leader_id=self.leader.id,
            leader_ip_addr=self.leader.ip_addr,
            leader_port=self.leader.port
        )
        return response