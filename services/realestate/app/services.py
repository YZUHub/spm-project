import json

import grpc

from pb.properties_pb2 import Response
from pb.properties_pb2_grpc import PropertyServiceServicer
from repositories import count_properties, count_property_units, read_property_units, read_single_property, read_single_unit, search_properties


class PropertyService(PropertyServiceServicer):
    async def SearchProperties(self, request, context) -> Response:
        properties = await search_properties(area=request.area, page=request.page)

        data = []
        for property in properties:
            data.append(property.model_dump(exclude_none=True))

        return Response(data=json.dumps(data))

    async def CountProperties(self, request, context):
        data = await count_properties(area=request.area, page=request.page)
        return Response(data=json.dumps({"count": data}))

    async def GetProperty(self, request, context) -> Response:
        property_id_nma = request.property_id_nma
        property = await read_single_property(property_id_nma)

        if not property:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Property not found")
            return Response()

        property_data = property.model_dump_json(exclude_none=True)
        return Response(data=property_data)

    async def GetPropertyUnits(self, request, context) -> Response:
        property_id_nma = request.property_id_nma
        units = await read_property_units(property_id_nma, request.page)

        data = []
        for unit in units:
            data.append(unit.model_dump(exclude_none=True))

        return Response(data=json.dumps(data))

    async def CountPropertyUnits(self, request, context):
        data = await count_property_units(property_id_nma=request.property_id_nma)
        return Response(data=json.dumps({"count": data}))

    async def GetUnit(self, request, context) -> Response:
        unit_id = request.unit_id
        unit = await read_single_unit(unit_id)

        if not unit:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Unit not found")
            return Response()

        unit_data = unit.model_dump_json(exclude_none=True)
        return Response(data=unit_data)
