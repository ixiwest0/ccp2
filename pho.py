import pandas as pd

filename = "작재실2/전북대온실 2조(C)_2024-10-02_2024-11-15.csv"
data = pd.read_csv(filename)

data['timestamp'] = data['timestamp'].str[:23]

data['timestamp'] = pd.to_datetime(data['timestamp'], format="%Y-%m-%d %H:%M:%S.%f")


data['date'] = data['timestamp'].dt.date
#data['time'] = data['timestamp'].dt.time


def calculate_mean_accumulated_light(data, start, end):
    start_date = pd.to_datetime(start).date()
    end_date = pd.to_datetime(end).date()

    date_range = pd.date_range(start=start_date, end=end_date).date

    last_light_values = []
    for current_date in date_range:
        filtered_data = data[data['date'] == current_date]
        if not filtered_data.empty:
            last_value = filtered_data.iloc[-1]['내부누적광량(J/cm2)']
            last_light_values.append(last_value)

    mean_accumulated_light = sum(last_light_values) / len(last_light_values)
    return mean_accumulated_light


# 사용자가 선택한 기간
start_date = "2024-11-08"
end_date = "2024-11-14"

mean_light = calculate_mean_accumulated_light(data, start_date, end_date)
print(f"{start_date}부터 {end_date}까지의 내부 누적광량 평균: {mean_light:.2f} J/cm2")
