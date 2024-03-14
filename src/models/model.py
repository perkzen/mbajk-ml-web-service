from keras import Sequential
from keras.layers import Dense, GRU, Dropout, Input
from keras.optimizers import Adam


def build_model(input_shape):
    model = Sequential(name="GRU")

    model.add(Input(shape=input_shape))
    model.add(GRU(units=128, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(GRU(units=64, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(GRU(units=32))

    model.add(Dense(units=32, activation="relu"))
    model.add(Dense(units=1))

    optimizer = Adam(learning_rate=0.01)
    model.compile(optimizer=optimizer, loss="mean_squared_logarithmic_error")

    return model
