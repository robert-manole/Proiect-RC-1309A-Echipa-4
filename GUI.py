from tkinter import *
from tkinter import ttk

class GUI:
    root = Tk()

    def __init__(self, client):

        self.client = client

        self.root.title("Client")
        self.root.geometry("300x300")
        self.root.resizable(False, False)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        ttk.Label(text="Username", font=("Arial", 15)).grid(column=1, row=1, padx=0, pady=(60, 8))
        username_entry = ttk.Entry()
        username_entry.grid(column=1, row=2)

        ttk.Label(text="Password", font=("Arial", 15)).grid(column=1, row=3, padx=0, pady=8)
        password_entry = ttk.Entry(show="*")
        password_entry.grid(column=1, row=4)

        ttk.Button(text="Login", command=lambda: self.onLogin(username_entry.get(), password_entry.get())).grid(column=1, row=5, padx=10, pady=10)

        # self.root.mainloop()

    def onLogin(self, username, password):
        self.client.connect(username, password)
        self.root.destroy()
        self.createClientGUI()

    def createClientGUI(self):
        self.root = Tk()
        self.root.title("Client " + str(self.client.getId()))
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        ttk.Label(text="Topics", font=("Arial", 15)).grid(column=1, row=0, pady=(60, 8))

        chosen_topic = StringVar()
        topic_combobox = ttk.Combobox(self.root, textvariable=chosen_topic)
        topic_combobox['values'] = ('CpuInfo', 'CpuUsage', 'MemoryInfo', 'DiskInfo')
        topic_combobox.grid(column=1, row=1)
        topic_combobox.current()

        ttk.Button(text="Publish", command=lambda: self.client.publish(chosen_topic.get())).grid(column=1, row=2)
        ttk.Button(text="Subscribe", command=lambda: self.client.subscribe(chosen_topic.get())).grid(column=1, row=3)


