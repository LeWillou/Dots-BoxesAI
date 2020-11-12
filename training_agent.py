import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
import numpy as np
import csv
import sys

maxInt = sys.maxsize

# while True:
#     # decrease the maxInt value by factor 10 
#     # as long as the OverflowError occurs.

#     try:
#         csv.field_size_limit(maxInt)
#         break
#     except OverflowError:
#         maxInt = int(maxInt/10)

# with open('dataset_training.csv', newline='') as csvfile:
#     data = list(csv.reader(csvfile, delimiter=','))

data = np.load('dataset_training.npy', allow_pickle=True)

dataset = list()

dataset_states = list()

dataset_choices = list()

transition_array = list()

for i in range(len(data[0])):
    dataset.append(data[0][i])

for i in range(len(dataset)):
    for j in range(len(dataset[i])):
        transition_array.append(dataset[i][j])
        #print(dataset[i][j])
    dataset_states.append(transition_array[0:])
    transition_array.clear()

# print(data[0][0].shape)

#print(dataset)

dataset_states_to_use = np.array(dataset_states)

#data[0].reshape(57, 112)

# print(data[1].shape)

dataset.clear()

for i in range(len(data[1])):
    dataset.append(data[1][i])

for i in range(len(dataset)):
    for j in range(len(dataset[i])):
        transition_array.append(dataset[i][j])
        #print(dataset[i][j])
    dataset_choices.append(transition_array[0:])
    transition_array.clear()

dataset_choices_to_use = np.array(dataset_choices)

# Y = np.asarray(dataset_choices_to_use).astype(np.float32)

opt = Adam(lr=0.1, beta_1=0.9, beta_2=0.999)

model = Sequential()

model.add(Dense(500, input_dim = 112))
model.add(Dropout(rate=0.3))
model.add(Dense(2))
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(dataset_states_to_use, dataset_choices_to_use, epochs=1000, verbose=2)
