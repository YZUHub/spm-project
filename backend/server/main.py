from fastapi import FastAPI

from server.events.startup import app_lifespan


def app():
    api = FastAPI(lifespan=app_lifespan)
    return api
