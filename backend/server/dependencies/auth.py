from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from server.dependencies.grpc import AuthClient


async def authenticate_user(
    client: Annotated[AuthClient, Depends(AuthClient)],
    authorization: Annotated[str, Header(alias="Authorization")],
):
    try:
        print(f"Authenticating user with token: {authorization}")
        if not authorization:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No token found")
        res = client.validate(authorization)
        if "permissions" not in res:
            raise Exception("No permissions found")
        return res
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
