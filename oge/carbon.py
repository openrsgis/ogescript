import json
import requests


class carbonEmission():
   
    def __init__(self): 
        self.region = None
        self.period = None

    # 获取省级碳排放数据
    def getProvinceCarbon(self,region, period):
        self.region = region
        self.period = period

        raw = json.dumps({
            "regions": region,
            "periods": period
        })
        headers = {
            'Content-Type': 'application/json'
        }
       
        response = requests.request('POST', 'http://localhost:19090/api/ceapp/carbon-emission/province-carbons', headers=headers, data=raw)
        result = response.json()
        return result.get('data')
           
    # 获取省级经济指标 
    def getProvinceCarbonIndex(self,region, period):
        self.region = region
        self.period = period
        raw = json.dumps({
            "regions": region,
            "periods": period
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request('POST', 'http://localhost:19090/api/ceapp/carbon-emission/province-carbon-indexes', headers=headers, data=raw)
        result = response.json()
        return result.get('data')
    
    # 获取分省的地级市列表
    def getCityByProvince(self,region):
        raw = json.dumps(region)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request('POST', 'http://localhost:19090/api/ceapp/carbon-emission/prefectures-by-provinces', headers=headers, data=raw)
        result = response.json()
        return result.get('data').get('prefectures')

    # 获取城市的经济统计指标
    def getCityCarbonIndex(self,regioncities,period):
        raw = json.dumps({
            "regions": regioncities,
            "periods": period
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request('POST', 'http://localhost:19090/api/ceapp/carbon-emission/prefecture-carbon-indexes', headers=headers, data=raw)
        result = response.json()
        return result.get('data').get('prefectureCarbonIndexes')
    
    # 获取城市的碳排放分配比例
    def getCityCarbonProportion(self,provinceCarbonIndex, cityCarbonIndex):
        raw = json.dumps({
            "regions": self.region,
            "periods": self.period
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request('POST', 'http://localhost:19090/api/ceapp/carbon-emission/carbon-proportions', headers=headers, data=raw)
        result = response.json()
        return result.get('data').get('prefectureCarbonIndex')
    
    # 获取城市的碳排放
    def getCityCarbon(self,regionCarbon, cityCarbonProportionList):
        raw = json.dumps({
            "regions": self.region,
            "periods": self.period
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request('POST', 'http://localhost:19090/api/ceapp/carbon-emission/prefecture-carbons', headers=headers, data=raw)
        result = response.json()
        return result.get('data')

