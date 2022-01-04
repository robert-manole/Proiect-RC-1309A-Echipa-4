from Client import Client
from GUI import GUI
from random import randint


if __name__ == "__main__":
    id = randint(1, 100000)
    client = Client(id)
    gui = GUI(client)
    gui.root.mainloop()




