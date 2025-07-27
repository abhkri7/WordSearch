from grid import *
inp = ""
while inp != "quit":
    mygrid = Grid()
    mygrid.initialize("level.txt")
    inp = input("Press enter to see the answers:")
    mygrid.printGrid(True)
    inp = input("Press enter to the next problem or type 'quit' to exit: ")
