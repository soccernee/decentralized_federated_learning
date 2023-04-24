# decentralized_federated_learning

Final Project for CS262: Distributed Systems, by @soccernee and @balt2.

This is a project to demonstrate the principles of distributed computing. We are building a centralized federated learning network, allowing anyone to connect to the network and share in the distributed machine learning network. The main idea of federated learning is that the data never leaves the individual node, just the updated model weights.

## To-Do-List

- [x] Nodes can connect to any node to find the leader
- [x] Nodes registers with the Leader
- [x] Leader connects to all (other) nodes
- [x] Leader maintains list of active nodes
- [x] Leader sends heartbeat to nodes (which includes active list of nodes & model weights)
- [x] Leader removes node from active list if heartbeat fails
- [x] Leader election if leader goes down
- [x] Base ML training per node
- [x] Nodes send updated model weights to Leader

## Setup

Run: `pip install sklearn openpyxl`

### Compiling for gRPC

These steps only need to occur after developmental changes. If you just cloned the repo and pulled down the latest you should not need to complete this step. However, if you make any changes to `node.proto`, you'll need to recompile by performing this step.

Run this command from the root directory: `python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. node.proto`

This will automatically update the `node_pb2.py` and `node_pb2_grpc.py` files for you (or generate them if they don't exist).


## Deployment

For the initial leader, run: `python node_server.py leader`. It is important to perform this step first.
For any other node, run: `python node_server.py <id>`. Example: `python node_server.py 3`

## Next Steps

We did not handle some things for the purpose of this assignment, including:
* Security & Authentication