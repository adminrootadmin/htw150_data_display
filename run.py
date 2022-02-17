import os
import re
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from datetime import datetime

VERSION_MAJOR = "0"
VERSION_MINOR = "0"
VERSION_PATCH = "0"
VERSION = VERSION_MAJOR + '.' + VERSION_MINOR + '.' + VERSION_PATCH
RE_MATCH = r"\[(\d{4}\-\d{1,2}\-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})] ST,GS,\s+(\d+\.\d+) lb"
UNIT_OF_WEIGHT = "lb"

data = []

if __name__ == '__main__':
    print("=" * 20)
    print("software version:" + VERSION + '\n')

    print("regular match:")
    print(RE_MATCH + '\n')

    print("unit of weight:", UNIT_OF_WEIGHT)
    print("=" * 20)

    print("current path:", os.getcwd())

    # 获取脚本所在目录下txt文件
    txt_files = [f for f in os.listdir(".") if re.match(r'.*\.txt', f)]
    print("the number of txt files:", len(txt_files))
    if len(txt_files) <= 0:
        print("[ERR]not found txt files.")
        os.system('pause')

    # 从一个或多个txt文件中获取符合正则表达式的行，并提取日期和重量
    for file in txt_files:
        for line in open(file):
            match_obj = re.match(RE_MATCH, line)
            if match_obj:
                dtime_weight = {"dtime": datetime.strptime(match_obj.group(1), "%Y-%m-%d %H:%M:%S"),
                                "weight": float(match_obj.group(2))}
                data.append(dtime_weight)
    print("the number of data:", len(data))
    if len(data) <= 0:
        print("[ERR]not found data by \"." + RE_MATCH + "\"")
        os.system('pause')

    df = pd.DataFrame(data)  # 载入数据
    df.sort_values("dtime", inplace=True)  # dtime排序

    # 设置格式
    plt.gca().set_xlabel("dtime")
    plt.gca().set_ylabel("weight(" + UNIT_OF_WEIGHT + ')')
    date_format = mpl_dates.DateFormatter('%Y-%m-%d %H:%M')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.grid()  # 开启网格线

    # 画表格
    plt.plot_date(df.dtime, df.weight, linestyle="solid")

    plt.show()
