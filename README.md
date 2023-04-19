# decentralized_federated_learning

Final Project for CS262: Distributed Systems, by @soccernee and @balt2.

This is a project to demonstrate the principles of distributed computing. We are building a centralized federated learning network, allowing anyone to connect to the network and share in the distributed machine learning network. The main idea of federated learning is that the data never leaves the individual node, just the updated model weights.

## To-Do-List

- [x] Nodes connect to Leader
- [x] Leader connects to all (other) nodes
- [x] Leader maintains list of active nodes
- [x] Leader sends heartbeat to nodes (which includes active list of nodes)
- [] Leader election if leader goes down
- [] Base ML training per node
- [] Nodes send updated model weights to Leader
- [] Leader aggregates weights and pushes update to all nodes


## Setup

### Compiling for gRPC

These steps only need to occur after developmental changes. If you just cloned the repo and pulled down the latest you should not need to complete this step. However, if you make any changes to `node.proto`, you'll need to recompile by performing this step. Same for `leader.proto`

1. Run this command from the root directory: `python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. node.proto`

This will automatically update the `node_pb2.py` and `node_pb2_grpc.py` files for you (or generate them if they don't exist).

2. Run this command from the root directory: `python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. leader.proto`

This will automatically update the `leader_pb2.py` and `leader_pb2_grpc.py` files for you (or generate them if they don't exist).


## Deployment

For the initial leader, run: `python node.py leader`. 
For any other node, run: `python node.py`

## Testing

TODO

## Next Steps

We did not handle some things for the purpose of this assignment, including:
* Security & Authentication