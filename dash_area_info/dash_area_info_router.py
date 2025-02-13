import os
import pandas as pd
import numpy as np
import common
import json
from . import utils
from common import verify_header
from .objects import AvgTotal
from sqlalchemy.orm import Session
from datetime import date, timedelta, datetime
from fastapi import Depends, APIRouter, HTTPException, Query
from .models import CultureScanners, CultureZone, CulturePolygon

router = APIRouter(prefix="/api/dash_area_info")

today = date.today()
one_week_ago = today - timedelta(7)
this_month_first = datetime(today.year, today.month, 1)


@router.get(
    "/get_all_culture_zones", tags=["DASH AREA INFO"], dependencies=[verify_header()]
)
async def get_all_culture_zones(db: Session = Depends(common.get_db)):
    try:
        return db.query(CultureZone).all()
    except Exception as e:
        print(e)


@router.get(
    "/get_all_culture_scanners", tags=["DASH AREA INFO"], dependencies=[verify_header()]
)
async def get_all_culture_scanners(db: Session = Depends(common.get_db)):
    try:
        return db.query(CultureScanners).all()
    except Exception as e:
        print(e)


@router.get(
    "/get_all_culture_polygon", tags=["DASH AREA INFO"], dependencies=[verify_header()]
)
async def get_all_culture_zones(db: Session = Depends(common.get_db)):
    try:
        return db.query(CulturePolygon).all()
    except Exception as e:
        print(e)


@router.get(
    "/get_region_cuurent_people",
    tags=["DASH AREA INFO"],
    dependencies=[verify_header()],
)
async def get_region_current_people(
    zones: list[str] = Query(
        ["연오랑세오녀 테마공원(귀비고)", "스페이스워크(환호공원)", "해상스카이워크"]
    ),
):
    try:
        current_df = await utils.device_count_hourly_util("10m")
        current_filter = current_df[current_df["zone"].isin(zones)]
        current_df = current_filter.drop_duplicates("zone", keep="last")
        current_df = current_df.groupby(by="zone").sum()
        current_df = current_df.drop("time", axis=1)
        df_json = current_df.to_json(orient="columns")

        return json.loads(df_json)
    except Exception as e:
        print(e)


@router.get(
    "/get_region_visitor_transition",
    tags=["DASH AREA INFO"],
    dependencies=[verify_header()],
)
async def get_region_visitor_transition(
    zones: list[str] = Query(
        ["연오랑세오녀 테마공원(귀비고)", "스페이스워크(환호공원)", "해상스카이워크"]
    ),
):
    try:
        visitor_df = await utils.device_count_day_util(
            date_from=one_week_ago, date_to=today
        )
        visitor_filter = visitor_df[visitor_df["zone"].isin(zones)]
        sum_transition = visitor_filter.groupby(by="time").sum()

        transition_visitor = sum_transition.drop("zone", axis=1)

        df_json = transition_visitor.to_json(orient="columns")
        return json.loads(df_json)
    except Exception as e:
        print(e)


@router.get(
    "/get_region_revisitor_transition",
    tags=["DASH AREA INFO"],
    dependencies=[verify_header()],
)
async def get_region_revisitor_transition(
    zones: list[str] = Query(
        ["연오랑세오녀 테마공원(귀비고)", "스페이스워크(환호공원)", "해상스카이워크"]
    ),
):
    try:
        revisitor_df = await utils.device_count_revisit_util(
            date_from=one_week_ago, date_to=today
        )
        revisitor_filter = revisitor_df[revisitor_df["zone"].isin(zones)]

        sum_transition = revisitor_filter.groupby(by="time").sum()

        transition_visitor = sum_transition.drop("zone", axis=1)

        df_json = transition_visitor.to_json(orient="columns")
        return json.loads(df_json)
    except Exception as e:
        print(e)


# 금년 전체 통계를 위한 API 입니다.
# 자세한 사항은 iP/docs 확인
@router.get("/area_total_avg", tags=["DASH AREA INFO"], dependencies=[verify_header()])
async def area_total_avg(find_key: str = "포항관광지 전체"):
    try:
        # 현재 체류 인원 전처리
        now_people_all = await utils.device_count_hourly_util(params="1d")
        now_people_all = now_people_all.drop_duplicates("zone", keep="first")
        now_people_condition = now_people_all["zone"] == find_key  # 키에 따른 값 추출
        now_people = now_people_all.loc[now_people_condition]  # 필요한 값 추출

        # 금일 방문자 전처리
        today_visitor_all = await utils.device_count_hourly_util(params="1d-1h")
        today_visitor_condition = (
            today_visitor_all["zone"] == find_key
        )  # 키에 따른 값 추출
        today_visitor = today_visitor_all.loc[today_visitor_condition]  # 필요한 값 추출
        today_total_visitor = np.sum(today_visitor["data"].values)  # 데이터 합산

        # 금월 방문자 전처리
        this_month_visitor_all = await utils.device_count_day_util(
            date_from=this_month_first.strftime("%Y-%m-%d"), date_to=today
        )
        this_month_condition = this_month_visitor_all["zone"] == find_key
        this_month_visitor_extract = this_month_visitor_all.loc[this_month_condition]
        this_month_total_visitor = np.sum(this_month_visitor_extract["data"], axis=0)

        area_total_avg = AvgTotal(
            nowPeople=int(now_people["data"]),
            today=int(today_total_visitor),
            month=int(this_month_total_visitor),
        )

        return area_total_avg
    except HTTPException as e:
        print(e)


