class Equation:
    def __init__(self, var, st):
        self.var = var
        self.st = st
        self.nextOpt = None
        self.next = None

    def add(self, opt, var, st):
        top = self
        while top.var != var and top.next is not None:
            top = top.next
        if top.var == var:
            top.st = f"({top.st}{opt}{st})"
        else:
            top.nextOpt = opt
            top.next = Equation(var, st)

    def substitute(self, name):
        top = self
        while top:
            if top.var != name:
                top.st = f"{self.var}"


    def ardenTheorem(self, name):
        top = self
        prev = None
        while top.var != name and top.next is not None:
            prev = top
            top = top.next
        if top.var == name:
            tmp = top.st
            if prev is None:
                self.__dict__.update(self.next.__dict__)
            else:
                prev.next = top.next
            self.printEqn(name)
            top = self
            while top is not None:
                top.st += f"({tmp})*"
                top = top.next

    def printEqn(self, name):
        s = f"{name} = ({self.var}){self.st}"
        top = self
        while top.next is not None:
            s += f" {top.nextOpt} "
            top = top.next
            s += f"({top.var}){top.st}"
        print(s)


class StateDiagram:
    def __init__(self):
        self.states = []
        self.terminals = []
        self.start = None
        self.final = []
        self.transition = {}

    def listInput(self, l):
        print("Enter N to stop")
        s = input()
        while s != "N":
            l.append(s)
            s = input()
        return l

    def inputTransition(self):
        print("Format : present:terminal>next")
        print("Enter N to stop")
        s = input()
        while s != 'N':
            s = s.replace('>', ':').split(':')
            if s[2] in self.transition:
                self.transition[s[2]].add('+', s[0], s[1])
            else:
                self.transition[s[2]] = Equation(s[0], s[1])
            s = input()
        self.transition[self.start].add('+', '$', '')

    def input(self):
        print("Enter the states:")
        self.listInput(self.states)
        print("Enter the terminals:")
        self.listInput(self.terminals)
        print("Enter the start symbol:")
        self.start = input()
        print("Enter the final state:")
        self.listInput(self.final)
        print("Enter the transition rules")
        self.inputTransition()

    def genRegEx(self):

        for i in self.final:
            self.transition[i].substitute()
            self.transition[i].ardenTheorem()

        s = self.final[0]
        for i in self.final[1:]:
            s += f" + {i}"
        s += f"{self.transition[0].st}"
        for i in self.final[1:]:
            s += f" + {self.transition[i].st}"

        print(s)

    def display(self):
        print(f"Q : {self.states}")
        print(f"Sigma : {self.terminals}")
        print("Transition Equations")
        for i in self.transition.keys():
            self.transition[i].printEqn(i)
            # print(f"{i} = ({self.transition[i].var}){self.transition[i].st}")
        print(f"Q0 : {self.start}")
        print(f"F : {self.final}")


if __name__ == "__main__":
    sd = StateDiagram()
    sd.input()
    sd.display()
    sd.genRegEx()
