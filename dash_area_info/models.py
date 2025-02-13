from sqlalchemy import Integer, String, DateTime, JSON
from sqlalchemy.orm import mapped_column
import common


class CultureZone(common.database.Base):
    __tablename__ = "culture_zones"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    zone = mapped_column(String(50), nullable=False)
    zoneid = mapped_column(String(10), nullable=False)
    zonename = mapped_column(String(10), nullable=True)
    lat = mapped_column(String(30), nullable=True)
    lon = mapped_column(String(30), nullable=True)
    radius = mapped_column(String(30), nullable=True)
    boundstartlat = mapped_column(String(30), nullable=True)
    boundstartlon = mapped_column(String(30), nullable=True)
    boundendlat = mapped_column(String(30), nullable=True)
    boundendlon = mapped_column(String(30), nullable=True)
    boundcolor = mapped_column(String(30), nullable=True)
    textlat = mapped_column(String(30), nullable=True)
    textlon = mapped_column(String(30), nullable=True)
    createdAt = mapped_column(DateTime)
    updatedAt = mapped_column(DateTime)


class CultureScanners(common.database.Base):
    __tablename__ = "culture_scanners"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    zone = mapped_column(String(50), nullable=False)
    region = mapped_column(String(10), nullable=True)
    zoneid = mapped_column(String(10), nullable=False)
    num = mapped_column(String(30), nullable=True)
    mac = mapped_column(String(20), nullable=True)
    intmac = mapped_column(String(20), nullable=True)
    status = mapped_column(String(20), nullable=True)
    type = mapped_column(String(20), nullable=True)
    lat = mapped_column(String(30), nullable=True)
    lon = mapped_column(String(30), nullable=True)
    createdAt = mapped_column(DateTime)
    updatedAt = mapped_column(DateTime)
    emplace_loc = mapped_column(String(100), nullable=True)
    scanner_color = mapped_column(String(10))


class CulturePolygon(common.database.Base):
    __tablename__ = "culture_polygon"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    zone = mapped_column(String(50), nullable=False)
    polygon = mapped_column(JSON)
    bound_color = mapped_column(String(10))
