class Task:
    name = ""
    reads = []
    writes = []
    run = None

class TaskSystem:
    def __init__(self, lTask=[Task], dict={}):
        self.lTask = lTask
        self.dict = dict

    def getDependencies(self, nomTache):
        depend = []
        ensemble = set()

        for i in self.lTask:
            if nomTache in i.reads:
                ensemble.add(i.name)
            if i.name not in ensemble and i.name != nomTache:
                execution = True
                for j in i.reads:
                    if j in ensemble:
                        execution = False
                        break
                if execution:
                    depend.append(i.name)

        return depend
    

    def runSeq(self):
        # Trouver la première tâche à exécuter
        to_run = None
        for tache in self.lTask:
            if not tache.reads:
                to_run = tache
                break
        if not to_run:
            # Aucune tâche sans dépendances trouvée
            return
        
        # Exécution de la tâche
        to_run.run()
        
        # Exécution des tâches dépendantes
        for dependance in self.lTask:
            if to_run.name in dependance.reads:
                self.runSeq(dependance)


        
# fonction
def runT1():
    global X
    X = 5
def runT2():
    global Y
    Y = 2
def runT3():
    global W
    W = 4
def runTsomme():
    global X, Y, Z , W
    Z = X + Y + W
t1 = Task()
t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1
t2 = Task()
t2.name = "T2"
t2.writes = ["Y"]
t2.run = runT2
t3 = Task()
t3.name = "T3"
t3.writes = ["W"]
t3.run = runT3
tSomme = Task()
tSomme.name = "somme"
tSomme.reads = ["X", "Y","W"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme

s1 = TaskSystem([t1, t2, tSomme,t3], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"],"T3":["somme","T2","T1"]})

#compilaiton
t1.run()
t2.run()
t3.run()
tSomme.run()
print(s1.getDependencies("T3"))