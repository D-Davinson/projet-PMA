class Task:
    name = ""
    reads = []
    writes = []
    run = None

class TaskSystem:
    def __init__(self, lTask=[Task], dict={}):
        self.lTask = lTask
        self.dict = dict

    def getDependencies(self,nomTache):
        visited = set()
        deps = []

        def search(t):
            visited.add(t)
            for depend in self.dict[t]:
                if depend not in visited:
                     search(depend)
                     deps.append(depend)

        search(nomTache)
        return sorted(set(deps))

        
# fonction
def runT1():
    global X
    X = 5
def runT2():
    global Y
    Y = 2
def runTsomme():
    global X, Y, Z
    Z = X + Y
t1 = Task()
t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1
t2 = Task()
t2.name = "T2"
t2.writes = ["Y"]
t2.run = runT2
tSomme = Task()
tSomme.name = "somme"
tSomme.reads = ["X", "Y"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme

s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]})

#compilaiton
t1.run()
t2.run()
tSomme.run()
print(X)
print(Y)
print(Z)
print(s1.getDependencies("somme"))