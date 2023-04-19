import node_pb2 as pb2
import node_pb2_grpc as pb2_grpc

#
# This class is the receiving portion of the Node.
# For simplicity, we moved it into its own file to 
# avoid cluttering node.py
#

class NodeExchange(pb2_grpc.NodeExchange):
    def __init__(self, id, ip_addr, port):
        self.nodes = {}
        self.id = id
        self.ip_addr = ip_addr
        self.port = port
        self.model_version = 1

    def RegisterNode(self, request, context):
        print("Register Node!")
        
        node_id = request.node_id
        node_ip_addr = request.ip_addr
        node_port = request.port

        self.nodes[node_id] = pb2.NodeRequest(
            node_id = node_id,
            ip_addr = node_ip_addr,
            port = node_port
        )
        print("nodes = ", self.nodes)

        response = pb2.NodeResponse(
            response_code=200,
            leader_id=self.id,
            leader_ip_addr=self.ip_addr,
            leader_port=self.port
        )
        return response

    def DeregisterNode(self, request, context):
        print("Deregister Node!")
        
        node_id = request.node_id
        self.nodes.pop(node_id)
        print("nodes = ", self.nodes)

        response = pb2.NodeResponse(response_code=200,leader_ip_addr=self.ip_addr,leader_port=self.port)
        return response

    def PingLeader(self, request, context):
        print("Ping Leader!")

        response = pb2.NetworkResponse(
            response_code=200,
            model_version=self.model_version,
            nodes=self.nodes.values()
        )
        return response