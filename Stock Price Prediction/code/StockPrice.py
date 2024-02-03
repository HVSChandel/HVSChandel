import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.models import load_model
import os

def train_and_save_model(csv_file, previous_model_file):
    # Load your data from the CSV file
    data = pd.read_csv(csv_file)

    # Split the "date" column into date, time, and timezone components
    split_values = data['date'].str.split(' ', expand=True)
    data['date'] = split_values[0]
    data['timezone'] = split_values[1]

    # Extract the timezone part
    split_values2 = data['timezone'].str.split('+', expand=True)
    data['time'] = split_values2[0]

    # Drop the "timezone" column
    data drop('timezone', axis=1, inplace=True)

    # Get the column names and reorder them
    column_names = data.columns.tolist()
    column_names = column_names[:-1]  # Exclude the last column
    column_names.insert(1, 'time')  # Insert the column to the second position

    data = data.dropna()
    trainData = data.iloc[:, 2:3].values

    sc = MinMaxScaler(feature_range=(0, 1))
    trainData = sc.fit_transform(trainData)

    num_rows = len(trainData)

    x_train = []
    y_train = []

    for i in range(60, num_rows):
        x_train.append(trainData[i-60:i, 0])
        y_train.append(trainData[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    
    model = load_model(previous_model_file)
    
    hist = model.fit(x_train, y_train, epochs=20, batch_size=32, verbose=2)

    # Save the model to the "modals" folder
    model_folder = "modals"
    model_filename = os.path.splitext(os.path.basename(csv_file))[0] + '.h5'
    model_path = os.path.join(model_folder, model_filename)
    model.save(model_path)

# Main folder path where CSV files are present
main_folder_path = "minute"
csv_files = [f for f in os.listdir(main_folder_path) if f.endswith(".csv")]

previous_model = "modals/3IINFOLTD.h5"  

for csv_file in csv_files:
    csv_file_path = os.path.join(main_folder_path, csv_file)
    train_and_save_model(csv_file_path, previous_model)
    # Update the previous_model for the next iteration
    previous_model = os.path.join("modals", os.path.splitext(os.path.basename(csv_file))[0] + '.h5')

