import leader_pb2
import leader_pb2_grpc
import node_pb2
import node_pb2_grpc

#
# This class is the receiving portion of the Node.
# For simplicity, we moved it into its own file to 
# avoid cluttering node.py
#

class LeaderExchange(leader_pb2_grpc.LeaderExchange):
    def __init__(self, active_nodes):
        self.active_nodes = active_nodes
        self.model_version = 1

    def Heartbeat(self, request, context):
        print("received heartbeat!")
        response = leader_pb2.HeartbeatResponse(received=True)
        return response


class NodeExchange(node_pb2_grpc.NodeExchange):
    def __init__(self, id, ip_addr, port, active_nodes):
        self.id = id
        self.ip_addr = ip_addr
        self.port = port
        self.active_nodes = active_nodes
        self.model_version = 1

    def RegisterNode(self, request, context):
        print("Register Node!")
        
        node_id = request.node_id
        node_ip_addr = request.ip_addr
        node_port = request.port
        node_request = node_pb2.NodeRequest(
            node_id = node_id,
            ip_addr = node_ip_addr,
            port = node_port
        )

        self.active_nodes.add_node(node_id, node_request)
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
        
        node_id = request.node_id
        self.active_nodes.remove_node(node_id)
        print("active_nodes = ", self.active_nodes.get_ids())

        response = node_pb2.NodeResponse(response_code=200,leader_ip_addr=self.ip_addr,leader_port=self.port)
        return response

    def PingLeader(self, request, context):
        print("Ping Leader!")

        response = node_pb2.NetworkResponse(
            response_code=200,
            model_version=self.model_version,
            nodes=self.active_nodes.values()
        )
        return response
    
