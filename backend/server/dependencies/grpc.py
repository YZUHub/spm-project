import json

import grpc
from fastapi import HTTPException, status
from google.protobuf.json_format import MessageToDict

from server.config import settings
from server.pb import ads_pb2, ads_pb2_grpc, auth_pb2, auth_pb2_grpc, properties_pb2, properties_pb2_grpc
from server.schemas.requests.auth import LoginRequest, RegisterRequest


class AuthClient:
    def __init__(self):
        self.channel = grpc.insecure_channel(f"{settings.AUTH_SERVICE_HOST}:{settings.AUTH_SERVICE_PORT}")
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


class RealestateClient:
    def __init__(self):
        self.properties_channel = grpc.insecure_channel(f"{settings.REALESTATE_SERVICE_HOST}:{settings.REALESTATE_SERVICE_PORT}")
        self.properties_stub = properties_pb2_grpc.PropertyServiceStub(self.properties_channel)

        self.ads_channel = grpc.insecure_channel(f"{settings.REALESTATE_SERVICE_HOST}:{settings.REALESTATE_SERVICE_PORT}")
        self.ads_stub = ads_pb2_grpc.AdServiceStub(self.ads_channel)

    def search_properties(self, min_area: float | None, max_area: float | None, page: int = 1) -> dict:
        payload = {"area": {"min": min_area, "max": max_area}, "page": page}
        response = self.properties_stub.SearchProperties(properties_pb2.FilterPropertyRequest(**payload))
        return json.loads(response.data)

    def count_properties(self, min_area: float | None, max_area: float | None) -> dict:
        payload = {"area": {"min": min_area, "max": max_area}}
        response = self.properties_stub.CountProperties(properties_pb2.FilterPropertyRequest(**payload))
        return json.loads(response.data)

    def get_property(self, property_id_nma: str) -> dict:
        payload = {"property_id_nma": property_id_nma}
        response = self.properties_stub.GetProperty(properties_pb2.SinglePropertyRequest(**payload))
        return json.loads(response.data)

    def get_property_units(self, property_id_nma: str, page: int = 1) -> dict:
        payload = {"property_id_nma": property_id_nma, "page": page}
        response = self.properties_stub.GetPropertyUnits(properties_pb2.PropertyUnitsRequest(**payload))
        return json.loads(response.data)

    def count_property_units(self, property_id_nma: str) -> dict:
        payload = {"property_id_nma": property_id_nma}
        response = self.properties_stub.CountPropertyUnits(properties_pb2.PropertyUnitsRequest(**payload))
        return json.loads(response.data)

    def get_unit(self, unit_id: str) -> dict:
        payload = {"unit_id": unit_id}
        response = self.properties_stub.GetUnit(properties_pb2.SingleUnitRequest(**payload))
        return json.loads(response.data)

    def get_owned_properties(self, owner_id: str, page: int = 1) -> dict:
        payload = {"owner_id": owner_id, "page": page}
        response = self.properties_stub.GetOwnedProperties(properties_pb2.OwnedItemsRequest(**payload))
        return json.loads(response.data)

    def count_owned_properties(self, owner_id: str) -> dict:
        payload = {"owner_id": owner_id}
        response = self.properties_stub.CountOwnedProperties(properties_pb2.OwnedItemsRequest(**payload))
        return json.loads(response.data)
