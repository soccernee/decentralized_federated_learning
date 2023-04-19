# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import node_pb2 as node__pb2


class NodeExchangeStub(object):
    """
    NodeExchange: the message exchange service definition for the nodes to connect with the leader.
    These functions are receieved by the Leader.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterNode = channel.unary_unary(
                '/NodeExchange/RegisterNode',
                request_serializer=node__pb2.NodeRequest.SerializeToString,
                response_deserializer=node__pb2.NodeResponse.FromString,
                )
        self.DeregisterNode = channel.unary_unary(
                '/NodeExchange/DeregisterNode',
                request_serializer=node__pb2.NodeRequest.SerializeToString,
                response_deserializer=node__pb2.NodeResponse.FromString,
                )
        self.ShareModelWeights = channel.unary_unary(
                '/NodeExchange/ShareModelWeights',
                request_serializer=node__pb2.ModelRequest.SerializeToString,
                response_deserializer=node__pb2.ModelResponse.FromString,
                )


class NodeExchangeServicer(object):
    """
    NodeExchange: the message exchange service definition for the nodes to connect with the leader.
    These functions are receieved by the Leader.
    """

    def RegisterNode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeregisterNode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ShareModelWeights(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NodeExchangeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterNode': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterNode,
                    request_deserializer=node__pb2.NodeRequest.FromString,
                    response_serializer=node__pb2.NodeResponse.SerializeToString,
            ),
            'DeregisterNode': grpc.unary_unary_rpc_method_handler(
                    servicer.DeregisterNode,
                    request_deserializer=node__pb2.NodeRequest.FromString,
                    response_serializer=node__pb2.NodeResponse.SerializeToString,
            ),
            'ShareModelWeights': grpc.unary_unary_rpc_method_handler(
                    servicer.ShareModelWeights,
                    request_deserializer=node__pb2.ModelRequest.FromString,
                    response_serializer=node__pb2.ModelResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'NodeExchange', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NodeExchange(object):
    """
    NodeExchange: the message exchange service definition for the nodes to connect with the leader.
    These functions are receieved by the Leader.
    """

    @staticmethod
    def RegisterNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NodeExchange/RegisterNode',
            node__pb2.NodeRequest.SerializeToString,
            node__pb2.NodeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeregisterNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NodeExchange/DeregisterNode',
            node__pb2.NodeRequest.SerializeToString,
            node__pb2.NodeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ShareModelWeights(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NodeExchange/ShareModelWeights',
            node__pb2.ModelRequest.SerializeToString,
            node__pb2.ModelResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
