import os
import pandas as pd
import numpy as np
import common
import json
from . import utils
from common import verify_header
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, Query
from datetime import date, timedelta, datetime
from .objects import AvgTotal, DiffZoneList, floatpopulationTotal, AvgChartList

router = APIRouter(prefix="/api/diff_analysis")

today = date.today()
this_month_first = datetime(today.year, today.month, 1)
one_week_ago = today - timedelta(7)


zone_list = [
    "구룡포 일본인가옥거리",
    "내연산/보경사",
    "사방기념공원",
    "송도송림테마거리(솔밭도시숲)",
    "송도해수욕장",
    "스페이스워크(환호공원)",
    "연오랑세오녀 테마공원(귀비고)",
    "영일대해수욕장/해상누각",
    "오어사",
    "이가리 닻 전망대",
    "일월문화공원",
    "장기유배문화체험촌",
    "해상스카이워크",
    "호미곶 해맞이광장",
]


# 금년 전체 통계를 위한 API 입니다.
# 자세한 사항은 iP/docs 확인
@router.get(
    "/diff_average_zone_value", tags=["DIFF ANALYSIS"], dependencies=[verify_header()]
)
async def diff_average_zone_value(date_from: date = date.today()):
    diff_zone_list = DiffZoneList()

    try:
        now_people_all_origin = await utils.device_count_hourly_util(params="1d")
        today_visitor_all_origin = await utils.device_count_hourly_util(params="1d-1h")
        yester_day_visitor_all_origin = await utils.device_count_revisit_util(
            date_from=date_from - timedelta(1), date_to=today
        )
        this_month_visitor_all_origin = await utils.device_count_day_util(
            date_from=this_month_first.strftime("%Y-%m-%d"), date_to=today
        )
        this_year_visitor_all_origin = await utils.device_count_day_util(
            date_from=str(today - timedelta(365)), date_to=today
        )
        residence_time_origin = await utils.device_residence_time_util(
            date_from=today - timedelta(1), date_to=today
        )

        for zones_key in zone_list:
            now_people_all = now_people_all_origin
            today_visitor_all = today_visitor_all_origin
            yester_day_visitor_all = yester_day_visitor_all_origin
            this_month_visitor_all = this_month_visitor_all_origin
            this_year_visitor_all = this_year_visitor_all_origin
            residence_time = residence_time_origin

            # 현재 체류 인원 전처리
            now_people_all = now_people_all.drop_duplicates("zone", keep="first")
            now_people_condition = (
                now_people_all["zone"] == zones_key
            )  # 키에 따른 값 추출
            now_people = now_people_all.loc[now_people_condition]  # 필요한 값 추출

            # 금일 현재시간까지 방문자 전처리
            today_visitor_condition = (
                today_visitor_all["zone"] == zones_key
            )  # 키에 따른 값 추출
            today_visitor = today_visitor_all.loc[
                today_visitor_condition
            ]  # 필요한 값 추출
            today_total_visitor = np.sum(today_visitor["data"].values)  # 데이터 합산

            # 전일 방문자 전처리
            yester_day_condition = yester_day_visitor_all["zone"] == zones_key
            yester_day_visitor_extract = yester_day_visitor_all[yester_day_condition]
            yester_day_visitor_extract = yester_day_visitor_extract.drop_duplicates(
                "zone", keep="first"
            )

            this_month_condition = this_month_visitor_all["zone"] == zones_key
            this_month_visitor_extract = this_month_visitor_all.loc[
                this_month_condition
            ]
            this_month_total_visitor = np.sum(
                this_month_visitor_extract["data"], axis=0
            )

            # 년 방문자 전처리 ( 오늘 날로 부터 1년전 )
            this_year_condition = this_year_visitor_all["zone"] == zones_key
            this_year_visitor_extract = this_year_visitor_all.loc[this_year_condition]
            this_year_total_visitor = np.sum(this_year_visitor_extract["data"], axis=0)

            # 평균 체류 시간

            residence_time_condition = residence_time["zone"] == zones_key
            residence_time_extract = residence_time[residence_time_condition]
            residence_time = np.sum(residence_time_extract["data"].values) / 60

            total_avg = AvgTotal(
                nowPeople=int(now_people["data"]),
                today=int(today_total_visitor),
                yesterday=int((yester_day_visitor_extract["data"])),
                month=int(this_month_total_visitor),
                year=int(this_year_total_visitor),
                residence=int(residence_time),
            )
            diff_zone_list.appendData(total_avg.getTargetDict(target=zones_key))

        diff_zone_list.appendData({"last_update": str(datetime.now())})
        return diff_zone_list.getDataList()
    except HTTPException as e:
        print(e)


