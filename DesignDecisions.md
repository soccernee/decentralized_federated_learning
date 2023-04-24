# Engineering Notebook

We designed a decentralized federated learning network to scale to n-nodes. One of the nodes serves as leader. Message passing happens through gRPC.

## Network

### Startup

When any new node decides to join the network, it pings the nodes in the known node list (config.LEADERS). Only one of these nodes needs to be in the network for a new node to join. The new node iterates through the known nodes and finds the first one that connects. It then asks that node for the leader's ip address and port. 

Once it knows who the leader is, the new node registers itself with the leader. 

### List of Active Nodes

The leader maintains a list of active nodes. It sends this to all of the nodes in every heartbeat.

### Nodes

The nodes receive the heartbeats from the leader. Both the list of active nodes and the model weights have a version number. When that version number is bumped, the node knows to overwrite its local copy of that data with the copy in the heartbeat.

### Nodes Exiting

If a node gracefully exits, it deregisters itself with the leader. The leader can remove it from the active nodes list and stop sending it heartbeats. 

If a node crashes, it still remains in the active list. When the leader goes to send the next heartbeat to that node, it will fail. At that point, the leader removes that node from the active nodes list. 

Any change to the active nodes list gets propagated to every node through the heartbeats.

### Leader Election

When 3 heartbeats are missed, the nodes declare the leader lost. The node with the highest uuid declares itself the leader, and sends a message to the other leaders. The other leaders accept this new leader.


## Machine Learning

We prototyped 5 out-of-the-box ML models on our dataset: decision tree, random forest, k-nearest neighbors, logistic regression, neural network. We found that the logistic regression model worked best, so we used that for our network.