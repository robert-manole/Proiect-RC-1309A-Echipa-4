# from tkinter import *
from mttkinter import mtTkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

class GUI:
    root = tk.Tk()


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
        for child in self.root.winfo_children():
            child.destroy()
        self.createClientGUI()

    def createClientGUI(self):

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

        chosen_topic_publish = tk.StringVar()
        topic_combobox = ttk.Combobox(publish_frame, textvariable=chosen_topic_publish)
        topic_combobox['values'] = ('CpuInfo', 'CpuUsage', 'MemoryInfo', 'DiskInfo')
        topic_combobox.grid(column=1, row=1)
        topic_combobox.current()

        QoS_Option = tk.StringVar()

        ttk.Button(publish_frame, text="Publish", command=lambda:self.client.publish(chosen_topic_publish.get(), int(QoS_Option.get()))).grid(column=1, row=2)

        ttk.Radiobutton(publish_frame, text="QoS 0", variable=QoS_Option, value=0).grid(column=1, row=3)
        ttk.Radiobutton(publish_frame, text="QoS 1", variable=QoS_Option, value=1).grid(column=1, row=4)
        ttk.Radiobutton(publish_frame, text="QoS 2", variable=QoS_Option, value=2).grid(column=1, row=5)

        # subscriber frame
        subscribe_frame.columnconfigure(0, weight=1)
        subscribe_frame.columnconfigure(1, weight=1)
        subscribe_frame.columnconfigure(2, weight=1)

        ttk.Label(subscribe_frame, text="Topics", font=("Arial", 15)).grid(column=1, row=0, pady=(60, 8))

        chosen_topic_subscribe = tk.StringVar()
        topic_combobox = ttk.Combobox(subscribe_frame, textvariable=chosen_topic_subscribe)
        topic_combobox['values'] = ('CpuInfo', 'CpuUsage', 'MemoryInfo', 'DiskInfo')
        topic_combobox.grid(column=1, row=1)
        topic_combobox.current()


        text_subs = tk.Text(subscribe_frame, height=5, width=52)
        text_subs.grid(column=1, row=5)
        text_subs.config(state='disabled')

        msg_text = ScrolledText(subscribe_frame, height=5, width=52)
        msg_text.grid(column=1, row=6)
        msg_text.config(state='disabled')

        ttk.Button(subscribe_frame, text="Subscribe", command=lambda: self.client.subscribe(chosen_topic_subscribe.get(), msg_text, text_subs)).grid(
            column=1, row=3)
        ttk.Button(subscribe_frame, text="Unsubscribe",
                   command=lambda: self.client.unsubscribe(chosen_topic_subscribe.get(), text_subs)).grid(
            column=1, row=4)















