# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0emessages.proto\"*\n\x0bModelWeight\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05\",\n\x0bNodeRequest\x12\x0f\n\x07ip_addr\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"p\n\x0cNodeResponse\x12\x15\n\rresponse_code\x18\x01 \x01(\x05\x12\x16\n\x0eleader_ip_addr\x18\x02 \x01(\t\x12\x13\n\x0bleader_port\x18\x03 \x01(\x05\x12\x12\n\x05\x65rror\x18\x04 \x01(\tH\x00\x88\x01\x01\x42\x08\n\x06_error\"/\n\x0eNetworkRequest\x12\x0f\n\x07ip_addr\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"?\n\x0fNetworkResponse\x12\x15\n\rresponse_code\x18\x01 \x01(\x05\x12\x15\n\rmodel_version\x18\x02 \x01(\x05\"H\n\x0cModelRequest\x12\x14\n\x0crequest_type\x18\x01 \x01(\x05\x12\"\n\x0cmodelWeights\x18\x02 \x03(\x0b\x32\x0c.ModelWeight\"\x0f\n\rModelResponse2\xd8\x01\n\rModelExchange\x12-\n\x0cRegisterNode\x12\x0c.NodeRequest\x1a\r.NodeResponse\"\x00\x12/\n\x0e\x44\x65registerNode\x12\x0c.NodeRequest\x1a\r.NodeResponse\"\x00\x12\x31\n\nPingLeader\x12\x0f.NetworkRequest\x1a\x10.NetworkResponse\"\x00\x12\x34\n\x11ShareModelWeights\x12\r.ModelRequest\x1a\x0e.ModelResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MODELWEIGHT._serialized_start=18
  _MODELWEIGHT._serialized_end=60
  _NODEREQUEST._serialized_start=62
  _NODEREQUEST._serialized_end=106
  _NODERESPONSE._serialized_start=108
  _NODERESPONSE._serialized_end=220
  _NETWORKREQUEST._serialized_start=222
  _NETWORKREQUEST._serialized_end=269
  _NETWORKRESPONSE._serialized_start=271
  _NETWORKRESPONSE._serialized_end=334
  _MODELREQUEST._serialized_start=336
  _MODELREQUEST._serialized_end=408
  _MODELRESPONSE._serialized_start=410
  _MODELRESPONSE._serialized_end=425
  _MODELEXCHANGE._serialized_start=428
  _MODELEXCHANGE._serialized_end=644
# @@protoc_insertion_point(module_scope)
