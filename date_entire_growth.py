#개체 별 생육데이터
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os

rc('font', family = 'AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


class GrowthDataAnalysis:
    def __init__(self, input_file, mode, output_dir):
        self.input_file = input_file
        self.mode = mode
        self.output_dir = output_dir

        self.grouped_data = None
        self.filled_data = None

        os.makedirs(self.output_dir, exist_ok = True)
    
    #데이터를 날짜, mode만 선택하여 재생성?되도록 함
    def adjust_data(self):
        file_df = pd.ExcelFile(self.input_file)
        data_with_dates = []
        for sheet in file_df.sheet_names:
            date = pd.read_excel(self.input_file, sheet_name= sheet)
            date['날짜'] = sheet
            data_with_dates.append(date)
        
        combined_data = pd.concat(data_with_dates)
        
        #줄기두께 파트에서 24.11.15일자 cm => mm 단위 변환 안된것 변환하는 코드
        if self.mode == "줄기두께(cm)":
            combined_data.loc[combined_data['날짜'] == "2024-11-15", self.mode] *= 0.1

        self.grouped_data = combined_data[['개체번호', self.mode, '날짜']].groupby('개체번호')

    #결측값 처리
    def missing_value_processing(self, method = "mean"):
        
        filled_data = []
        for group_name, group_data in self.grouped_data:
            if method == 'interpolate':
                group_data[self.mode] = group_data[self.mode].interpolate(method = 'linear')
            elif method == 'mean':
                group_data[self.mode] = group_data[self.mode].fillna(group_data[self.mode].mean())
            filled_data.append(group_data)

        self.filled_data = pd.concat(filled_data).groupby("개체번호")
    
    #이상값 처리: 초장길이 데이터에서만 적용, 현재 값이 다음 값보다 큰 경우 '(그 전날의 값 + 그 다음날의 값) / 2'로 대체
    def error_value_processing(self):
        processed_data = []
        for group_name, group_data in self.filled_data:
            values = group_data[self.mode].values
            for i in range(1, len(values) - 1):
                if values[i] > values[i + 1]:
                    values[i] = (values[i - 1] + values[i + 1]) / 2
            group_data[self.mode] = values
            processed_data.append(group_data)

        self.filled_data = pd.concat(processed_data).groupby("개체번호")

    #그래프 그리기: ylim, 그래프 타입 지정해야함
    def graph_data(self, ylim = None, graph_type = "scatter"):
        plt.figure(figsize=(12, 8))
        
        for num, group in self.filled_data:
            if graph_type == "plot":
                plt.plot(group['날짜'], group[self.mode], marker='o', label=f'개체 {num}')
            elif graph_type == "scatter":
                plt.scatter(group['날짜'], group[self.mode], label=f'개체 {num}')
        
        plt.title(f"모든 개체의 {self.mode}")
        plt.xlabel("날짜")
        plt.ylabel(self.mode)
        plt.ylim(ylim)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # 범례를 그래프 바깥에 배치
        plt.grid(True)

        file_name = os.path.join(self.output_dir, f"{self.mode}_통합.png")
        plt.tight_layout()  # 레이아웃 자동 조정
        plt.savefig(file_name)
        plt.close()



input_file_name = "작재실2/작재2 생육 데이터.xlsx"
OUTPUT_BASE_DIR = "../Desktop/생육데이터2/개체 별 생육데이터_통합"

full_length = GrowthDataAnalysis(input_file= input_file_name, mode="초장(cm)", output_dir= OUTPUT_BASE_DIR)
full_length.adjust_data()
full_length.missing_value_processing(method="interpolate")
full_length.error_value_processing()
full_length.graph_data(ylim=(50,240), graph_type="plot")

flower_length = GrowthDataAnalysis(input_file= input_file_name, mode="화방높이(cm)", output_dir= OUTPUT_BASE_DIR)
flower_length.adjust_data()
flower_length.missing_value_processing(method="mean")
flower_length.graph_data(ylim=(0, 35), graph_type= "scatter")

leaf_length = GrowthDataAnalysis(input_file= input_file_name, mode="엽장(cm)", output_dir= OUTPUT_BASE_DIR)
leaf_length.adjust_data()
leaf_length.missing_value_processing(method="mean")
leaf_length.graph_data(ylim=(0, 50), graph_type= "scatter")

leaf_width = GrowthDataAnalysis(input_file= input_file_name, mode = "엽폭(cm)", output_dir= OUTPUT_BASE_DIR)
leaf_width.adjust_data()
leaf_width.missing_value_processing(method="mean")
leaf_width.graph_data(ylim=(0, 35), graph_type= "scatter")

stem_thickness = GrowthDataAnalysis(input_file= input_file_name, mode="줄기두께(cm)", output_dir= OUTPUT_BASE_DIR)
stem_thickness.adjust_data()
stem_thickness.missing_value_processing(method="mean")
stem_thickness.graph_data(ylim=(0, 1.2), graph_type= "scatter")

flower_group1 = GrowthDataAnalysis(input_file= input_file_name, mode="개화군", output_dir= OUTPUT_BASE_DIR)
flower_group1.adjust_data()
flower_group1.missing_value_processing(method="interpolate")
flower_group1.graph_data(ylim=(0, 10), graph_type= "scatter")

flower_group2 = GrowthDataAnalysis(input_file= input_file_name, mode="개화군", output_dir= OUTPUT_BASE_DIR)
flower_group2.adjust_data()
flower_group2.missing_value_processing(method="interpolate")
flower_group2.graph_data(ylim=(0, 10), graph_type= "plot")

fruit = GrowthDataAnalysis(input_file= input_file_name, mode="열매수", output_dir= OUTPUT_BASE_DIR)
fruit.adjust_data()
fruit.missing_value_processing(method="interpolate")
fruit.graph_data(ylim=(0, 75), graph_type= "plot")