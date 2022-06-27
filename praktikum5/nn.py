from pprint import pprint
import tensorflow as tf
import numpy as np
mnist = tf.keras.datasets.mnist

DEBUG = True


def trenner():
    print("\n" + "=-" * 80 + "=\n")


def test_model(model: tf.keras.models.Sequential):

    # Datensatz laden
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    if DEBUG:
        print("Vorher:")
        pprint(x_train[0])
        trenner()

    # Anschließend werden die Integer (0-255) zu Floating Point Zahlen (0.0-1.0) konvertiert, Normierung
    x_train, x_test = x_train / 255.0, x_test / 255.0
    if DEBUG:
        print("Nachher:")
        pprint(x_train[0])
        trenner()

    # 6:1 Verhaeltnis
    if DEBUG:
        print("6 zu 1:")
        print("Train:", x_train.shape)
        print("Test:", x_test.shape)
        trenner()

    # 3:1 Verhaeltnis
    x = np.concatenate((x_train, x_test))
    y = np.concatenate((y_train, y_test))

    splitted_x = np.array_split(x, 4)
    splitted_y = np.array_split(y, 4)
    x_train = np.concatenate(
        (np.concatenate((splitted_x[0], splitted_x[1])), splitted_x[2]))
    y_train = np.concatenate(
        (np.concatenate((splitted_y[0], splitted_y[1])), splitted_y[2]))
    x_test = splitted_x[3]
    y_test = splitted_y[3]

    if DEBUG:
        print("3 zu 1:")
        print("Train:", x_train.shape)
        print("Test:", x_test.shape)
        trenner()

    # Das Model macht eine Prediction für die erste gezeichnete Zahl
    # Das Ergebnis (Output-Layer) ist die Bewertung pro Zahl bzw. der Inhalt pro Neuron im Output-Layer
    predictions = model(x_train[:1]).numpy()
    if DEBUG:
        print("Predictions:")
        print(f"{predictions = }", type(predictions))
        trenner()

    # Transformiert die Werte zu Wahrscheinlichkeiten
    # Die Summe aller Werte (Wahrscheinlichkeiten) ergibt also 1 (100%)
    softmax = tf.nn.softmax(predictions).numpy()
    if DEBUG:
        print("Softmax:")
        print(softmax)
        print(f"{sum(softmax[0]) = }")
        trenner()

    # Setze Loss Function.
    # Diese Berechnet die Abweichung vom tatsaechlichen Ergebnis (Der echten gezeichneten Zahl)
    # Der Loss sollte bei einem untrainierten Model initial ca. log(1/10) = 2.3 sein,
    # da die Wahrscheinlichkeit 1/10 ist, dass richtig geraten wird
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    loss = loss_fn(y_train[:1], predictions).numpy()
    if DEBUG:
        print("Loss:")
        print(f"{loss = }")
        trenner()

    # Setze die benoetigten Attribute fuer das Model:
    # Adam: Ein Optimizer nach dem Adam Algoritmus
    # Setze die generierte Loss Function
    # Metrik Accuracy: Gewichtet (Anzahl Richtiger Treffer) / (Anzahl Gesamte Inputs)
    model.compile(
        optimizer='adam',
        loss=loss_fn,
        metrics=['accuracy']
    )

    # Trainiere einmal mit allen Trainingsdaten in Fünf Epochen
    model.fit(x_train, y_train, epochs=5)

    # Checke die Performance
    # Pro Image: Ist Wahrheit = Model Prediction
    model.evaluate(x_test,  y_test, verbose=2)

    # Versehe das Model mit dem Softmax-Algorithmus
    probability_model = tf.keras.Sequential([
        model,
        tf.keras.layers.Softmax()
    ])

    # Printe, was tatsaechlich die erste gezeichnete Test Zahl ist
    print(f"{y_test[:1] = }")

    # Prediction des Models fuer diese Zahl
    print(f"{probability_model(x_test[:1]) = }")


if __name__ == "__main__":
    models = [
        # Ohne Hidden Layer
        tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10)
        ]),
        # 2 Hidden Layer, eines mit mindestens 16 Neuronen (NN2)
        tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(200, activation='relu'),
            tf.keras.layers.Dense(20),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10)
        ]),
        # 8 Hidden Layer, eines mit maximal 4 Neuronen
        tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(10, activation='relu'),
            tf.keras.layers.Dense(10),
            tf.keras.layers.Dense(10),
            tf.keras.layers.Dense(10),
            tf.keras.layers.Dense(10),
            tf.keras.layers.Dense(10),
            tf.keras.layers.Dense(10),
            tf.keras.layers.Dense(4),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10)
        ]),
        # NN2 mit hard sigmoid als Aktivierungsfunktion
        tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(200, activation='hard_sigmoid'),
            tf.keras.layers.Dense(20),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10)
        ]),
        # NN2 mit linear als Aktivierungsfunktion
        tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(200, activation='linear'),
            tf.keras.layers.Dense(20),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10)
        ])]

    test_model(models[1])
