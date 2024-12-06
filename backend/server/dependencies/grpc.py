import grpc
from fastapi import HTTPException, status
from google.protobuf.json_format import MessageToDict

from server.config import settings
from server.pb import auth_pb2, auth_pb2_grpc
from server.schemas.requests.auth import LoginRequest, RegisterRequest


class AuthClient:
    def __init__(self):
        self.channel = grpc.insecure_channel(f"{settings.AUTH_GRPC_HOST}:{settings.AUTH_GRPC_PORT}")
        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

    def send_otp(self, phone_number: str) -> dict:
        response = self.stub.SendOtp(auth_pb2.SendOtpRequest(phone_number=phone_number))
        return MessageToDict(response)

    def register(self, payload: RegisterRequest) -> dict:
        response = self.stub.Register(auth_pb2.RegisterRequest(**payload.model_dump()))
        res = MessageToDict(response)
        if "success" in res and res["success"]:
            return res
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res["message"])

    def login(self, payload: LoginRequest) -> dict:
        response = self.stub.Login(auth_pb2.LoginRequest(**payload.model_dump()))
        res = MessageToDict(response)
        if "success" in res and res["success"]:
            return res
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res["message"])

    def validate(self, token: str) -> dict:
        response = self.stub.Validate(auth_pb2.ValidateRequest(token=token))
        return MessageToDict(response)
