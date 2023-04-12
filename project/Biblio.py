#import
import threading,graphviz,random,time
class Task:
    name = ""
    reads = []
    writes = []
    run = None

class TaskSystem:
    def __init__(self, lTask=[Task], dict={}, max_threads=4):
        self.lTask = lTask
        self.dict = dict
        self.max_threads = max_threads

    def getDependencies(self, nomTache):
        visited = set()
        deps = []

        def search(task):
            visited.add(task)
            for i in self.dict[task]:
                if i not in visited:
                    dependencies_ready = True
                    for j in self.lTask:
                        if j.name == i and j.run is None:
                            dependencies_ready = False
                            break
                    if dependencies_ready:
                        thread = threading.Thread(target=search, args=(i,))
                        thread.start()
                        deps.append(i)

        search(nomTache)
        for thread in threading.enumerate():
            if thread != threading.main_thread():
                thread.join()
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
        # Liste des threads en cours d'exécution
        running_threads = []

        # Liste des tâches prêtes à être exécutées
        ready_tasks = [t for t in self.lTask if not t.reads]

        while ready_tasks or running_threads:
            # Lancer autant de threads que possible
            while len(running_threads) < self.max_threads and ready_tasks:
                tache = ready_tasks.pop(0)
                thread = threading.Thread(target=tache.run)
                thread.start()
                running_threads.append((tache, thread))

            # Attendre la fin d'un thread
            for task_thread in running_threads:
                task, thread = task_thread
                if not thread.is_alive():
                    running_threads.remove(task_thread)
                    # Exécuter les tâches dépendantes
                    for dependance in self.lTask:
                        if task.name in dependance.reads:
                            dependance.reads.remove(task.name)
                            if not dependance.reads:
                                ready_tasks.append(dependance)
    
    def detTestRnd(self, num_runs=10):

        for i in range(num_runs):
            # Générer des valeurs aléatoires pour les variables
            for i in self.lTask:
                for j in i.reads + i.writes:
                    setattr(i, j, random.randint(0, 1000))

            # Exécuter le système de tâches en mode séquentiel et stocker le résultat
            results_seq = {}
            for i in self.lTask:
                i.run = lambda: results_seq.update({i.name: getattr(i, "result", None)})
            self.runSeq()

            # Exécuter le système de tâches en mode parallèle et comparer le résultat
            results_par = {}
            for i in self.lTask:
                i.run = lambda: results_par.update({i.name: getattr(i, "result", None)})
            self.run()

            # Comparer les résultats de l'exécution séquentielle et parallèle
            if results_seq != results_par:
                print(f"Le test a échoué pour le jeu de valeurs aléatoires n°{i+1}")
                return False

        # Tous les tests ont réussi
        print(f"Tous les {num_runs} tests ont réussi")
        return True
    
    def parCost(self, num_runs=10):
        seq_times = []
        par_times = []
        
        # execution des tâches en mode séquentiel et parallèle
        self.runSeq()
        self.run()
        
        # mesure l'execution en time
        for i in range(num_runs):
            start_time_sq = time.time()
            self.runSeq()
            seq_times.append(time.time() - start_time_sq)
            
            start_time_par = time.time()
            self.run()
            par_times.append(time.time() - start_time_par)
            
        seq_avg = sum(seq_times) / num_runs
        par_avg = sum(par_times) / num_runs
        
        print(f"Execution séquenciel: {seq_avg:.6f} secondes")
        print(f"Execution parallèle: {par_avg:.6f} secondes")
        print(f"Diffèrence: {par_avg - seq_avg:.6f} secondes")
                            

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
tSomme.reads = ["X", "Y"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme

#compilaiton
t1.run()
t2.run()
tSomme.run()
s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]})
s1.draw()