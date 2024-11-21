#개체 별 초장길이 변화

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os

file = "작재실2/작재2 생육 데이터.xlsx"
file_df = pd.ExcelFile(file)

mode = "초장(cm)"
#df에 날짜 추가
data_with_dates = []
for sheet in file_df.sheet_names:
    date = pd.read_excel(file, sheet_name= sheet)
    date['날짜'] = sheet
    data_with_dates.append(date)
#print(data_with_dates)

combined_data = pd.concat(data_with_dates)

grouped_data = combined_data[['개체번호', mode, '날짜']].groupby('개체번호')



#결측값 처리
filled_data = []
for group_name, group_data in grouped_data:
    group_data[mode] = group_data[mode].interpolate(method = 'linear')
    filled_data.append(group_data)

filled_data = pd.concat(filled_data).groupby("개체번호")

#이상값 처리
correct_data = []
for group_name, group_data in filled_data:
    values = group_data[mode].values
    for i in range(1, len(values) - 1):
        if values[i] > values[i + 1]:
            values[i] = (values[i - 1] + values[i + 1]) / 2
    group_data[mode] = values
    correct_data.append(group_data)

processed_data = pd.concat(correct_data)

#그래프 그리기
rc('font', family = 'AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

new_data_dir = "../Desktop/생육데이터/개체 별 초장길이"

for num, group in processed_data.groupby("개체번호"):
    plt.figure()
    plt.plot(group['날짜'], group[mode], marker='o', label=f'{num} 초장길이')
    plt.title(f"{num}의 {mode}")
    plt.xlabel("날짜")
    plt.ylabel("mode")
    plt.ylim(50, 240)
    plt.grid(True)
    plt.legend()
    #plt.show()

    file_name = os.path.join(new_data_dir, f"{num}_{mode}.png")
    plt.savefig(file_name)
    plt.close()
