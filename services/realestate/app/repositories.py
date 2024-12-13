from beanie.operators import In

import schemas
from models import Owner, Property, Unit
from pb.properties_pb2 import RangeQuery


async def read_single_property(property_id_nma: str) -> schemas.PropertyDetail:
    property = await Property.find(Property.property_id_nma == property_id_nma, fetch_links=True).project(schemas.Property).first_or_none()
    return property


async def search_properties(area: RangeQuery, page: int) -> list[schemas.Property]:
    match_query = {"geometry.coordinates.0": {"$gte": 10.65, "$lte": 10.85}, "geometry.coordinates.1": {"$gte": 59.95, "$lte": 59.97}}

    if area.min or area.max:
        match_query["area"] = {}
        if area.min:
            match_query["area"]["$gte"] = area.min
        if area.max:
            match_query["area"]["$lte"] = area.max

    properties = await Property.find(match_query).project(schemas.Property).skip((page - 1) * 20).limit(20).to_list()
    return properties


async def count_properties(area: RangeQuery, page: int) -> int:
    match_query = {"geometry.coordinates.0": {"$gte": 10.65, "$lte": 10.85}, "geometry.coordinates.1": {"$gte": 59.95, "$lte": 59.97}}

    if area.min or area.max:
        match_query["area"] = {}
        if area.min:
            match_query["area"]["$gte"] = area.min
        if area.max:
            match_query["area"]["$lte"] = area.max

    properties = await Property.find(match_query).count()
    return properties


async def read_single_unit(unit_id: int) -> schemas.Unit:
    unit = await Unit.find(Unit.unit_id == unit_id).project(schemas.Unit).first_or_none()
    return unit


async def read_property_units(property_id_nma: str, page: int | None = None) -> list[schemas.Unit]:
    query = {
        "geometry.coordinates.0": {"$gte": 10.65, "$lte": 10.85},
        "geometry.coordinates.1": {"$gte": 59.95, "$lte": 59.97},
    }

    if page:
        query["property_id_nma"] = property_id_nma
        return await Unit.find(query).project(schemas.Unit).skip((page - 1) * 20).limit(20).to_list()
    else:
        query["property_id_nma_main"] = property_id_nma
        return await Unit.find(query).project(schemas.Unit).skip((page - 1) * 20).limit(20).to_list()


async def count_property_units(property_id_nma: str, page: int | None = None) -> int:
    query = {
        "geometry.coordinates.0": {"$gte": 10.65, "$lte": 10.85},
        "geometry.coordinates.1": {"$gte": 59.95, "$lte": 59.97},
    }

    if page:
        query["property_id_nma"] = property_id_nma
        return await Unit.find(query).count()
    else:
        query["property_id_nma_main"] = property_id_nma
        return await Unit.find(query).count()


async def get_owned_properties(owner_id: str, page: int) -> list[schemas.Property]:
    query = {
        "phone_number": owner_id,
        "geometry.coordinates.0": {"$gte": 10.65, "$lte": 10.85},
        "geometry.coordinates.1": {"$gte": 59.95, "$lte": 59.97},
    }

    owned_properties = await Owner.find(query).skip((page - 1) * 20).limit(20).to_list()
    properties = [item.property_id_nma for item in owned_properties]

    if properties:
        return await Property.find(In(Property.property_id_nma, properties)).project(schemas.Property).to_list()
    else:
        return []


async def count_owned_properties(owner_id: str) -> int:
    query = {
        "phone_number": owner_id,
        "geometry.coordinates.0": {"$gte": 10.65, "$lte": 10.85},
        "geometry.coordinates.1": {"$gte": 59.95, "$lte": 59.97},
    }
    owned_properties = await Owner.find(query).count()
    return owned_properties
