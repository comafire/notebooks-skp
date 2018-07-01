import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import Conv2D, MaxPooling2D, Flatten
from keras import optimizers

def create_dnn(n_input, n_class, lr=0.001, dropout_rate=0.5):
    model = Sequential()
    model.add(Dense(256, input_shape=(n_input,), kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform'))
    model.add(Activation('relu'))
    model.add(Dense(128, input_shape=(256,), kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform'))
    model.add(Activation('relu'))

    model.add(Dense(n_class * 2, input_shape=(128,), kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform'))
    model.add(Activation('relu'))
    
    model.add(Dropout(dropout_rate))
    model.add(Dense(n_class, activation='softmax'))

    optimizer = optimizers.Adam(lr=lr)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    return model

def create_cnn(input_shape, n_class, lr=0.001, dropout_rate=0.5):
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape,
                     kernel_initializer='glorot_uniform'))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu',
                     kernel_initializer='glorot_uniform'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu', kernel_initializer='glorot_uniform'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(n_class, activation='softmax',
                    kernel_initializer='glorot_uniform', bias_initializer='glorot_uniform'))

    optimizer = optimizers.Adam(lr=lr)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    return model