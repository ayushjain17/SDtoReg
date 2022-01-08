class Equation:
    def __init__(self, states):
        self.eq = {}
        for i in states:
            self.eq[i] = None
        self.eq['$'] = None

    def add(self, var, st):
        if self.eq[var] is None:
            self.eq[var] = st
        else:
            self.eq[var] += "+" + st

    def concat(self, var_st, st):
        ad_st = st if len(st) == 1 else f"({st})"
        # or var_st[-1] == ')' or var_st[-1] == '*'
        orig = '' if (var_st == '$' or var_st == '') else var_st if '+' not in var_st else f"({var_st})"
        return f"{orig}{ad_st}"

    def substitute(self, name, eq):
        for i in self.eq.keys():
            if i is not name:
                if self.eq[name] is None or eq.eq[i] is None:
                    continue
                st = self.concat(eq.eq[i], self.eq[name])
                # ad_st = self.eq[name] if len(self.eq[name]) == 1 else f"({self.eq[name]})"
                # st = ad_st if eq.eq[i] == '$' else f"{eq.eq[i]}{ad_st}"
                self.add(i, st)
        self.eq[name] = None

    def ardenTheorem(self, name):
        if self.eq[name] is not None:
            for i in self.eq.keys():
                if i != name and self.eq[i] is not None:
                    self.eq[i] = f"{self.concat(self.eq[i], self.eq[name])}*"
                    # self.concat(i, self.eq[name])
            self.eq[name] = None

    def getEqn(self, name):
        s = f"{name} = "
        for i in self.eq.keys():
            if self.eq[i] is not None:
                if i == '$':
                    s += f"{self.eq[i]} + "
                else:
                    s += f"({i})({self.eq[i]}) + "
        return s[:-3]+"\n"


class StateDiagram:
    def __init__(self):
        self.states = []
        self.terminals = []
        self.start = None
        self.final = []
        self.transition = {}

    def clear(self):
        self.__init__()

    def listInput(self, l):
        print("Enter N to stop")
        s = input()
        while s != "N":
            l.append(s)
            s = input()
        return l

    def inputTransition(self, d=None):
        if d:
            for i in d:
                if i[2] not in self.transition:
                    self.transition[i[2]] = Equation(self.states)
                self.transition[i[2]].add(i[0], i[1])
            if self.start not in self.transition:
                self.transition[self.start] = Equation(self.states)
            self.transition[self.start].add('$', '$')
        else:
            print("Format : present:terminal>next")
            print("Enter N to stop")
            s = input()
            while s != 'N':
                s = s.replace('>', ':').split(':')
                if s[2] not in self.transition:
                    self.transition[s[2]] = Equation(self.states)
                self.transition[s[2]].add(s[0], s[1])
                s = input()
            if self.start not in self.transition:
                self.transition[self.start] = Equation(self.states)
            self.transition[self.start].add('$', '$')

    def input(self, M=None):
        if M:
            (Q, Sigma, d, q0, F) = M
            self.states = Q
            self.terminals = Sigma
            self.start = q0
            self.final = F
            self.inputTransition(d)
        else:
            print('Enter the states:')
            self.listInput(self.states)
            print('Enter the terminals:')
            self.listInput(self.terminals)
            print('Enter the start symbol:')
            self.start = input()
            print('Enter the final state:')
            self.listInput(self.final)
            print('Enter the transition rules')
            self.inputTransition()

    def genRegEx(self):
        for i in range(len(self.states)):
            var = self.states[i]
            self.transition[var].ardenTheorem(var)
            # print(self.transition[var].getEqn(var))
            for j in range(len(self.states)):
                if j != i:
                    self.transition[self.states[j]].substitute(var, self.transition[var])
                    # print(self.transition[self.states[j]].getEqn(self.states[j]))
        ans = Equation(self.states)
        # for i in self.states:
        #     print(self.transition[i].getEqn(i))
        s = self.final[0]
        for i in self.final[1:]:
            s += f" + {i}"
        for j in self.final:
            ans.add('$', self.transition[j].eq['$'])
        return ans.getEqn(s)

    def get_Equations(self):
        text = ''
        for i in self.transition.keys():
            text += self.transition[i].getEqn(i)
        return text

    def display(self):
        print("\nAutomata:")
        print("M : [Q, Sigma, Transition function, Q0, F]")
        print(f"Q : {self.states}")
        print(f"Sigma : {self.terminals}")
        print("Transition Equations")
        print(self.get_Equations())
        print(f"q0 : {self.start}")
        print(f"F : {self.final}")


if __name__ == "__main__":
    sd = StateDiagram()
    sd.input()
    sd.display()
    print("\nThe Regular Expression for the final state(s):", sd.genRegEx())
