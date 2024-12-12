import json

import joblib

from etl import convert_data
from pb.valuation_pb2_grpc import ValuationServiceServicer
from pb.valuation_pb2 import ValuationResponse
from realestate import RealestateClient


class ValuationService(ValuationServiceServicer):
    def __init__(self):
        super().__init__()
        self.model = joblib.load("models/valuation.pkl")
        self.features = ["floor_number", "floors", "bta", "bra", "prom", "rooms", "bedrooms", "bathrooms", "wcs", "nearest_train_station_distance", "nearest_bus_station_distance", "nearest_ferry_terminal_distance", "nearest_tram_station_distance", "nearest_underground_station_distance", "nearest_airport_distance", "nearest_kindergartens_distance", "nearest_elementary_middle_school_distance", "nearest_high_school_distance", "nearest_fire_station_distance", "in_beach_zone", "lat", "lon", "year", "month"]

    async def GetPropertyValuation(self, request, context) -> ValuationResponse:
        client = RealestateClient()
        units = client.get_property_units(request.property_id_nma)
        X = convert_data(units, request.date)
        y = self.model.predict(X[self.features])
        X["index"] = y
        return ValuationResponse(valuations=json.dumps(X[["unit_id", "year", "month", "index"]].to_dict(orient="records")))

    async def GetUnitValuation(self, request, context) -> ValuationResponse:
        client = RealestateClient()
        unit = client.get_unit(request.unit_id)
        X = convert_data([unit], request.date)
        y = self.model.predict(X[self.features])
        X["index"] = y
        return ValuationResponse(valuations=json.dumps(X[["unit_id", "year", "month", "index"]].to_dict(orient="records")))
