import math
from functools import partial
from tkinter import *
from tkinter import simpledialog
from MBox import Mbox
from StateDiagram_CUI import StateDiagram


class Node:
    def __init__(self, parent, canvas, id, label, initial, final):
        # canvas properties
        self.canvas = canvas
        self.parent = parent

        #  state (node) properties
        self.id = id
        self.label = label
        self.boundOut = []
        self.boundIn = []
        self.loop = []
        self.isInitial = initial
        self.isFinal = final

        # node properties - graph
        self.anchor = canvas.create_oval(22 + 250, 2 + 250, 27 + 250, 7 + 250, fill='black', tags=f"{self.id}_node")
        self.node = canvas.create_oval(2 + 250, 2 + 10 + 250, 50 + 250, 50 + 10 + 250, fill='white',
                                       tags=(self.id, f"{self.id}_node"))
        self.text = canvas.create_text(24 + 250, 24 + 10 + 250, text=label, tags=(self.id, f"{self.id}_node"))
        self.initial = None
        self.initialText = None
        self.final = None

        if final:
            self.make_final((2 + 250, 2 + 10 + 250, 50 + 250, 50 + 10 + 250))
        if initial:
            self.make_initial((2 + 250, 2 + 10 + 250, 50 + 250, 50 + 10 + 250))

        self.m = Menu(parent.master, tearoff=0)
        self.m.add_command(label="Self Loop", command=self.self_loop)
        self.m.add_command(label="Re-Config", command=self.change_config)
        self.m.add_command(label="Delete", command=self.delete)

        canvas.tag_bind(self.anchor, '<Enter>', self.anchor_hover)
        canvas.tag_bind(self.anchor, '<Leave>', self.anchor_hover_stop)
        canvas.tag_bind(self.anchor, '<Button-1>', self.drag_start)
        canvas.tag_bind(self.anchor, '<B1-Motion>', self.drag_motion)
        canvas.tag_bind(self.anchor, '<ButtonRelease-1>', self.drag_stop)
        canvas.tag_bind(self.id, "<ButtonPress-1>", partial(parent.conn_start, self))
        canvas.tag_bind(self.id, "<ButtonRelease-1>", partial(parent.conn_stop, self))
        canvas.tag_bind(self.id, "<B1-Motion>", partial(parent.conn_motion, self))
        canvas.tag_bind(self.id, "<Button-3>", self.do_popup)

    def add(self, enter=None, out=None, loop=None):
        if enter:
            self.boundIn.append(enter)
        if out:
            self.boundOut.append(out)
        if loop:
            self.loop.append(loop)

    def remove(self, enter=None, out=None, loop=None):
        if enter:
            self.boundIn.remove(enter)
        if out:
            self.boundOut.remove(out)
        if loop:
            self.loop.remove(loop)

    def make_initial(self, coords=None):
        self.parent.modify(initial=self)
        (x, y, x0, y0) = coords if coords else self.canvas.coords(self.node)
        self.initial = self.canvas.create_line(x - 50, y + 24, x, y + 24, arrow=LAST,
                                               tags=(self.id, f"{self.id}_node"))
        self.initialText = self.canvas.create_text(x - 25, y + 15, text='$', tags=(self.id, f"{self.id}_node"))

    def del_initial(self):
        self.parent.modify(initial=None)
        self.canvas.delete(self.initial)
        self.canvas.delete(self.initialText)

    def make_final(self, coords=None):
        (x, y, x0, y0) = coords if coords else self.canvas.coords(self.node)
        self.final = self.canvas.create_oval(x + 5, y + 5, x0 - 5, y0 - 5, tags=(self.id, f"{self.id}_node"))

    def del_final(self):
        self.canvas.delete(self.final)

    def do_popup(self, event):
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def self_loop(self):
        label = simpledialog.askstring(title="Transition Name", prompt="Enter the terminal:")
        if not label or label == '':
            return
        if self.loop:
            self.loop[0].change_name(f"{self.loop[0].label}+{label}")
        else:
            loop = Loop(self.parent, self.canvas, label, self.canvas.coords(self.node), self)
            self.add(loop=loop)
            self.parent.add_loop(loop)

    def change_config(self):
        d = {'name': self.label, 'initial': self.isInitial, 'final': self.isFinal}
        while True:
            self.parent.master.wait_window(
                Mbox(self.parent.master, "State Name", "Enter the State Name:", (d, 'name', 'initial', 'final')).top)
            if not (d['name'] != self.label and d['name'] in [q.label for q in self.parent.nodes.values()]) \
                    and not (d['initial'] != self.isInitial and d['initial'] and self.parent.initial is not None and
                             self.parent.initial != self):
                break
            d = {'name': self.label, 'initial': self.isInitial, 'final': self.isFinal}

        if d['initial'] != self.isInitial:
            self.make_initial() if d['initial'] else self.del_initial()
            self.isInitial = d['initial']

        if d['final'] != self.isFinal:
            self.make_final() if d['final'] else self.del_final()
            self.isFinal = d['final']

        if d['name'] != self.label:
            self.label = d['name']
            self.canvas.itemconfig(self.text, text=self.label)

    def delete(self):
        self.parent.remove(self)
        arrows = list(self.boundIn)
        for arrow in arrows:
            arrow.delete()
        arrows = list(self.boundOut)
        for arrow in arrows:
            arrow.delete()
        loops = list(self.loop)
        for loop in loops:
            loop.delete()
        del arrows
        del loops
        self.canvas.delete(self.node)
        self.canvas.delete(self.anchor)
        self.canvas.delete(self.text)
        if self.isInitial:
            self.del_initial()
        if self.isFinal:
            self.del_final()

    def has_link(self, node):
        for arrow in self.boundOut:
            if arrow.end == node:
                return arrow
        return None

    def anchor_hover(self, event):
        self.canvas.config(cursor="fleur")

    def anchor_hover_stop(self, event):
        self.canvas.config(cursor="arrow")

    def drag_start(self, event):
        self.canvas.config(cursor="fleur")
        widget = event.widget
        widget.startX = event.x
        widget.startY = event.y

    def drag_motion(self, event):
        self.canvas.config(cursor="fleur")
        widget = event.widget
        widget.move(f"{self.id}_node", event.x - widget.startX, event.y - widget.startY)
        (x0, y0, x1, y1) = self.canvas.coords(self.node)
        for arrow in self.boundIn:
            (x, y, x1, y1) = self.canvas.coords(arrow.part[0])
            arrow.move([x, y], [x0 + 24, y0 + 24])
        for arrow in self.boundOut:
            (x1, y1, x, y) = self.canvas.coords(arrow.part[1])
            arrow.move([x0 + 24, y0 + 24], [x, y])
        for loop in self.loop:
            loop.move(event.x - widget.startX, event.y - widget.startY)
        widget.startX, widget.startY = event.x, event.y

    def drag_stop(self, event):
        self.canvas.config(cursor="arrow")


