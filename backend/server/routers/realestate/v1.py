from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from server.dependencies.auth import authenticate_user
from server.dependencies.grpc import RealestateClient, ValuationClient
from server.dependencies.requests import page_number


def router_factory() -> APIRouter:
    router = APIRouter(prefix="/v1/spm")

    @router.get("/properties")
    async def search_properties(
        client: Annotated[RealestateClient, Depends(RealestateClient)],
        page: Annotated[int | None, Depends(page_number)],
        min_area: Annotated[float | None, Query(ge=0)] = None,
        max_area: Annotated[float | None, Query(ge=0)] = None,
    ):
        if min_area is not None and max_area is not None:
            if min_area > max_area:
                return {"message": "min_area should be less than max_area"}

        data = client.search_properties(min_area=min_area, max_area=max_area, page=page)
        return data

    @router.get("/properties/me")
    async def get_owned_properties(
        client: Annotated[RealestateClient, Depends(RealestateClient)],
        page: Annotated[int | None, Depends(page_number)],
        phone_number: Annotated[str, Depends(authenticate_user)],
    ):
        data = client.get_owned_properties(owner_id=phone_number, page=page)
        return data

    @router.get("/properties/me/count")
    async def count_owned_properties(
        client: Annotated[RealestateClient, Depends(RealestateClient)],
        phone_number: Annotated[str, Depends(authenticate_user)],
    ):
        data = client.count_owned_properties(owner_id=phone_number)
        return data

    @router.get("/properties/count")
    async def count_properties(
        client: Annotated[RealestateClient, Depends(RealestateClient)],
        min_area: Annotated[float | None, Query(ge=0)] = None,
        max_area: Annotated[float | None, Query(ge=0)] = None,
    ):
        if min_area is not None and max_area is not None:
            if min_area > max_area:
                return {"message": "min_area should be less than max_area"}

        data = client.count_properties(min_area=min_area, max_area=max_area)
        return data

    @router.get("/properties/{property_id_nma}")
    async def get_property(
        client: Annotated[RealestateClient, Depends(RealestateClient)], property_id_nma: str
    ):
        data = client.get_property(property_id_nma=property_id_nma)
        return data

    @router.get("/properties/{property_id_nma}/units")
    async def get_property_units(
        client: Annotated[RealestateClient, Depends(RealestateClient)],
        property_id_nma: str,
        page: Annotated[int | None, Depends(page_number)],
    ):
        data = client.get_property_units(property_id_nma=property_id_nma, page=page)
        return data

    @router.get("/properties/{property_id_nma}/units/count")
    async def count_property_units(
        client: Annotated[RealestateClient, Depends(RealestateClient)], property_id_nma: str
    ):
        data = client.count_property_units(property_id_nma=property_id_nma)
        return data

    @router.get("/units/{unit_id}")
    async def get_unit(client: Annotated[RealestateClient, Depends(RealestateClient)], unit_id: int):
        data = client.get_unit(unit_id=unit_id)
        return data

    @router.get("/units/{unit_id}/valuations", dependencies=[Depends(authenticate_user)])
    async def get_valuations(
        unit_id: int,
        date: Annotated[date | None, Query()],
        client: Annotated[RealestateClient, Depends(RealestateClient)],
        valuation_client: Annotated[ValuationClient, Depends(ValuationClient)],
    ):
        historic_data = client.get_historic_valuations(unit_id=unit_id)
        future_data = valuation_client.get_unit_valuation(unit_id=unit_id, date=date)
        return {"historic_data": historic_data, "future_data": future_data}

    return router
