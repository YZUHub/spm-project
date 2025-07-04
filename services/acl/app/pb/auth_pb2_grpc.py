# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import pb.auth_pb2 as auth__pb2

GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in auth_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class AuthServiceStub(object):
    """The authentication service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendOtp = channel.unary_unary(
                '/auth.AuthService/SendOtp',
                request_serializer=auth__pb2.SendOtpRequest.SerializeToString,
                response_deserializer=auth__pb2.NoTokenResponse.FromString,
                _registered_method=True)
        self.Register = channel.unary_unary(
                '/auth.AuthService/Register',
                request_serializer=auth__pb2.RegisterRequest.SerializeToString,
                response_deserializer=auth__pb2.TokenResponse.FromString,
                _registered_method=True)
        self.Login = channel.unary_unary(
                '/auth.AuthService/Login',
                request_serializer=auth__pb2.LoginRequest.SerializeToString,
                response_deserializer=auth__pb2.TokenResponse.FromString,
                _registered_method=True)
        self.Validate = channel.unary_unary(
                '/auth.AuthService/Validate',
                request_serializer=auth__pb2.ValidateRequest.SerializeToString,
                response_deserializer=auth__pb2.ValidateResponse.FromString,
                _registered_method=True)


class AuthServiceServicer(object):
    """The authentication service definition.
    """

    def SendOtp(self, request, context):
        """Send an OTP for login with a phone number.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Register(self, request, context):
        """Registers a user with a phone number.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Login(self, request, context):
        """Logs in a user with a phone number and OTP.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Validate(self, request, context):
        """Verify and validate a token
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendOtp': grpc.unary_unary_rpc_method_handler(
                    servicer.SendOtp,
                    request_deserializer=auth__pb2.SendOtpRequest.FromString,
                    response_serializer=auth__pb2.NoTokenResponse.SerializeToString,
            ),
            'Register': grpc.unary_unary_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=auth__pb2.RegisterRequest.FromString,
                    response_serializer=auth__pb2.TokenResponse.SerializeToString,
            ),
            'Login': grpc.unary_unary_rpc_method_handler(
                    servicer.Login,
                    request_deserializer=auth__pb2.LoginRequest.FromString,
                    response_serializer=auth__pb2.TokenResponse.SerializeToString,
            ),
            'Validate': grpc.unary_unary_rpc_method_handler(
                    servicer.Validate,
                    request_deserializer=auth__pb2.ValidateRequest.FromString,
                    response_serializer=auth__pb2.ValidateResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'auth.AuthService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('auth.AuthService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class AuthService(object):
    """The authentication service definition.
    """

    @staticmethod
    def SendOtp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/auth.AuthService/SendOtp',
            auth__pb2.SendOtpRequest.SerializeToString,
            auth__pb2.NoTokenResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/auth.AuthService/Register',
            auth__pb2.RegisterRequest.SerializeToString,
            auth__pb2.TokenResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Login(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/auth.AuthService/Login',
            auth__pb2.LoginRequest.SerializeToString,
            auth__pb2.TokenResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Validate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/auth.AuthService/Validate',
            auth__pb2.ValidateRequest.SerializeToString,
            auth__pb2.ValidateResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
