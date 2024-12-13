import asyncio
import logging
from concurrent import futures

from beanie import init_beanie
from grpc.experimental import aio
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from models import Building, Floor, Owner, Property, Unit
from pb.properties_pb2_grpc import add_PropertyServiceServicer_to_server
from services import PropertyService


async def serve():
    client = AsyncIOMotorClient(settings.DB_URI)
    await init_beanie(client["SPM"], document_models=[Building, Floor, Owner, Property, Unit])

    server = aio.server(futures.ThreadPoolExecutor(max_workers=10))

    add_PropertyServiceServicer_to_server(PropertyService(), server)

    server.add_insecure_port(f"[::]:{settings.PORT}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    logging.info("Starting server")
    print(f"Server running on port {settings.PORT}")
    asyncio.run(serve())
