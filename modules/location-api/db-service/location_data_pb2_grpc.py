# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import location_data_pb2 as location__data__pb2


class LocationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SaveLocation = channel.unary_unary(
                '/LocationService/SaveLocation',
                request_serializer=location__data__pb2.LocationData.SerializeToString,
                response_deserializer=location__data__pb2.LocationData.FromString,
                )
        self.GetAllLocations = channel.unary_unary(
                '/LocationService/GetAllLocations',
                request_serializer=location__data__pb2.Empty.SerializeToString,
                response_deserializer=location__data__pb2.LocationDataList.FromString,
                )


class LocationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SaveLocation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllLocations(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LocationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SaveLocation': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveLocation,
                    request_deserializer=location__data__pb2.LocationData.FromString,
                    response_serializer=location__data__pb2.LocationData.SerializeToString,
            ),
            'GetAllLocations': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllLocations,
                    request_deserializer=location__data__pb2.Empty.FromString,
                    response_serializer=location__data__pb2.LocationDataList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'LocationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LocationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SaveLocation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LocationService/SaveLocation',
            location__data__pb2.LocationData.SerializeToString,
            location__data__pb2.LocationData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllLocations(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LocationService/GetAllLocations',
            location__data__pb2.Empty.SerializeToString,
            location__data__pb2.LocationDataList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
