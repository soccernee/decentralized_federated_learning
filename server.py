import node_pb2
import node_pb2_grpc

#
# This class is the receiving portion of the Node (the "server" in client-server lingo).
# For simplicity, we moved it into its own file to avoid cluttering node.py
#

class NodeExchange(node_pb2_grpc.NodeExchange):
    def __init__(self, id, ip_addr, port, active_nodes, heartbeat_timer):
        self.id = id
        self.ip_addr = ip_addr
        self.port = port
        self.active_nodes = active_nodes
        self.heartbeat_timer = heartbeat_timer
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
    
    def Heartbeat(self, request, context):
        self.heartbeat_timer.refresh()

        # logic to add new nodes and remove old nodes to active_nodes
        if request.active_nodes_version != self.active_nodes.get_version():
            print("different version! check nodes list")
            active_ids = self.active_nodes.get_ids()
            for node in request.nodes:
                if node.node_id not in active_ids:
                    print("adding this node to my active list! ", node.node_id)
                    self.active_nodes.add_node(node.node_id, node)

            current_ids = (n.node_id for n in request.nodes)
            for id in active_ids:
                if id not in current_ids:
                    print("removing node = ", id)
                    self.active_nodes.remove_node(id)
        

        response = node_pb2.HeartbeatResponse(received=True)
        return response