class Loop:
    def __init__(self, parent, canvas, label, coords, node):
        self.parent = parent
        self.canvas = canvas
        self.label = label
        self.node = node

        (x, y, x0, y0) = coords
        self.loop = self.canvas.create_oval(x, y - 30, x0, y0 - 30)
        self.arrow = self.canvas.create_line((x + x0) / 2 + 2, y - 30, (x + x0) / 2 + 4, y - 30, arrow=LAST)
        self.text = self.canvas.create_text((x + x0) / 2, y - 40, text=label)
        self.canvas.tag_lower(self.loop)
        self.canvas.tag_lower(self.arrow)
        self.canvas.tag_lower(self.text)
        self.canvas.tag_bind(self.loop, "<Button-3>", self.do_popup)
        self.canvas.tag_bind(self.arrow, "<Button-3>", self.do_popup)
        self.canvas.tag_bind(self.text, "<Button-3>", self.do_popup)

        self.m = Menu(parent.master, tearoff=0)
        self.m.add_command(label="Rename", command=self.change_name)
        self.m.add_command(label="Delete", command=self.delete)

    def do_popup(self, event):
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def change_name(self, label=''):
        while (label is None and self.label == '') or label == '':
            label = simpledialog.askstring(title="Transition Name", prompt="Enter the terminal:",
                                           initialvalue=self.label)
        if label:
            self.label = label
            self.canvas.itemconfig(self.text, text=self.label)

    def move(self, delta_x, delta_y):
        self.canvas.move(self.loop, delta_x, delta_y)
        self.canvas.move(self.arrow, delta_x, delta_y)
        self.canvas.move(self.text, delta_x, delta_y)

    def delete(self):
        self.destroy_symbol()
        self.node.remove(loop=self)
        self.parent.remove(self)

    def destroy_symbol(self):
        self.canvas.delete(self.loop)
        self.canvas.delete(self.arrow)
        self.canvas.delete(self.text)


