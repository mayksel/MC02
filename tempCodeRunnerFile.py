    if self.slots == self.n:
                print("Empty fitting room. ", other_count)
                if(other_count != 0):
                    print("Other")
                    other_turn.set()  # Signal the other color to enter
                else:
                    print("Own")
                    own_turn.set()