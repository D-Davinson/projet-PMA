#import
import threading
import graphviz
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


    def run(self):
        # Dictionnaire des threads en cours d'exécution pour chaque tâche
        running_threads = {}

        while True:
            # Trouver toutes les tâches sans dépendances non encore exécutées
            to_run = []
            for tache in self.lTask:
                if not tache.reads and tache.name not in running_threads:
                    to_run.append(tache)
            if not to_run:
                # Aucune tâche sans dépendances non encore exécutée trouvée
                break

            # Lancer autant de threads que possible
            max_threads = 4  # Nombre maximal de threads en cours d'exécution simultanément
            for tache in to_run:
                if len(running_threads) < max_threads:
                    running_threads[tache.name] = threading.Thread(target=tache.run)
                    running_threads[tache.name].start()

            # Attendre la fin de tous les threads en cours d'exécution
            for tache_name, thread in running_threads.items():
                thread.join()
                del running_threads[tache_name]
    def draw():
            # graphviz pour generer les noeud et arc
        g = graphviz.Digraph('G',filename ='Biblio.gv')
        g.edge(t1.name,tSomme.name)
        g.edge(t2.name,tSomme.name)
        g.view()


        
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
tSomme.reads = ["X", "Y","W"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme

s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]})
#compilaiton
t1.run()
t2.run()
tSomme.run()
s1.runSeq
s1.run
print(X)
print(Y)
print(Z)
print(s1.getDependencies("somme"))

s1.draw()


# graphviz pour generer les noeud et arc