from auth import create_token, decode_token
from pb.auth_pb2 import NoTokenResponse, TokenResponse, ValidateResponse
from pb.auth_pb2_grpc import AuthServiceServicer
from repositories import create_account, read_accout_by_phone_number
from utils import validate_otp


class AuthService(AuthServiceServicer):
    async def SendOtp(self, request, context):
        try:
            await read_accout_by_phone_number(request.phone_number)
            return NoTokenResponse(success=True, message="Verify OTP")
        except ValueError:
            return NoTokenResponse(success=False, message="Phone number already exists")

    async def Register(self, request, context):
        try:
            if validate_otp(request.otp):
                account = await create_account(request.phone_number, request.name)
                token = create_token(account)
                return TokenResponse(success=True, message="Account created", token=token)
            else:
                return NoTokenResponse(success=False, message="Invalid OTP")
        except ValueError:
            return NoTokenResponse(success=False, message="Phone number already exists")

    async def Login(self, request, context):
        account = await read_accout_by_phone_number(request.phone_number)
        if not account:
            return NoTokenResponse(success=False, message="Phone number does not exist")
        token = create_token(account)
        return TokenResponse(success=True, message="Logged in", token=token)

    async def Validate(self, request, context):
        try:
            decode_token(request.token)
            return ValidateResponse(permissions=["read", "write"])
        except Exception:
            return ValidateResponse(permissions=["read"])
