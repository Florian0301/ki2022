from json import load
from pprint import pprint
from math import pow
from functools import reduce


def context_manager():
    # Aufgabe 1
    with open("praktikum1/fruits.json") as file:
        data = load(file)
        pprint(data)
        for x in data:
            for (key, value) in x.items():
                print(f"{key}: {value}")
    print(file.closed)


def generator(n):
    # Aufgabe 2
    counter = 1
    for i in range(1, n):
        counter *= i
        yield counter


def generator_expressions():
    # Aufgabe 3
    n = 100
    folge = [x+1 for x in range(n)]
    gen = (x+1 for x in range(n))
    pprint(folge)
    i = 0
    for item in gen:
        pprint(item)
        i+=1
        print(i)


def list_manipulation():
    # Aufgabe 4
    liste = range(1, 10+1)  # 1-10
    n = len(liste)
    summe = reduce(lambda a, b: b, liste) / n
    print(summe)


if __name__ == "__main__":
    print("------ Aufgabe 1")
    context_manager()
    print("------ Aufgabe 2")
    gen = generator(10)
    for item in gen:
        pprint(item)
    print("------ Aufgabe 3")
    generator_expressions()
    print("------ Aufgabe 4")
    list_manipulation()
