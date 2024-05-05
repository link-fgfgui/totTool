import pprint
import requests
import urllib.parse
import copy
import re
import json
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))
rd = {
    "info": {
        "uid": "000000000",
        "lang": "zh-cn",
    },
    "list": [
        # {
        #     "gacha_type": "000",
        #     "item_id": "",
        #     "count": "1",
        #     "time": "yyyy-MM-dd HH:mm:ss",
        #     "name": "以理服人",
        #     "item_type": "武器",
        #     "rank_type": "3",
        #     "id": "1600099200004770203",
        #     "uigf_gacha_type": "000",
        # },

    ]
}

in_ = input("Please Input Url:\n")
q = urllib.parse.urlparse(in_).query
ak = re.findall("&authkey=(.*?)&",q)[0]
# pprint.pprint(ak)

r = s.get(f"https://api-takumi.mihoyo.com/common/nxx_self_query/api/playerinfo?sign_type=2&auth_appid=csc&authkey_ver=1&win_direction=portrait&page_id=7&operating_system=Android%20OS%2014%20%2F%20API-34%20%28UP1A.231005.007%2FV816.0.1.0.ULHCNXM%29&device_model=Xiaomi%2023054RA19C&authkey={ak}&lang=zh-cn&game_biz=nxx_cn&device_type=mobile&region=cn_prod_gf01&plat_type=android").json()["data"]
rd['info']["uid"] = r["uid"]

r = s.get(
    f"https://api-takumi.mihoyo.com/common/nxx_self_query/api/submenulist?sign_type=2&auth_appid=csc&authkey_ver=1&win_direction=portrait&page_id=7&operating_system=Android%20OS%2014%20%2F%20API-34%20%28UP1A.231005.007%2FV816.0.1.0.ULHCNXM%29&device_model=Xiaomi%2023054RA19C&authkey={ak}&lang=zh-cn&game_biz=nxx_cn&device_type=mobile&region=cn_prod_gf01&plat_type=android&type=gacha")
j = r.json()
lst = j["data"]["list"]


for it in lst:
    type_ = it["type"]
    page=1
    while True:
        r = s.get(
            f"https://api-takumi.mihoyo.com/common/nxx_self_query/api/gachalist?sign_type=2&auth_appid=csc&authkey_ver=1&win_direction=portrait&page_id=7&operating_system=Android%20OS%2014%20%2F%20API-34%20%28UP1A.231005.007%2FV816.0.1.0.ULHCNXM%29&device_model=Xiaomi%2023054RA19C&authkey={ak}&lang=zh-cn&game_biz=nxx_cn&device_type=mobile&region=cn_prod_gf01&plat_type=android&page={page}&page_size=10&type={type_}")
        j = r.json()["data"]["list"]
        if j==[]:
            break
        for itt in j:
            od = dict()
            od["gacha_type"] = type_
            od["count"] = "1"
            od["time"] = itt["time"]
            od["name"] = re.findall(" 「(.*?)」", itt["item"])[0]
            od["item_type"] = "思绪"
            od["rank_type"] = re.findall("(.*?) 「", itt["item"])[0]
            rd["list"].append(od)
            page+=1
with open("{}.json".format(rd["info"]["uid"]),"w") as f:
    json.dump(rd,f)

