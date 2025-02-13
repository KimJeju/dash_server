import os
import httpx
import pandas as pd
from fastapi import HTTPException
from common.common_utils import to_dict_data, sort_value_use_key

TOY_API_SERVER = os.getenv("TOY_API_SERVER")


async def device_count_hourly_util(params: str):
    print(TOY_API_SERVER)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                TOY_API_SERVER + f"/DeviceCountHourly?unit={params}"
            )
            data = response.json()
            df = pd.DataFrame(data)
            return df
    except HTTPException as e:
        print(e + " " + "device_count_hourly_util")


async def device_residence_time_util(date_from: str, date_to: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                TOY_API_SERVER + f"/DeviceResidenceTime?from={date_from}&to={date_to}"
            )
            data = response.json()
            df = pd.DataFrame(data)
            return df
    except HTTPException as e:
        print(e + " " + "device_residence_time_util")


async def device_count_day_util(date_from: str, date_to: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                TOY_API_SERVER + f"/DeviceCountDay?from={date_from}&to={date_to}"
            )
            data = response.json()
            df = pd.DataFrame(data)
            return df
    except HTTPException as e:
        print(e + " " + "device_count_day_util")


async def device_count_revisit_util(date_from: str, date_to: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                TOY_API_SERVER + f"/DeviceCountRevisit?from={date_from}&to={date_to}"
            )
            data = response.json()
            df = pd.DataFrame(data)
            return df
    except HTTPException as e:
        print(e + " " + "device_count_revisit_util")


# async def device_count_day_hour_util(date_from: str, date_to: str):
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(
#                 TOY_API_SERVER + f"/DeviceCountDayHour?from={date_from}&to={date_to}"
#             )
#             data = response.json()
#             df = sort_value_use_key(data, "time")
#             df = to_dict_data(df)
#             return df.to_dict()
#     except Exception:
#         print("URL 또는 파라미터를 확인하세요")


async def device_count_monthly_util(date_from: str, date_to: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                TOY_API_SERVER + f"/DeviceCountMonthly?from={date_from}&to={date_to}"
            )
            data = response.json()
            df = pd.DataFrame(data)

            return df
    except Exception:
        print("URL 또는 파라미터를 확인하세요")
