import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

dataset_train = pd.read_csv('StockData/Training_Data.csv')
with open('StockData/Training_Data.csv',"r") as f:
    reader = csv.reader(f,delimiter = ",")
    data = list(reader)
    row_count = len(data)-1
print(row_count)
training_set = dataset_train.iloc[:, 1:5].values

dataset_train.head()

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

X_train = []
y_train = []
for i in range(60, row_count):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0:])
X_train, y_train = np.array(X_train), np.array(y_train)

X_train = np.reshape(X_train, (-1, X_train.shape[1], 1))
y_train = np.reshape(y_train, (-1, y_train.shape[1]))

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras import backend as K

print(X_train.shape)

regressor = Sequential()

regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units = 4))

regressor.summary()

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

dataset_test = pd.read_csv('StockData/Test_Data.csv')
with open('StockData/Test_Data.csv',"r") as f:
    reader = csv.reader(f,delimiter = ",")
    data = list(reader)
    row_count = len(data)-1
print(row_count)
real_stock_price = dataset_test.iloc[:, 1:5].values

dataset_total = pd.concat((dataset_train['open'], dataset_test['open']), axis = 0)
print(dataset_total.shape)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.fit_transform(inputs)
X_test = []
for i in range(60, row_count):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
print(inputs.shape)
print(X_test.shape)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

print("Predicted Price:")
print(predicted_stock_price)
print("Actual Price:")
print(real_stock_price)

plt.plot(real_stock_price, color = 'black', label = 'TATA Stock Price')
plt.plot(predicted_stock_price, color = 'green', label = 'Predicted TATA Stock Price')
plt.title('TATA Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('TATA Stock Price')
plt.legend()
plt.savefig('TATA.png')