import os
import pandas as pd
import numpy as np
import json
from . import utils
import common
from common import verify_header
from typing import List, Optional
from sqlalchemy.orm import Session
from dateutil.relativedelta import *
from datetime import date, timedelta, datetime
from .objects import AvgTotal, AvgChart, AvgChartList
from fastapi import Depends, APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/total_analysis")

today = date.today()
this_month_first = datetime(today.year, today.month, 1)


# 금년 전체 통계를 위한 API 입니다.
# 자세한 사항은 iP/docs 확인
@router.get(
    "/current_average_total_value",
    tags=["TOTAL ANALYSIS"],
    dependencies=[verify_header()],
)
async def current_average_total_value(
    find_key: str = "포항관광지 전체", date_from: date = date.today()
):
    try:
        # 현재 체류 인원 전처리
        now_people_all = await utils.device_count_hourly_util(params="1d")
        now_people_all = now_people_all.drop_duplicates("zone", keep="first")
        now_people_condition = now_people_all["zone"] == find_key  # 키에 따른 값 추출
        now_people = now_people_all.loc[now_people_condition]  # 필요한 값 추출

        # 금일 현재시간까지 방문자 전처리
        today_visitor_all = await utils.device_count_hourly_util(params="1d-1h")
        today_visitor_condition = (
            today_visitor_all["zone"] == find_key
        )  # 키에 따른 값 추출
        today_visitor = today_visitor_all.loc[today_visitor_condition]  # 필요한 값 추출
        today_total_visitor = np.sum(today_visitor["data"].values)  # 데이터 합산

        # 전일 방문자 전처리
        yester_day_visitor_all = await utils.device_count_revisit_util(
            date_from=date_from - timedelta(1), date_to=today
        )
        yester_day_condition = yester_day_visitor_all["zone"] == find_key
        yester_day_visitor_extract = yester_day_visitor_all[yester_day_condition]
        yester_day_visitor_extract = yester_day_visitor_extract.drop_duplicates(
            "zone", keep="first"
        )

        # 금월 방문자 전처리
        this_month_visitor_all = await utils.device_count_day_util(
            date_from=this_month_first.strftime("%Y-%m-%d"), date_to=today
        )
        this_month_condition = this_month_visitor_all["zone"] == find_key
        this_month_visitor_extract = this_month_visitor_all.loc[this_month_condition]
        this_month_total_visitor = np.sum(this_month_visitor_extract["data"], axis=0)

        # 금년 방문자 전처리
        this_year_visitor_all = await utils.device_count_day_util(
            date_from="2025-01-01", date_to=today
        )
        this_year_condition = this_year_visitor_all["zone"] == find_key
        this_year_visitor_extract = this_year_visitor_all.loc[this_year_condition]
        this_year_total_visitor = np.sum(this_year_visitor_extract["data"], axis=0)

        # 평균 체류 시간
        residence_time = await utils.device_residence_time_util(
            date_from=today - timedelta(1), date_to=today
        )
        residence_time_condition = residence_time["zone"] == find_key
        residence_time_extract = residence_time[residence_time_condition]
        residence_time = residence_time_extract["data"].values / 60

        current_total_avg = AvgTotal(
            nowPeople=int(now_people["data"]),
            today=int(today_total_visitor),
            yesterday=int((yester_day_visitor_extract["data"])),
            month=int(this_month_total_visitor),
            year=int(this_year_total_visitor),
            time=int(residence_time),
            last_update=str(datetime.now()),
        )

        return current_total_avg
    except HTTPException as e:
        print(e)