# 차트 관련 API 입니다.
@router.get(
    "/area_subtotal_list", tags=["DASH AREA INFO"], dependencies=[verify_header()]
)
async def area_subtotal_list(
    zones: list[str] = Query(
        ["연오랑세오녀 테마공원(귀비고)", "스페이스워크(환호공원)", "해상스카이워크"]
    ),
    date_from: date = date.today(),
):

    avg_chart_list = common.AvgChartList()

    try:

        total_now_people = 0  # 현재 체류인원 총합을 저장할 변수
        total_today_people = 0  # 오늘 인원 총합을 저장할 변수
        total_month_people = 0  # 오늘 인원 총합을 저장할 변수

        now_people_all_origin = await utils.device_count_hourly_util(params="1h")
        today_visitor_all_origin = await utils.device_count_hourly_util(params="1d-1h")
        residence_time_origin = await utils.device_residence_time_util(
            date_from=today - timedelta(1), date_to=today
        )
        yester_day_visitor_all_origin = await utils.device_count_revisit_util(
            date_from=date_from - timedelta(1), date_to=today
        )
        this_month_visitor_all_origin = await utils.device_count_day_util(
            date_from=this_month_first, date_to=today
        )
        for zone in zones:
            now_people_all = now_people_all_origin
            today_visitor_all = today_visitor_all_origin
            residence_time = residence_time_origin
            yester_day_visitor_all = yester_day_visitor_all_origin
            this_month_visitor_all = this_month_visitor_all_origin

            today_total_visitor_dict = {}
            residence_time_dict = {}
            yesterday_visitor_dict = {}
            # 체류 인원

            now_people_all = now_people_all.drop_duplicates("zone", keep="first")
            now_people_condition = now_people_all["zone"] == zone
            now_people = now_people_all.loc[now_people_condition]
            now_people_value = int(now_people["data"])
            # #총합을 위해 다 더해주고
            total_now_people += now_people_value
            # now_people_dict["total"] = total_now_people

            # 금일 현재시간까지 방문자 전처리
            today_visitor_condition = (
                today_visitor_all["zone"] == zone
            )  # 현재 zone에 해당하는 데이터 필터링
            today_visitor = today_visitor_all.loc[
                today_visitor_condition
            ]  # 필터링된 데이터 가져오기
            today_total_visitor = today_visitor["data"].sum()  # 합산
            today_total_visitor_dict[zone] = int(
                today_total_visitor
            )  # numpy타입때문에 int가 필요
            # numpy.int64는 파이썬의 기본int랑 다른 타입이다 json으로 직렬화 할때 TypeError를 막기위해 int필요

            total_today_people += today_total_visitor  # 오늘 방문객 총합에 더하기
            today_total_visitor_dict["total"] = int(total_today_people)

            # 평균 체류 시간
            residence_time_condition = residence_time["zone"] == zone
            residence_time_extract = residence_time[residence_time_condition]
            residence_time = residence_time_extract["data"].values / 60
            residence_time_dict[zone] = int(residence_time)

            # 전일 방문자 전처리
            yester_day_condition = yester_day_visitor_all["zone"] == zone
            yester_day_visitor_extract = yester_day_visitor_all[yester_day_condition]
            yester_day_visitor_extract = yester_day_visitor_extract.drop_duplicates(
                "zone", keep="first"
            )
            yesterday_visitor_dict[zone] = int(
                yester_day_visitor_extract["data"].values
            )

            # # 금월
            this_month_condition = this_month_visitor_all["zone"] == zone
            this_month_visitor_extract = this_month_visitor_all.loc[
                this_month_condition
            ]
            this_month_total_visitor = np.sum(
                this_month_visitor_extract["data"], axis=0
            )
            # 총합을 위해 다 더해주고고
            total_month_people += int(this_month_total_visitor)

            avg_value = common.AvgTotal(
                nowPeople=0,
                today=int(today_total_visitor),
                revisitor=int(yester_day_visitor_extract["data"].values),
                month=0,
                year=0,
                residence=int(residence_time),
            )
            result_data = common.AvgChart(target=zone, chartData=avg_value)
            avg_chart_list.appendData(result_data.getTargetDict())

        avg_total_value = common.AvgTotal(
            nowPeople=int(total_now_people),  # 현재 체류인원 총합을 저장할 변수
            today=int(total_today_people),  # 오늘 인원 총합을 저장할 변수
            month=int(total_month_people),
            residence=0,
            revisitor=0,
            year=0,
        )
        result_total_data = common.AvgChart(
            target="권역별 방문객", chartData=avg_total_value
        )
        avg_chart_list.appendData(result_total_data.getTargetDict())

        return avg_chart_list.getDataList()
    except HTTPException as e:
        print(e)
