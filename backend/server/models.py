from datetime import datetime, timezone
from typing import Annotated, Union

import pymongo
from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field


class BaseDocument(Document):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The date and time of the document creation",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The date and time of the document update",
    )

    class Settings:
        use_cache = True
        use_revision = True
        use_state_management = True
        validation_on_save = True

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.Settings.name = f"{cls.__name__.lower()}s"


class PointGeometry(BaseModel):
    type: str = "Point"
    coordinates: list[float]


class Owner(BaseDocument):
    property_id: int
    property_id_nma: Annotated[str, Indexed()]
    name: Annotated[str, Indexed(index_type=pymongo.TEXT)]
    full_address: str
    phone_number: Annotated[str, Indexed()]
    geometry: Annotated[PointGeometry, Indexed(index_type=pymongo.GEOSPHERE)]


class Floor(BaseDocument):
    building_id: int
    floor_id: int
    floor_code_id: int
    floor_number: int
    units_home: int
    ufs_home: float
    ufs_other: float
    ufs_total: float
    alternative_area: int
    alternative_area_2: int
    gba_home: float
    gba_other: float
    gba_total: float
    floor_code_name: Union[str, None]
    floor_code_value: str


class Building(BaseDocument):
    property_id: int
    property_id_nma: Annotated[str, Indexed()]
    building_id: Annotated[int, Indexed()]
    building_number: str
    address: Union[str, None]
    has_sefrak_artifact: bool
    has_cultural_artifact: bool
    has_elevator: bool
    units_home: int
    built_area: float
    gba_total: float
    ufs_total: float
    building_status_code_name: str
    industry_group_code_name: Union[str, None]
    industry_group_code_value: Union[str, None]
    building_type_code_name: Union[str, None]
    building_type_code_value: Union[float, None]
    building_change_code_name: Union[str, None]
    energy_grade: Union[str, None]
    heating_grade: Union[str, None]
    floors: Union[int, None]
    serial_number: int
    city_name: Annotated[str, Indexed(index_type=pymongo.TEXT)]
    cultural_artifact_id: Union[int, None]
    locality_number: Union[int, None]
    cultural_monument_number: Union[str, None]
    geometry: Annotated[PointGeometry, Indexed(index_type=pymongo.GEOSPHERE)]
    floor_data: list[Link[Floor]]


class Property(BaseDocument):
    property_id: int
    property_id_nma: Annotated[str, Indexed()]
    established_date: str
    number_of_buildings: int
    number_of_addresses: int
    number_of_sections: int
    number_of_leases: int
    number_of_owners: int
    number_of_plots: int
    parking_garage: bool
    area: float
    postal_number: int
    postal_location: str
    city_name: Annotated[str, Indexed(index_type=pymongo.TEXT)]
    city_district_id: int
    city_district_name: str
    geometry: Annotated[PointGeometry, Indexed(index_type=pymongo.GEOSPHERE)]
    buildings: list[Link[Building]]
    owners: list[Link[Owner]]
