# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: node.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nnode.proto\"8\n\x0bNodeRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07ip_addr\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\x05\"e\n\x0cNodeResponse\x12\x15\n\rresponse_code\x18\x01 \x01(\x05\x12\x11\n\tleader_id\x18\x02 \x01(\t\x12\x16\n\x0eleader_ip_addr\x18\x03 \x01(\t\x12\x13\n\x0bleader_port\x18\x04 \x01(\x05\"T\n\x0cModelRequest\x12\x15\n\rmodel_version\x18\x01 \x01(\x05\x12\x17\n\x0fnum_data_points\x18\x02 \x01(\x05\x12\x14\n\x0cmodelWeights\x18\x03 \x03(\x02\"!\n\rModelResponse\x12\x10\n\x08received\x18\x01 \x01(\x08\"k\n\x10HeartbeatRequest\x12\x1c\n\x14\x61\x63tive_nodes_version\x18\x01 \x01(\x05\x12\x1c\n\x05model\x18\x02 \x01(\x0b\x32\r.ModelRequest\x12\x1b\n\x05nodes\x18\x03 \x03(\x0b\x32\x0c.NodeRequest\"%\n\x11HeartbeatResponse\x12\x10\n\x08received\x18\x01 \x01(\x08\x32\xc9\x02\n\x0cNodeExchange\x12-\n\x0cRegisterNode\x12\x0c.NodeRequest\x1a\r.NodeResponse\"\x00\x12/\n\x0e\x44\x65registerNode\x12\x0c.NodeRequest\x1a\r.NodeResponse\"\x00\x12\x34\n\x11ShareModelWeights\x12\r.ModelRequest\x1a\x0e.ModelResponse\"\x00\x12\x34\n\tHeartbeat\x12\x11.HeartbeatRequest\x1a\x12.HeartbeatResponse\"\x00\x12\x39\n\x16\x44istributeModelWeights\x12\r.ModelRequest\x1a\x0e.ModelResponse\"\x00\x12\x32\n\x11\x44\x65\x63lareLeadership\x12\x0c.NodeRequest\x1a\r.NodeResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'node_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NODEREQUEST._serialized_start=14
  _NODEREQUEST._serialized_end=70
  _NODERESPONSE._serialized_start=72
  _NODERESPONSE._serialized_end=173
  _MODELREQUEST._serialized_start=175
  _MODELREQUEST._serialized_end=259
  _MODELRESPONSE._serialized_start=261
  _MODELRESPONSE._serialized_end=294
  _HEARTBEATREQUEST._serialized_start=296
  _HEARTBEATREQUEST._serialized_end=403
  _HEARTBEATRESPONSE._serialized_start=405
  _HEARTBEATRESPONSE._serialized_end=442
  _NODEEXCHANGE._serialized_start=445
  _NODEEXCHANGE._serialized_end=774
# @@protoc_insertion_point(module_scope)
