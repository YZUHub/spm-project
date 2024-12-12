import schemas
from models import Property, Unit
from pb.properties_pb2 import RangeQuery


async def read_single_property(property_id_nma: str) -> schemas.Property:
    property = await Property.find(Property.property_id_nma == property_id_nma, fetch_links=True).project(schemas.Property).first_or_none()
    return property


async def search_properties(area: RangeQuery, page: int) -> list[schemas.Property]:
    match_query = {}

    if area.min or area.max:
        match_query["area"] = {}
        if area.min:
            match_query["area"]["$gte"] = area.min
        if area.max:
            match_query["area"]["$lte"] = area.max

    properties = await Property.find(match_query, fetch_links=True).project(schemas.Property).skip(page * 10).limit(10).to_list()
    return properties


async def read_single_unit(unit_id: int) -> schemas.Unit:
    unit = await Unit.find(Unit.unit_id == unit_id).project(schemas.Unit).first_or_none()
    return unit


async def read_property_units(property_id_nma: str) -> list[schemas.Unit]:
    units = await Unit.find(Unit.property_id_nma == property_id_nma).project(schemas.Unit).to_list()
    return units
