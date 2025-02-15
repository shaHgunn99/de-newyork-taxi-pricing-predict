from datetime import datetime 
import pandas as pd 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
import sklearn.metrics as metrics
import pickle # 모델 저장

input_file = "/Users/dongwoo/trip_csv/yellow_tripdata_2021-01.csv"

df = pd.read_csv(input_file, header=0)

# 필요한 정보 가져오기 #
"""
total amount가 20 이하,
trip_distance 가 100mile 이하

"""
df = df.loc[(df["total_amount"] < 20) & (df["trip_distance"] < 100)]
distance = df["trip_distance"]
hours = df["tpep_pickup_datetime"].map(
  lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").hour
)
data = pd.concat([hours, distance], axis=1)

target = df["total_amount"]

# 데이터 분할 #
train_x, test_x, train_y, test_y = train_test_split(
  data,
  target,
  test_size = 0.2,
  random_state = 24
)


# 머신러닝 #
lr = LinearRegression()
lr.fit(train_x, train_y)

prediction = lr.predict(test_x) # 예측

mse = metrics.mean_squared_error(test_y, prediction)
print(mse)
print("PREDICTION")
print(prediction[:5])
print("LABEL")
print(test_y[:5])


# training한 모델 저장 #
with open("model.pkl", "wb") as f:
  pickle.dump(lr, f)