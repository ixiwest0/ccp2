#날짜 별 생육데이터
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os

rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


class GrowthDataAnalysis:
    def __init__(self, input_file, mode, output_dir):
        self.input_file = input_file
        self.mode = mode
        self.output_dir = output_dir

        self.grouped_data = None
        self.filled_data = None

        os.makedirs(self.output_dir, exist_ok=True)

    # 데이터를 날짜와 mode만 선택하여 재구성
    def adjust_data(self):
        file_df = pd.ExcelFile(self.input_file)
        data_with_dates = []
        for sheet in file_df.sheet_names:
            date = pd.read_excel(self.input_file, sheet_name=sheet)
            date['날짜'] = sheet
            data_with_dates.append(date)

        combined_data = pd.concat(data_with_dates)

        # 줄기두께의 단위 변환 (2024-11-15일자 cm -> mm)
        if self.mode == "줄기두께(cm)":
            combined_data.loc[combined_data['날짜'] == "2024-11-15", self.mode] *= 0.1

        self.grouped_data = combined_data[['개체번호', self.mode, '날짜']].groupby('날짜')

    # 결측값 처리
    def missing_value_processing(self, method="mean"):
        filled_data = []
        for date, group_data in self.grouped_data:
            if method == 'interpolate':
                group_data[self.mode] = group_data[self.mode].interpolate(method='linear')
            elif method == 'mean':
                group_data[self.mode] = group_data[self.mode].fillna(group_data[self.mode].mean())
            filled_data.append(group_data)

        self.filled_data = pd.concat(filled_data).groupby('날짜')

    # 이상값 처리: 초장 데이터에서만 적용
    def error_value_processing(self):
        processed_data = []
        for date, group_data in self.filled_data:
            values = group_data[self.mode].values
            for i in range(1, len(values) - 1):
                if values[i] > values[i + 1]:
                    values[i] = (values[i - 1] + values[i + 1]) / 2
            group_data[self.mode] = values
            processed_data.append(group_data)

        self.filled_data = pd.concat(processed_data).groupby('날짜')

    # 그래프 그리기: x축 개체번호, y축 mode
    def graph_data(self, ylim=None, graph_type = None):
        for date, group in self.filled_data:
            plt.figure(figsize=(10, 6))
            if graph_type == "plot":
                plt.plot(group['개체번호'], group[self.mode], marker='o', label=f"{date}의 {self.mode}", color='blue')
            elif graph_type == "scatter":
                plt.scatter(group['개체번호'], group[self.mode], marker='o', label=f"{date}의 {self.mode}", color='blue')
            elif graph_type == "bar":
                plt.bar(group['개체번호'], group[self.mode], label=f"{date}의 {self.mode}", color='blue')
            plt.title(f"{date}의 {self.mode}")
            plt.xlabel("개체번호")
            plt.ylabel(self.mode)
            plt.ylim(ylim)
            plt.grid(True)
            plt.legend()

            # 그래프 저장
            file_name = os.path.join(self.output_dir, f"{date}_{self.mode}.png")
            plt.savefig(file_name)
            plt.close()


# 입력 파일 및 출력 디렉토리 설정
input_file_name = "작재실2/작재2 생육 데이터.xlsx"
OUTPUT_BASE_DIR = "../Desktop/생육데이터2/날짜 별 생육데이터"

full_length = GrowthDataAnalysis(input_file= input_file_name, mode="초장(cm)", output_dir= os.path.join(OUTPUT_BASE_DIR, "날짜 별 개체들의 초장길이"))
full_length.adjust_data()
full_length.missing_value_processing(method="interpolate")
full_length.error_value_processing()
full_length.graph_data(ylim=(50,240), graph_type="scatter")

flower_length = GrowthDataAnalysis(input_file= input_file_name, mode="화방높이(cm)", output_dir= os.path.join(OUTPUT_BASE_DIR, "날짜 별 개체들의 화방높이"))
flower_length.adjust_data()
flower_length.missing_value_processing(method="mean")
flower_length.graph_data(ylim=(0, 35), graph_type= "scatter")

leaf_length = GrowthDataAnalysis(input_file= input_file_name, mode="엽장(cm)", output_dir= os.path.join(OUTPUT_BASE_DIR, "날짜 별 개체들의 엽장"))
leaf_length.adjust_data()
leaf_length.missing_value_processing(method="mean")
leaf_length.graph_data(ylim=(0, 50), graph_type= "scatter")

leaf_width = GrowthDataAnalysis(input_file= input_file_name, mode = "엽폭(cm)", output_dir= os.path.join(OUTPUT_BASE_DIR, "날짜 별 개체들의 엽폭"))
leaf_width.adjust_data()
leaf_width.missing_value_processing(method="mean")
leaf_width.graph_data(ylim=(0, 35), graph_type= "scatter")

stem_thickness = GrowthDataAnalysis(input_file= input_file_name, mode="줄기두께(cm)", output_dir= os.path.join(OUTPUT_BASE_DIR, "날짜 별 개체들의 줄기두께"))
stem_thickness.adjust_data()
stem_thickness.missing_value_processing(method="mean")
stem_thickness.graph_data(ylim=(0, 1.2), graph_type= "scatter")

flower_group1 = GrowthDataAnalysis(input_file= input_file_name, mode="개화군", output_dir= os.path.join(OUTPUT_BASE_DIR, "날짜 별 개체들의 개화군"))
flower_group1.adjust_data()
flower_group1.missing_value_processing(method="interpolate")
flower_group1.graph_data(ylim=(0, 10), graph_type= "scatter")

fruit = GrowthDataAnalysis(input_file= input_file_name, mode="열매수", output_dir= os.path.join(OUTPUT_BASE_DIR, "날짜 별 개체들의 열매수"))
fruit.adjust_data()
fruit.missing_value_processing(method="interpolate")
fruit.graph_data(ylim=(0, 75), graph_type= "bar")