class Arrow:
    def __init__(self, parent, canvas):
        # canvas properties
        self.canvas = canvas
        self.parent = parent

        #  terminal (link) properties
        self.label = ""
        self.st = None
        self.end = None

        # arrow properties - graph
        self.part = [None, None]
        self.text = None

        self.m = Menu(parent.master, tearoff=0)
        self.m.add_command(label="Rename", command=self.change_name)
        self.m.add_command(label="Delete", command=self.delete)

    def do_popup(self, event):
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def start(self, node, event):
        widget = event.widget
        (x, y, x0, y0) = widget.coords(node.node)
        widget.startX = x + 24
        widget.startY = y + 24
        self.create((widget.startX, widget.startY), node)

    def create(self, coords, node):
        self.st = node
        self.part[0] = self.canvas.create_line(coords[0], coords[1], coords[0], coords[1], arrow=LAST)
        self.part[1] = self.canvas.create_line(coords[0], coords[1], coords[0], coords[1])
        self.text = self.canvas.create_text(coords[0], coords[1], text=self.label)
        self.canvas.tag_bind(self.part[0], "<Button-3>", self.do_popup)
        self.canvas.tag_bind(self.part[1], "<Button-3>", self.do_popup)
        self.canvas.tag_bind(self.text, "<Button-3>", self.do_popup)

    def motion(self, event):
        widget = event.widget
        self.move([widget.startX, widget.startY], [event.x, event.y])
        self.canvas.tag_lower(self.part[0])
        self.canvas.tag_lower(self.part[1])

    def move(self, start, end):
        x0 = (start[0] + 2*end[0])/3
        y0 = (start[1] + 2*end[1])/3
        self.canvas.coords(self.part[0], start[0], start[1], x0, y0)
        self.canvas.coords(self.part[1], x0, y0, end[0], end[1])
        denominator = float('inf') if end[0] == start[0] else end[0] - start[0]
        pos = 1 if math.cos(math.atan((end[1] - start[1]) / denominator)) >= 0 else -1
        self.canvas.coords(self.text, x0 + pos * 10, y0 + pos * 10)

    def stop(self, event):
        widget = event.widget
        canvasx = widget.canvasx(event.x)
        canvasy = widget.canvasy(event.y)
        item_tags = widget.itemcget(widget.find_closest(canvasx, canvasy)[0], "tags").split(' ')
        widget.startX = None
        widget.startY = None
        print(type(item_tags))
        return item_tags

    def set_end(self, node):
        self.end = node
        node.add(enter=self)

    def change_name(self, label=''):
        while (label is None and self.label == '') or label == '':
            label = simpledialog.askstring(title="Transition Name", prompt="Enter the terminal:",
                                           initialvalue=self.label)
        if label:
            self.label = label
            self.canvas.itemconfig(self.text, text=self.label)
            self.canvas.tag_lower(self.text)

    def delete(self):
        self.destroy_symbol()
        self.st.remove(out=self)
        self.end.remove(enter=self)
        self.parent.remove(self)

    def destroy_symbol(self):
        self.canvas.delete(self.part[0])
        self.canvas.delete(self.part[1])
        self.canvas.delete(self.text)


