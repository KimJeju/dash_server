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
                TOY_API_SERVER
                + f"/DeviceResidenceTime?from={date_from}&date_to={date_to}"
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


async def sensor_data_hourly_util():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(TOY_API_SERVER + f"/sensorDataHourly")
            data = response.json()
            df = sort_value_use_key(data, "time")
            df = to_dict_data(df)
            return df.to_dict()
    except Exception:
        print("URL 또는 파라미터를 확인하세요")


async def sensor_data_day_average_util(date_from: str, date_to: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                TOY_API_SERVER + f"/SensorDataDayAverage?from={date_from}&to={date_to}"
            )
            data = response.json()
            df = sort_value_use_key(data, "time")
            df = to_dict_data(df)
            return df.to_dict()
    except Exception:
        print("URL 또는 파라미터를 확인하세요")


async def device_count_monthly_util():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(TOY_API_SERVER + f"/DeviceCountMonthly")
            data = response.json()
            df = sort_value_use_key(data, "time")
            df = to_dict_data(df)
            return df.to_dict()
    except Exception:
        print("URL 또는 파라미터를 확인하세요")


async def hour_move_util(date_from: str, date_to: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                TOY_API_SERVER + f"/HourMove?from={date_from}&to={date_to}"
            )
            data = response.json()
            df = sort_value_use_key(data, "time")
            df = to_dict_data(df)
            return df.to_dict()
    except Exception:
        print("URL 또는 파라미터를 확인하세요")


async def day_move_util(date_from: str, date_to: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                TOY_API_SERVER + f"/DayMove?from={date_from}&to={date_to}"
            )
            data = response.json()
            df = sort_value_use_key(data, "time")
            df = to_dict_data(df)
            return df.to_dict()
    except Exception:
        print("URL 또는 파라미터를 확인하세요")


# async def week_move_util(date_from:str, date_to:str):
#         try:
#                 async with httpx.AsyncClient() as client:
#                         response = await client.get(TOY_API_SERVER + f'/WeekMove?from={date_from}&to={date_to}')
#                         data = response.json()
#                         df = sort_value_use_key(data, 'time')
#                         df = to_dict_data(df)
#                         return df.to_dict()
#         except Exception:
#                 print("URL 또는 파라미터를 확인하세요")


async def month_move_util(date_from: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(TOY_API_SERVER + f"/MonthMove?from={date_from}")
            data = response.json()
            df = sort_value_use_key(data, "time")
            df = to_dict_data(df)
            return df.to_dict()
    except Exception:
        print("URL 또는 파라미터를 확인하세요")


async def month_statistics_util(year: str, month: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                TOY_API_SERVER + f"/MonthStatistics?year={year}&month={month}"
            )
            data = response.json()
            df = sort_value_use_key(data, "time")
            df = to_dict_data(df)
            return df.to_dict()
    except Exception:
        print("URL 또는 파라미터를 확인하세요")


async def density_day_hour_util(date_from: str, date_to: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                TOY_API_SERVER + f"/DensityDayHour?from={date_from}&to={date_to}"
            )
            data = response.json()
            df = sort_value_use_key(data, "time")
            df = to_dict_data(df)
            return df.to_dict()
    except Exception:
        print("URL 또는 파라미터를 확인하세요")


async def device_count_day_hour_util(date_from: str, date_to: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                TOY_API_SERVER + f"/DeviceCountDayHour?from={date_from}&to={date_to}"
            )
            data = response.json()
            df = sort_value_use_key(data, "time")
            df = to_dict_data(df)
            return df.to_dict()
    except Exception:
        print("URL 또는 파라미터를 확인하세요")


# def get_questions(db:Session):
#     return db.query(models.QuestionList).all()


# def insert_question(db: Session, question: schema.QuestionCreate):
#     # create_at을 명시적으로 지정하지 않아도 데이터베이스에서 처리되도록 할 수 있습니다.
#     new_question = models.QuestionList(**question.dict())  # dict()로 데이터 변환 후 모델에 전달

#     # 새로운 질문을 세션에 추가
#     db.add(new_question)

#     # 트랜잭션 커밋
#     db.commit()

#     # 추가된 객체를 새로고침하여 데이터베이스에서 생성된 값을 반영 (예: ID)
#     db.refresh(new_question)

#     return new_question
