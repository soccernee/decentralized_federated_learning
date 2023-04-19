#
# A lightweight class to store the list of active nodes in the system.
# Each node maintains their own ActiveNodes instance, which contains info
# about the other active nodes in the network.
#

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