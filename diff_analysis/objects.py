class AvgTotal:
    def __init__(
        self,
        nowPeople: int,
        today: int,
        yesterday: int,
        month: int,
        year: int,
        residence: int,
    ):
        self.nowPeople = nowPeople
        self.today = today
        self.yesterday = yesterday
        self.month = month
        self.year = year
        self.residence = residence

    def getTargetDict(self, target: str):
        target_dict = {}
        target_dict["data"] = {
            "zone": target,
            "nowPeople": self.nowPeople,
            "today": self.today,
            "yesterday": self.yesterday,
            "month": self.month,
            "year": self.year,
            "residence": self.residence,
        }
        return target_dict


class AvgChartList:
    def __init__(self):
        self.dataList = []

    def appendData(self, charData: dict):
        self.dataList.append(charData)

    def getDataList(self):
        return self.dataList


class floatpopulationTotal:
    def __init__(
        self,
        nowPeople: int,  # 현재 체류 인원 ㅇㅇㅇ
        yesterday: int,  # 전일 방문자 ㅇㅇ
        month: int,  # 월 방문자 ㅇㅇ
        residence: int,  # 평균 체류 시간 ㅇㅇㅇ
        last_update: str,
    ):
        self.nowPeople = nowPeople
        self.yesterday = yesterday
        self.month = month
        self.residence = residence
        self.last_update = last_update

    def getTargetDict(self, target: str):
        target_dict = {}
        target_dict[target] = {
            "nowPeople": self.nowPeople,
            "yesterday": self.yesterday,
            "month": self.month,
            "residence": self.residence,
            "last_update": self.last_update,
        }
        return target_dict


class DiffZoneList:
    def __init__(self):
        self.dataList = []

    def appendData(self, charData: dict):
        self.dataList.append(charData)

    def getDataList(self):
        return self.dataList
