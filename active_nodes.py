#
# A lightweight class to store the list of active nodes in the system.
# Each node maintains their own ActiveNodes instance, which contains info
# about the other active nodes in the network.
#

class ActiveNodes():
    def __init__(self):
        self.version = 1
        self.active_nodes = {}
        self.recent_additions = []
        self.recent_deletions = []
    
    def get_node(self, id):
        return self.active_nodes.get(id)
    
    def get_version(self):
        return self.version
    
    def set_version(self, version):
        self.version = version
    
    def get_ids(self):
        ids = []
        for id, node in self.active_nodes.items():
            if node is not None:
                ids.append(id)
        return ids
    
    def get_nodes(self):
        print("[active_nodes] get_nodes")
        return self.active_nodes.values()
    
    def add_node(self, node_id, node):
        print("[active_nodes] add_node")
        self.active_nodes[node_id] = node
        self.recent_additions.append(node_id)
        self.version += 1

    def remove_node(self, node_id):
        print("[active_nodes] remove_node")
        self.active_nodes[node_id] = None
        # self.active_nodes.pop(node_id)
        self.recent_deletions.append(node_id)
        self.version += 1

    def new_nodes(self):
        return self.recent_additions
    
    def reset_new_nodes(self):
        self.recent_additions = []
    
    def removed_nodes(self):
        return self.recent_deletions
    
    def reset_removed_nodes(self):
        self.recent_deletions = []