from tkinter import *
# from StateDiagram_CUI import StateDiagram
#
#
# class StateDiagramWidget(Frame):
#     def __init__(self, master, width, height):
#         Frame.__init__(self, master)
#
#         # canvas properties
#         self.master = master
#         self.add_button = Button(text="Add State", command=self.add_node, cursor='hand2')
#         self.add_button.place(x=0, y=0)
#         self.check_button = Button(text="Check", command=self.print_all, cursor='hand2')
#         self.check_button.place(x=100, y=0)
#         self.canvas = Canvas(width=width, height=height, borderwidth=0, highlightthickness=0)
#         self.canvas.create_rectangle(0, 0, width - 1, height - 1)
#         self.canvas.pack()
#
#         self.define_button = Button(text="Define Automata", command=self.define, cursor='hand2')
#         self.define_button.pack()
#         self.clear_button = Button(text="Clear", command=self.clear, cursor='hand2')
#         self.clear_button.pack()
#
#         self.machine = Text(self)
#         self.machine.insert(INSERT, "No Machine defined yet.")
#         self.machine.pack()
#         self.machine.bind("<Key>", lambda e: "break")
#         self.item_count = 0
#
#         # graph properties
#         self.objs = []
#         self.nodes = {}
#         self.arrows = []
#         self.loops = []
#         self.initial = None
#         self.arrow = None
#
#         self.sd = StateDiagram()


class ScrolledText(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)
        self.text = Text(self, *args, **kwargs)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        # self.scrolled_text = ScrolledText(self)

        self.text = Text(self)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        # self.scrolled_text.pack(side="top", fill="both", expand=True)
        with open(__file__, "r") as f:
            self.text.insert("1.0", f.read())


root = Tk()
Example(root).pack(side="top", fill="both", expand=True)
root.mainloop()
