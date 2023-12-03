import threading
import time

class FittingRoom:
    def __init__(self, n):
        self.n = n
        self.slots = n
        self.blue_count = 0
        self.green_count = 0
        self.lock = threading.Lock()
        self.lock2 = threading.Lock()
        self.lock3 = threading.Lock()
        self.blue_semaphore = threading.Semaphore(n)
        self.green_semaphore = threading.Semaphore(n)
        self.blue_turn = threading.Event()
        self.green_turn = threading.Event()
        self.blue_turn_semaphore = threading.Semaphore(0)
        self.green_turn_semaphore = threading.Semaphore(0)

    def enter_room(self, thread_id, color):
        if color == "blue":
            semaphore = self.blue_semaphore
            turn_semaphore = self.blue_turn_semaphore
            self.blue_count += 1
            other_count = self.green_count
            turn_event = self.blue_turn
        elif color == "green":
            semaphore = self.green_semaphore
            turn_semaphore = self.green_turn_semaphore
            self.green_count += 1
            other_count = self.blue_count
            turn_event = self.green_turn
            

        with self.lock:
            if other_count > 0 or self.slots == 0:
                print(f"{color.capitalize()} thread {thread_id} is in the waiting room.")
                self.lock.release()
                turn_event.wait()  # Wait for the other color to finish entering
                turn_semaphore.acquire()
                self.lock.acquire()
                
            
            semaphore.acquire()
            self.slots -=1
            print(f"{color.capitalize()} only.")
            print(f"{color.capitalize()} thread {thread_id} entered. Slots left: {self.slots}")


        

    def exit_room(self, thread_id, color):
        if color == "blue":
            semaphore = self.blue_semaphore
            self.blue_count -= 1
            other_count = self.green_count
            other_turn = self.green_turn
            other_semaphore = self.green_turn_semaphore
            own_turn = self.blue_turn
            own_semaphore = self.blue_turn_semaphore
        elif color == "green":
            semaphore = self.green_semaphore
            self.green_count -= 1
            other_count = self.blue_count
            other_turn = self.blue_turn
            other_semaphore = self.blue_turn_semaphore
            own_turn = self.green_turn
            own_semaphore = self.green_turn_semaphore
        with self.lock2:
            semaphore.release()
            self.slots += 1
            print(f"{color.capitalize()} thread {thread_id} exited. Slots left: {self.slots}")

            if self.slots == self.n:
                print("Empty fitting room. ")
                if(other_count != 0):
                    other_turn.set()  # Signal the other color to enter
                    other_semaphore.release(n)
                else:
                    own_turn.set()
                    own_semaphore.release(n)


def simulate_fitting_room(n, b, g):
    fitting_room = FittingRoom(n)
    threads = []

    def thread_function(thread_id, color):
        fitting_room.enter_room(thread_id, color)
        time.sleep(5)  # Simulate thread inside fitting room
        fitting_room.exit_room(thread_id, color)

    for i in range(b):
        thread = threading.Thread(target=thread_function, args=(i, "blue"))
        threads.append(thread)

    for i in range(g):
        thread = threading.Thread(target=thread_function, args=(i + b, "green"))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

# Example usage
n = int(input("Enter the number of slots inside the fitting room: "))
b = int(input("Enter the number of blue threads: "))
g = int(input("Enter the number of green threads: "))

simulate_fitting_room(n, b, g)