# 금년 전체 통계를 위한 API 입니다.
# 자세한 사항은 iP/docs 확인
@router.get(
    "/total_floatpopulation", tags=["DIFF ANALYSIS"], dependencies=[verify_header()]
)
async def total_floatpopulation_api(
    find_key: str = "포항관광지 전체",
    date_from: date = one_week_ago,
    date_to: date = today,
):
    try:
        # 체류 인원 데이터 받아오기
        now_people_all = await utils.device_count_day_util(
            date_from=date_from, date_to=date_to
        )

        # now_people_all이 DataFrame인지 확인하고 처리
        if isinstance(now_people_all, pd.DataFrame):
            # 'zone'이 find_key와 일치하는 데이터만 필터링
            filtered_data = now_people_all[now_people_all["zone"] == find_key]

            # 'data' 값을 모두 더함
            total_people = filtered_data["data"].sum()
            # print('total_people', total_people)

            # 날짜 차이 계산
            diff_day = (date_to - date_from).days
            # print(f"날짜 차이(diff_day): {diff_day}일")

            # 평균 계산
            average_people = total_people / diff_day

            # print(f"전체 인원 수: {total_people}, 평균 인원 수: {average_people}")

        # 전일 방문자 전처리
        yester_day_visitor_all = await utils.device_count_revisit_util(
            date_from=date_from, date_to=date_to
        )
        yester_day_condition = yester_day_visitor_all["zone"] == find_key
        yester_day_visitor_extract = yester_day_visitor_all[yester_day_condition]
        yester_day_visitor_extract = np.sum(yester_day_visitor_extract["data"], axis=0)

        # 7일전부터 현재까지 방문자 전처리
        this_month_visitor_all = await utils.device_count_day_util(
            date_from=date_from, date_to=date_to
        )
        this_month_condition = this_month_visitor_all["zone"] == find_key
        this_month_visitor_extract = this_month_visitor_all.loc[this_month_condition]
        this_month_total_visitor = np.sum(this_month_visitor_extract["data"], axis=0)

        # 평균 체류 시간
        residence_time = await utils.device_residence_time_util(
            date_from=date_from, date_to=date_to
        )
        residence_time_condition = residence_time["zone"] == find_key
        residence_time_extract = residence_time[residence_time_condition]
        residence_time_total_sum_sum = np.sum(residence_time_extract["data"].values)
        residence_time = residence_time_total_sum_sum / 60 / 24

        total_floatpopulation_data = floatpopulationTotal(
            nowPeople=int(average_people),
            yesterday=int((yester_day_visitor_extract)),
            month=int(this_month_total_visitor),
            residence=int(residence_time),
            last_update=str(datetime.now()),
        )

        return total_floatpopulation_data
    except HTTPException as e:
        print(e)


@router.get(
    "/range_popular_all_list", tags=["DIFF ANALYSIS"], dependencies=[verify_header()]
)
async def range_popular_all_list(
    date_from: date = one_week_ago,
    date_to: date = today,
):

    avg_chart_list = common.AvgChartList()

    try:
        range_now_people_dict = {}
        range_revisitor_dict = {}
        range_this_month_dict = {}
        range_residence_time_dict = {}

        # 데이터 원본 유지 및 API 재 호출 방지
        range_people_all = await utils.device_count_day_util(
            date_from=date_from, date_to=date_to
        )
        range_revisitor_all = await utils.device_count_revisit_util(
            date_from=date_from, date_to=date_to
        )
        range_month_visitor_all = await utils.device_count_day_util(
            date_from=date_from, date_to=date_to
        )
        range_residence_time = await utils.device_residence_time_util(
            date_from=date_from, date_to=date_to
        )

        for zones in zone_list:
            # 원본 데이터 손상방지를 위한 데이터셋 카피
            range_people_all_copy = range_people_all
            range_month_visitor_all_copy = range_month_visitor_all
            range_revisitor_all_copy = range_revisitor_all
            range_residence_time_copy = range_residence_time

            # 체류인원
            range_people_condition = range_people_all_copy["zone"] == zones
            range_people_extract = range_people_all_copy.loc[range_people_condition]
            range_people = np.sum(range_people_extract["data"], axis=0)
            range_now_people_dict[zones] = int(range_people)

            # 재방문자
            revisitor_all_copy_condition = range_revisitor_all_copy["zone"] == zones
            revisitor_all__extract = range_revisitor_all_copy[
                revisitor_all_copy_condition
            ]
            range_revisitor_all_copy = np.sum(revisitor_all__extract["data"], axis=0)
            range_revisitor_dict[zones] = int(range_revisitor_all_copy)

            # 월 누계
            range_this_month_condition = range_month_visitor_all_copy["zone"] == zones
            range_this_month_visitor_extract = range_month_visitor_all_copy.loc[
                range_this_month_condition
            ]
            range_month_visitor_all_copy = np.sum(
                range_this_month_visitor_extract["data"], axis=0
            )
            range_this_month_dict[zones] = int(range_month_visitor_all_copy)

            # 평균 체류 시간
            range_residence_time_condition = range_residence_time_copy["zone"] == zones
            residence_time_extract = range_residence_time_copy[
                range_residence_time_condition
            ]
            range_residence_time_copy = (
                np.sum(residence_time_extract["data"].values) / 60 / 24
            )
            range_residence_time_dict[zones] = int(range_residence_time_copy)

        range_today_data = common.AvgChart(
            target="today", chartData=range_now_people_dict
        )
        range_revisitor_data = common.AvgChart(
            target="revisitor", chartData=range_revisitor_dict
        )
        range_this_month_data = common.AvgChart(
            target="month", chartData=range_this_month_dict
        )
        range_residence_data = common.AvgChart(
            target="residence", chartData=range_residence_time_dict
        )

        avg_chart_list.appendData(range_today_data.getTargetDict())
        avg_chart_list.appendData(range_revisitor_data.getTargetDict())
        avg_chart_list.appendData(range_this_month_data.getTargetDict())
        avg_chart_list.appendData(range_residence_data.getTargetDict())
        avg_chart_list.appendData({"last_update": str(datetime.now())})

        return avg_chart_list.getDataList()
    except HTTPException as e:
        print(e)
