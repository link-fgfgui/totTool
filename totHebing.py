import pprint
import json
import time
ins = []
i = 1
try:
    while True:
        ins.append(input(f"file{i} path:"))
        i += 1
except KeyboardInterrupt:
    pass
print(f"\ninputed {i-1} files")
print("reading...")
i = 0
db = {}
uid = None
for j in ins:
    i += 1
    print(f"read No.{i} {j}")
    with open(j, "r")as f:
        d = json.load(f)
    if i == 1:
        outlist = d["list"]
        uid = d["info"]["uid"]
        continue
    if (uid != d["info"]["uid"]) and (uid != None):
        print("请不要使用不同账号的数据进行合并!程序将自动退出")
        import sys
        sys.exit(1)
    kkkk = 0
    # for kkkk in range():
    while kkkk < len(d["list"]):
        k = d["list"][kkkk]
        for kk in outlist:
            if k["time"] == kk["time"]:
                print("finded! "+k["gacha_type"] +
                      ' '+k["rank_type"]+" "+k["name"])
                break
        else:
            if kkkk != len(d["list"])-1:
                if d["list"][kkkk+1]["time"] == k["time"]:
                    for kkk in range(10):
                        print("passed! "+d["list"][kkkk+kkk]["gacha_type"] +
                              ' '+d["list"][kkkk+kkk]["rank_type"]+" "+d["list"][kkkk+kkk]["name"])
                        outlist.append(d["list"][kkkk+kkk])
                    kkkk += 10
                    continue
            print("not find! "+k["gacha_type"] +
                  ' '+k["rank_type"]+" "+k["name"])
            outlist.append(k)
        kkkk += 1

    # for h in d["list"]:
    #     if db.get(h["gacha_type"])==None:
    #         db[h["gacha_type"]]=[]
    #     timee=int(time.mktime(time.strptime(h["time"],"%Y-%m-%d %H:%M:%S")))
    #     db[i][h["gacha_type"]].append((timee,h))
    # for k in db[i]:
    #     db[i][k].sort(key=lambda e:e[0])

    #     if db[h["gacha_type"]].get(h["rank_type"])==None:
    #         db[h["gacha_type"]][h["rank_type"]]={}
    #     if db[h["gacha_type"]][h["rank_type"]].get(h["time"])==None:
    #         db[h["gacha_type"]][h["rank_type"]][h["time"]]={}
    #     db[h["gacha_type"]][h["rank_type"]][h["time"]][h["name"]]=h
print("readed")
print("saveing")
# pprint.pprint(db)
# outlist=list()
# for i1 in db:
#     for i2 in db[i1]:
#         for i3 in db[i1][i2]:
#             for i4 in db[i1][i2][i3]:
#                 outlist.append(db[i1][i2][i3][i4])
d["list"] = outlist
with open(uid+"hbOut.json", "w")as f:
    json.dump(d, f)
