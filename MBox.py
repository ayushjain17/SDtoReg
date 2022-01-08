from tkinter import *

class Mbox(object):

    def __init__(self, parent, title, msg, dict_key=None):
        """
        msg = <str> the message to be displayed
        dict_key = <sequence> (dictionary, key) to associate with user input
        (providing a sequence for dict_key creates an entry for user input)
        """
        self.top = Toplevel(parent)
        self.top.title(title)
        frm = Frame(self.top, borderwidth=4, relief='ridge')
        frm.pack(fill='both', expand=True)
        label = Label(frm, text=msg)
        label.pack(padx=4, pady=4)

        if dict_key is not None:
            d, key, key2, key3 = dict_key
            self.entry = Entry(frm)
            self.entry.insert(0, d[key])
            self.entry.focus_set()
            self.entry.pack(pady=4)

            self.initial = IntVar()
            self.final = IntVar()
            self.initial.set(int(d[key2]))
            self.final.set(int(d[key3]))
            # set and get the value of this variable
            checkButton1 = Checkbutton(frm, text="Initial", variable=self.initial)
            checkButton2 = Checkbutton(frm, text="Final", variable=self.final)
            checkButton1.pack()
            checkButton2.pack()

            b_submit = Button(frm, text='Okay')
            b_submit['command'] = lambda: self.entry_to_dict(d, key, key2, key3)
            b_submit.pack()

        b_cancel = Button(frm, text='Cancel')
        b_cancel['command'] = self.top.destroy
        b_cancel.pack(padx=4, pady=4)

    def entry_to_dict(self, d, key, key2, key3):
        data = self.entry.get()
        if data:
            d[key] = data
            d[key2] = self.initial.get() == 1
            d[key3] = self.final.get() == 1
            self.top.destroy()
