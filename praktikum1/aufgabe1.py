


def fibo(n) -> int:
    if(n <= 1):
        return n
    else:
        return fibo(n-1)+fibo(n-2)

def number_guessing() -> None:
    solution = 20
    guess = 0
    while guess != solution:
        try:
            guess = int(input("Enter guess: "))
        except ValueError:
           print("No number!")
    print("Guess correct!")

class Car(object):
    def __init__(self) -> None:
        self.Motor = False

    def Start_Car(self) -> None:
        if not self.Motor:
            self.Motor = True
            print("Car started")
        else:
            print("Car already running")
        
    
    def Stop_Car(self) -> None:
        if self.Motor:
            self.Motor = False
            print("Car stopped")
        else:
            print("Car already stopped")

    def Drive(self) -> None:
        if self.Motor:
            print("Drive")
        else:
            print("Car not started yet")

class Polo(Car):

    def Drive(self) -> None:
        if self.Motor:
            print("Drive")
        else:
            print("Polo not started yet")
    
    def __private_method(self) -> None:
        print("hi im private!")

    def public_method(self) -> None:
        print("hi im public and i can call private!")
        self.__private_method()



if __name__ == "__main__":
    car = Car()
    polo = Polo()

    polo.Drive()
    car.Drive()
    polo.Start_Car()
    polo.public_method()
    try:
        polo.__private_method()
    except AttributeError as e:
        print(e)

    
    for i in range(20):
        print(fibo(i))

    number_guessing()

