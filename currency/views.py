import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from django.http import HttpResponse

def do(request):
    # Генерируем случайные данные о курсах валют в диапазоне от 80 до 100
    data = np.random.uniform(low=80, high=100, size=(1000,))

    # Подготовка данных для LSTM модели
    def prepare_data(data, time_steps):
        X, y = [], []
        for i in range(len(data) - time_steps):
            X.append(data[i:(i + time_steps)])
            y.append(data[i + time_steps])
        return np.array(X), np.array(y)

    time_steps = 10
    X, y = prepare_data(data, time_steps)

    # Определение архитектуры LSTM модели
    model = Sequential([
        Input(shape=(time_steps, 1)),
        LSTM(50),
        Dense(1)
    ])

    # Компиляция модели
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Обучение модели
    model.fit(X.reshape(-1, time_steps, 1), y, epochs=50, batch_size=32, verbose=1)

    # Сделать предсказание следующего значения курса валюты
    last_sequence = data[-time_steps:].reshape(1, time_steps, 1)
    prediction = model.predict(last_sequence)[0][0]

    # Возвращаем предсказанное значение
    return HttpResponse("Predicted exchange rate: {}".format(prediction).encode('utf-8'))
