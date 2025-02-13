class AvgChart:

    def __init__(self, target: str, chartData: dict):
        self.target = target
        self.chartData = chartData

    def getProperties(self):
        print(f"target is {self.target} && chartdata os {self.chartData}")

    def getTargetDict(self):
        target_dict = {}
        target_dict[self.target] = self.chartData
        return target_dict


class AvgChartList:
    def __init__(self):
        self.dataList = []

    def appendData(self, charData: dict):
        self.dataList.append(charData)

    def getDataList(self):
        return self.dataList
    
class AvgTotal:
    def __init__(
        self,
        nowPeople: int,
        today: int,
        revisitor: int,
        month: int,
        year: int,
        residence: int,
    ):
        self.nowPeople = nowPeople
        self.today = today
        self.revisitor = revisitor
        self.month = month
        self.year = year
        self.residence = residence

