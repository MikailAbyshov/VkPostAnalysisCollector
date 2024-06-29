import requests
import datetime


class PostAnalysisCollector:

    def __init__(self, TOKEN, DOMAIN):
        self.TOKEN = TOKEN
        self.DOMAIN = DOMAIN

    def GetAnalysisByPeriod(self, startPeriod, endPerod=datetime.MAXYEAR):
        pass
    