@router.get(
    "/before_average_total_value",
    tags=["TOTAL ANALYSIS"],
    dependencies=[verify_header()],
)
async def before_average_total_value(
    find_key: str = "포항관광지 전체", date_from: date = date.today()
):
    # 지난달 첫일
    last_month_first = (
        datetime(today.year, today.month, 1) + relativedelta(months=-1)
    ).strftime("%Y-%m-%d")

    # 지난달 말일
    last_month_last = (
        datetime(today.year, today.month, 1) + relativedelta(seconds=-1)
    ).strftime("%Y-%m-%d")

    # 1년전
    ago_one_year = datetime(today.year, today.month, 1) + relativedelta(months=-12)

    try:
        # 전전일 방문자
        twodaysago_day_visitor_all = await utils.device_count_day_util(
            date_from=date_from - timedelta(3), date_to=today - timedelta(2)
        )
        twodaysago_day_condition = twodaysago_day_visitor_all["zone"] == find_key
        twodaysago_day_extract = twodaysago_day_visitor_all[twodaysago_day_condition]
        twodaysago_day_extract = twodaysago_day_extract.drop_duplicates(
            "zone", keep="first"
        )

        # 전월 방문자
        last_month_visitor_all = await utils.device_count_day_util(
            date_from=last_month_first,
            date_to=last_month_last,
        )
        last_month_condition = last_month_visitor_all["zone"] == find_key
        last_month_visitor_extract = last_month_visitor_all.loc[last_month_condition]
        last_month_total_visitor = np.sum(last_month_visitor_extract["data"], axis=0)

        # 전년 방문자 전처리 ( 오늘 날로 부터 1년전 )
        this_year_visitor_all = await utils.device_count_day_util(
            date_from=ago_one_year, date_to=last_month_last
        )
        this_year_condition = this_year_visitor_all["zone"] == find_key
        this_year_visitor_extract = this_year_visitor_all.loc[this_year_condition]
        this_year_total_visitor = np.sum(this_year_visitor_extract["data"], axis=0)

        # 전일평균 체류 시간
        residence_time = await utils.device_residence_time_util(
            date_from=today - timedelta(2), date_to=today - timedelta(1)
        )
        residence_time_condition = residence_time["zone"] == find_key
        residence_time_extract = residence_time[residence_time_condition]
        residence_time = residence_time_extract["data"].values / 60

        before_total_avg = AvgTotal(
            nowPeople=int(0),
            today=int(0),
            yesterday=int(twodaysago_day_extract["data"]),
            month=int(last_month_total_visitor),
            year=int(this_year_total_visitor),
            time=int(residence_time),
        )
        return before_total_avg
    except HTTPException as e:
        print(e)


# 차트 관련 API 입니다.
@router.get(
    "/zone_average_chart_value", tags=["TOTAL ANALYSIS"], dependencies=[verify_header()]
)
async def zone_average_chart_value(
    zones: list[str] = Query(
        ["연오랑세오녀 테마공원(귀비고)", "스페이스워크(환호공원)", "해상스카이워크"]
    ),
    date_from: date = date.today(),
):

    avg_chart_list = AvgChartList()

    now_people_dict = {}
    this_month_dict = {}
    residence_time_dict = {}
    yesterday_visitor_dict = {}

    try:
        for zone in zones:
            # 체류 인원
            now_people_all = await utils.device_count_hourly_util(params="1d")
            now_people_all = now_people_all.drop_duplicates("zone", keep="first")
            now_people_condition = now_people_all["zone"] == zone
            now_people = now_people_all.loc[now_people_condition]
            now_people_dict[zone] = int(now_people["data"])

            # 금월
            this_month_visitor_all = await utils.device_count_day_util(
                date_from=this_month_first, date_to=today
            )
            this_month_condition = this_month_visitor_all["zone"] == zone
            this_month_visitor_extract = this_month_visitor_all.loc[
                this_month_condition
            ]
            this_month_total_visitor = np.sum(
                this_month_visitor_extract["data"], axis=0
            )
            this_month_dict[zone] = int(this_month_total_visitor)

            # 평균 체류 시간
            residence_time = await utils.device_residence_time_util(
                date_from=today - timedelta(1), date_to=today
            )
            residence_time_condition = residence_time["zone"] == zone
            residence_time_extract = residence_time[residence_time_condition]
            residence_time = residence_time_extract["data"].values / 60
            residence_time_dict[zone] = int(residence_time)

            # 전일 방문자 전처리
            yester_day_visitor_all = await utils.device_count_revisit_util(
                date_from=date_from - timedelta(1), date_to=today
            )
            yester_day_condition = yester_day_visitor_all["zone"] == zone
            yester_day_visitor_extract = yester_day_visitor_all[yester_day_condition]
            yester_day_visitor_extract = yester_day_visitor_extract.drop_duplicates(
                "zone", keep="first"
            )
            yesterday_visitor_dict[zone] = int(
                yester_day_visitor_extract["data"].values
            )

        today_data = AvgChart(target="today", chartData=now_people_dict)
        yesterday_data = AvgChart(target="yesterday", chartData=yesterday_visitor_dict)
        this_month_data = AvgChart(target="month", chartData=this_month_dict)
        residence_data = AvgChart(target="residence", chartData=residence_time_dict)

        avg_chart_list.appendData(today_data.getTargetDict())
        avg_chart_list.appendData(yesterday_data.getTargetDict())
        avg_chart_list.appendData(this_month_data.getTargetDict())
        avg_chart_list.appendData(residence_data.getTargetDict())
        avg_chart_list.appendData({"last_update": str(datetime.now())})

        return avg_chart_list.getDataList()
    except HTTPException as e:
        print(e)
