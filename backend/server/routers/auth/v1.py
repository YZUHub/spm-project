from fastapi import APIRouter


def router_factory() -> APIRouter:
    router = APIRouter(prefix="/v1/auth")

    @router.get("/check")
    async def health():
        return {"status": "ok"}

    return router
