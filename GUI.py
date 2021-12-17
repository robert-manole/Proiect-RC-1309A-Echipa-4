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

        tabControl = ttk.Notebook(self.root)
        publish_frame = ttk.Frame(tabControl)
        subscribe_frame = ttk.Frame(tabControl)
        tabControl.add(publish_frame, text='Publisher')
        tabControl.add(subscribe_frame, text='Subscriber')
        tabControl.pack(expand=1, fill="both")

        # publisher frame
        publish_frame.columnconfigure(0, weight=1)
        publish_frame.columnconfigure(1, weight=1)
        publish_frame.columnconfigure(2, weight=1)

        ttk.Label(publish_frame, text="Topics", font=("Arial", 15)).grid(column=1, row=0, pady=(60, 8))

        chosen_topic_publish = StringVar()
        topic_combobox = ttk.Combobox(publish_frame, textvariable=chosen_topic_publish)
        topic_combobox['values'] = ('CpuInfo', 'CpuUsage', 'MemoryInfo', 'DiskInfo')
        topic_combobox.grid(column=1, row=1)
        topic_combobox.current()

        ttk.Button(publish_frame, text="Publish", command=lambda: self.client.publish(chosen_topic_publish.get())).grid(column=1, row=2)

        # subscriber frame
        subscribe_frame.columnconfigure(0, weight=1)
        subscribe_frame.columnconfigure(1, weight=1)
        subscribe_frame.columnconfigure(2, weight=1)

        ttk.Label(subscribe_frame, text="Topics", font=("Arial", 15)).grid(column=1, row=0, pady=(60, 8))

        chosen_topic_subscribe = StringVar()
        topic_combobox = ttk.Combobox(subscribe_frame, textvariable=chosen_topic_subscribe)
        topic_combobox['values'] = ('CpuInfo', 'CpuUsage', 'MemoryInfo', 'DiskInfo')
        topic_combobox.grid(column=1, row=1)
        topic_combobox.current()

        msg_text = Text(subscribe_frame, height=5, width=52)
        msg_text.grid(column=1, row=4)
        msg_text.config(state='disabled')

        ttk.Button(subscribe_frame, text="Subscribe", command=lambda: self.client.subscribe(chosen_topic_subscribe.get(), msg_text)).grid(
            column=1, row=3)

        # T.insert('1.0', "saluajsnda\n")
        # T.insert('1.0', " ALT TEXT\n")








