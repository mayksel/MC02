from threading import BoundedSemaphore, Thread
import time

#use room
#consumes 1 instance of the semaphore, which is used to store available slots in the room.
#releases after fitting is completed and outputs a message saying such.
def use_room(sema, thread_no, color): #acquire the sema then print the color and thread number then release sema
  sema.acquire()
  print(f"A {color} using thread {thread_no} is changing in the room.")
  time.sleep(2)
  sema.release()
  print(f"{color} at thread {thread_no} left the room.")


def main():
  # input from user
  n, b, g = list(map(int, input().rstrip().split(" ")))

  # Create n fitting room/s
  roomSema = BoundedSemaphore(n)

  #alternate turns in the fitting rooms
  turn = True  #blue starts first
  hasQueue = True

  # Round Robin style scheduling for green and blues
  # n is used to also set up how many of a color can use the room at a time
  while hasQueue:
    waiting = []

    if turn:  #If blue's turn
      print("Blue Only")

      if b == 0:  #No more blues left
        print("All blues have used the fitting room!")

      else: #Make blues then start
        for y in range(0, min(n, b)):
          t = Thread(target=use_room, args=(roomSema, y, "Blue"))
          t.start()
          waiting.append(t)

        #Wait for this thread batch to finish & decrement b
        for t in waiting:
          t.join()
          b -= 1

        print("Empty Fitting Rooms")

    elif ~turn:  #If green's turn
      print("Green Only")

      if g == 0:  #No more greens left
        print("All greens have used the fitting room!")

      else:
        for y in range(0, min(n, g)): #Make greens then start
          t = Thread(target=use_room, args=(roomSema, y, "Green"))
          t.start()
          waiting.append(t)

        #Wait for this batch to finish & decrement g
        for t in waiting:
          t.join()
          g -= 1

        print("Empty Fitting Room")

    #Alternate the turns
    turn ^= True

    if b == 0 and g == 0:  #End the loop if no more blues and greens
      hasQueue = False
      print("Everybody has used the fitting room.")


      main()