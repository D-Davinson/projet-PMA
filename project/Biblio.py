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

    def getDependencies(self,nomTache):
        visited = set()
        deps = []

        def search(t):
            visited.add(t)
            for i in self.dict[t]:
                if i not in visited:
                     search(i)
                     deps.append(i)

        search(nomTache)
        return sorted(set(deps))

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

    def draw(self):
        # Créer le graphe
        graph = graphviz.Digraph()

        # Ajouter les noeuds
        for tache in self.lTask:
            graph.node(tache.name)

        # Ajouter les liens
            for dep in self.dict[tache.name]:
                graph.edge(dep, tache.name)

        # Afficher le graphe
        graph.view()


def error_message(lTask, dict):
    # Vérifier si les noms de tâches sont uniques
    task_names = [t.name for t in lTask]
    if len(task_names) != len(set(task_names)):
        print("Erreur: Les noms des tâches ne sont pas uniques")
        return False
    
    # Vérifier si toutes les tâches mentionnées dans le dictionnaire de précédence existent
    all_task_names = set(task_names)
    for t, deps in dict.items():
        if t not in all_task_names:
            print(f"Erreur: La tâche {t} n'existe pas")
            return False
        for dep in deps:
            if dep not in all_task_names:
                print(f"Erreur: La tâche {dep} mentionnée comme dépendance de {t} est inexistante")
                return False
    
    # Vérifier si le système de tâches est déterminé
    visited = set()
    for t in all_task_names:
        if t not in visited:
            deps = TaskSystem(lTask, dict).getDependencies(t)
            visited.update(deps)
    if visited != all_task_names:
        print("Erreur: Le système de tâches est indéterminé")
        return False
    
    return True        



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

#compilaiton
t1.run()
t2.run()
tSomme.run()
s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": [], "somme": ["T1", "T2"]})
print(X)
print(Y)
print(Z)


error_message([t1, t2, tSomme], {"T1": [], "T2": [], "somme": ["T1", "T2"]})