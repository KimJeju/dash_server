from pydantic import BaseModel
import datetime


class CultureZoneBase(BaseModel):
    zone: str
    zoneid: str
    zonename: str
    lat: str
    lon: str
    radius: str
    boundstartlat: str
    boundstartlon: str
    boundendlat: str
    boundendlon: str
    boundcolor: str
    textlat: str
    textlon: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime

    class Config:
        from_attributes = True


class CultureZoneCreate(CultureZoneBase):
    pass


class CultureZone(CultureZoneBase):
    id: int

    class Config:
        from_attributes = True


class CultureScannersBase(BaseModel):
    zone: str
    region: str
    zoneid: str
    num: str
    mac: str
    intmac: str
    status: str
    type: str
    lat: str
    lon: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    emplace_loc: str

    class Config:
        orm_mode = True


class CultureScanners(CultureScannersBase):
    id: int

    class Config:
        from_attributes = True