class MyFirstGUI:
    def __init__(self, master):
        print("init-GUI")
        # canvas properties
        self.master = master
        master.title("A simple GUI")
        self.add_button = Button(master, text="Add State", command=self.add_node, cursor='hand2')
        self.add_button.place(x=0, y=0)
        self.check_button = Button(master, text="Check", command=self.print_all, cursor='hand2')
        self.check_button.place(x=100, y=0)
        self.canvas = Canvas(master, width=master.winfo_screenwidth() * 2 / 3,
                             height=master.winfo_screenheight() * 1 / 2, borderwidth=0, highlightthickness=0)
        self.canvas.create_rectangle(0, 0, master.winfo_screenwidth() * 2 / 3 - 1,
                                     master.winfo_screenheight() * 1 / 2 - 1)
        self.canvas.pack()

        self.define_button = Button(master, text="Define Automata", command=self.define, cursor='hand2')
        self.define_button.pack()
        self.clear_button = Button(master, text="Clear", command=self.clear, cursor='hand2')
        self.clear_button.pack()

        self.machine = Text(master)
        self.machine.insert(INSERT, "No Machine defined yet.")
        self.machine.pack()
        self.machine.bind("<Key>", lambda e: "break")
        self.item_count = 0

        # graph properties
        self.objs = []
        self.nodes = {}
        self.arrows = []
        self.loops = []
        self.initial = None
        self.arrow = None

        self.sd = StateDiagram()

    def gen_id(self, type):
        self.item_count += 1
        return f"{type}{self.item_count}"

    def clear(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.master.winfo_screenwidth() * 2 / 3 - 1,
                                     self.master.winfo_screenheight() * 1 / 2 - 1)
        self.objs = []
        self.nodes = {}
        self.arrows = []
        self.loops = []
        self.initial = None
        self.arrow = None
        self.item_count = 0
        self.machine.delete('1.0', END)
        self.machine.insert(INSERT, "No Machine defined yet.")

    def print_all(self):
        text = f"self.master : {self.master}\n" \
               f"self.objs : {self.objs}\n" \
               f"self.nodes : {self.nodes}\n" \
               f"self.arrows : {self.arrows}\n" \
               f"self.loops : {self.loops}\n" \
               f"self.canvas : {self.canvas}\n" \
               f"self.initial : {self.initial}\n" \
               f"self.arrow : {self.arrow}\n\n" \
               f"canvas items : {self.canvas.find_all()}\n\n"
        for node in self.objs:
            text += f"node object : {node}\n" \
                    f"node.canvas : {node.canvas}\n" \
                    f"node.label : {node.label}\n" \
                    f"node.anchor : {node.anchor}\n" \
                    f"node.node : {node.node}\n" \
                    f"node.text : {node.text}\n" \
                    f"node.parent : {node.parent}\n" \
                    f"node.isInitial : {node.isInitial}\n"
            if node.isInitial:
                text += f"node.initial : {node.initial}\n" \
                        f"node.initialText : {node.initialText}\n"
            text += f"node.isFinal : {node.isFinal}\n"
            if node.isFinal:
                text += f"node.final : {node.final}\n"
            text += f"node.boundIn : {node.boundIn}\n" \
                    f"node.boundOut : {node.boundOut}\n" \
                    f"node.loop : {node.loop}\n\n"
        for arrow in self.arrows:
            text += f"arrow object : {arrow}\n" \
                    f"arrow.canvas : {arrow.canvas}\n" \
                    f"arrow.label : {arrow.label}\n" \
                    f"arrow.text : {arrow.text}\n" \
                    f"arrow.parent : {arrow.parent}\n" \
                    f"arrow.part : {arrow.part}\n" \
                    f"arrow.st : {arrow.st}\n" \
                    f"arrow.end : {arrow.end}\n\n"
        for loop in self.loops:
            text += f"loop.object : {loop}\n" \
                    f"loop.canvas : {loop.canvas}\n" \
                    f"loop.label : {loop.label}\n" \
                    f"loop.parent : {loop.parent}\n" \
                    f"loop.node : {loop.node}\n" \
                    f"loop.loop : {loop.loop}\n" \
                    f"loop.arrow : {loop.arrow}\n" \
                    f"loop.text : {loop.text}\n\n"
        print(text)

    def add_node(self):
        print("AddNode")
        d = {'name': '', 'initial': False, 'final': False}
        self.master.wait_window(
            Mbox(self.master, "State Name", "Enter the State Name:", (d, 'name', 'initial', 'final')).top)
        print(d['name'], type(d['name']))
        print(d['initial'])
        print(d['final'])
        if d['name'] == '' or d['name'] in [q.label for q in self.nodes.values()] or (d['initial'] and self.initial is not None):
            return
        node = Node(self, self.canvas, self.gen_id("Node"), d['name'], d['initial'], d['final'])
        self.nodes[node.id] = node
        self.objs.append(node)

    def modify(self, initial):
        self.initial = initial

    def remove(self, obj):
        obj_type = type(obj)
        if obj_type == Node:
            self.objs.remove(obj)
            del self.nodes[obj.id]
        elif obj_type == Arrow:
            self.arrows.remove(obj)
        elif obj_type == Loop:
            self.loops.remove(obj)

    def add_loop(self, loop):
        self.loops.append(loop)

    def conn_start(self, node, event):
        print("GUI Arrow Start")
        self.arrow = Arrow(self, self.canvas)
        self.arrow.start(node, event)

    def conn_motion(self, node, event):
        print("GUI Arrow Motion")
        self.arrow.motion(event)

    def conn_stop(self, node, event):
        print("GUI Arrow Stop")
        item = self.arrow.stop(event)
        print(item)
        if item[0] == node.id or item[0] not in self.nodes.keys():
            self.arrow.destroy_symbol()
            del self.arrow
        else:
            label = simpledialog.askstring(title="Transition Name", prompt="Enter the terminal:")
            if not label or label == '':
                self.arrow.destroy_symbol()
                del self.arrow
            else:
                a = self.arrow.st.has_link(self.nodes[item[0]])
                if a:
                    a.change_name(f"{a.label}+{label}")
                    self.arrow.destroy_symbol()
                    del self.arrow
                else:
                    node.add(out=self.arrow)
                    self.arrow.set_end(self.nodes[item[0]])
                    self.arrow.change_name(label)
                    self.arrows.append(self.arrow)
        self.arrow = None

    def define(self):
        self.machine.delete('1.0', END)
        if not self.objs:
            self.machine.insert(INSERT, "No state found.")
            return
        if self.initial is None:
            self.machine.insert(INSERT, "No initial state defined.")
            return
        Q = []
        F = []
        for q in self.nodes.values():
            Q.append(q.label)
            if q.isFinal and q.boundIn:
                F.append(q.label)
        if not F:
            self.machine.insert(INSERT, "Final state not defined or not reachable.")
            return

        Sigma = []
        d = []
        transitions = f"\nd({self.initial.label}, $) = {self.initial.label}"
        for arrow in self.arrows:
            if arrow.label not in Sigma:
                Sigma.append(arrow.label)
            d.append([arrow.st.label, arrow.label, arrow.end.label])
            # transitions += f"\n{arrow.st.label} : {arrow.label} > {arrow.end.label}"
            transitions += f"\nd({arrow.st.label}, {arrow.label}) = {arrow.end.label}"
        for loop in self.loops:
            if loop.label not in Sigma:
                Sigma.append(loop.label)
            d.append([loop.node.label, loop.label, loop.node.label])
            # transitions += f"\n{loop.node.label} : {loop.label} > {loop.node.label}"
            transitions += f"\nd({loop.node.label}, {loop.label}) = {loop.node.label}"
        q0 = self.initial.label
        self.sd.clear()
        self.sd.input((Q, Sigma, d, q0, F))
        self.machine.insert(INSERT, f"Machine M : (Q, Sigma, Transition Function, q0, F)\n"
                                    f"States Q : {Q}\n"
                                    f"Terminals Sigma : {Sigma}\n"
                                    f"Transition Function :{transitions}\n"
                                    f"Initial state q0 : {q0}\n"
                                    f"Final state(s) F : {F}\n"
                                    f"State Equations :\n{self.sd.get_Equations()}\n")

        a = self.sd.genRegEx()
        print(a)
        self.machine.insert(INSERT, f"Regex:\n{a}")


if __name__ == '__main__':
    root = Tk()
    root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight()))
    my_gui = MyFirstGUI(root)
    root.mainloop()
