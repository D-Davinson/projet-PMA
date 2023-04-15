#import
import threading,graphviz,random,time
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
        #initialisation
        parcouru = set()
        deps = []
        #fonction récurisive seach qui permet d'explorer toute les tâches dependantes de la tâche donnée en parametre
        def search(task):
            parcouru.add(task)
            for i in self.dict[task]:
                if i not in parcouru:
                    pret_dep = True
                    for j in self.lTask:
                        if j.name == i and j.run is None:
                            pret_dep = False
                            break
                    if pret_dep:
                        thread = threading.Thread(target=search, args=(i,))
                        thread.start()
                        deps.append(i)

        search(nomTache)
        for thread in threading.enumerate():
            if thread != threading.main_thread():
                thread.join()
        # tri et enlèvent les redondances et retourne la liste de dépendances        
        return sorted(set(deps))
    
    # Récuperer les noms des Tâches
    def getTask(self, nomTache):
        for tache in self.lTask:
            if nomTache == tache.name:
                return tache  
    # Run les tâches récuperer par getTask  et relance runTask de manière récursive pour run la totalité des tâches via le dictionnaire      
    def runTask(self, tache):
        for dep in self.dict[tache.name]:
            depTask = self.getTask(dep)
            if depTask:
                self.runTask(depTask)
        tache.run()
    # Lancement des méthodes auxilaire dans la liste de nos tâches
    def runSeq(self):
        for tache in self.lTask:
            self.runTask(tache)


    def run(self, max_threads=10):
        # Liste des threads en cours d'exécution
        init_threads = []

        # Liste des tâches prêtes à être exécutées
        exec_tasks = [t for t in self.lTask if not t.reads]

        while exec_tasks or init_threads:
            # Lancer autant de threads que possible
            while len(init_threads) < max_threads and exec_tasks:
                tache = exec_tasks.pop(0)
                thread = threading.Thread(target=tache.run)
                thread.start()
                init_threads.append((tache, thread))

            # Attendre la fin d'un thread
            for task_thread in init_threads:
                task, thread = task_thread
                if not thread.is_alive():
                    init_threads.remove(task_thread)
                    # Exécuter les tâches dépendantes
                    for dependance in self.lTask:
                        if task.name in dependance.reads:
                            dependance.reads.remove(task.name)
                            if not dependance.reads:
                                exec_tasks.append(dependance)
    
    def detTestRnd(self, nb_test):

        for i in range(nb_test):
            # Générer des valeurs aléatoires pour les variables
            for i in self.lTask:
                for j in i.reads + i.writes:
                    setattr(i, j, random.randint(0, 100))

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
        print(f"Tous les {nb_test} tests ont réussi")
        return True
    
    def parCost(self, nb_test):
        seq_times = []
        par_times = []

        # mesure l'execution en time
        for i in range(nb_test):
            start_time_sq = time.time()
            self.runSeq()
            seq_times.append(time.time() - start_time_sq)
            
            start_time_par = time.time()
            self.run()
            par_times.append(time.time() - start_time_par)
        #Calcul de la moyenne des deux executions    
        average_seq = sum(seq_times) / nb_test
        average_par = sum(par_times) / nb_test
        
        print(f"Execution séquenciel: {average_seq:.6f} secondes")
        print(f"Execution parallèle: {average_par:.6f} secondes")
        print(f"Diffèrence: {average_seq - average_par:.6f} secondes")
                            

    def draw(self):
        # Créer le graphe
        graph = graphviz.Digraph()
        # Ajouter les noeuds
        for t in self.lTask:
            graph.node(t.name)
        #Ajout des liens
            for dep in self.getDependencies(t.name):
                graph.edge(dep, t.name)

        # Ajout les liens parallèles suivant la condition de Bersteins
            for i, t1 in enumerate(self.lTask):
                for j in range(i+1, len(self.lTask)):
                    t2 = self.lTask[j]
                    if not set(t1.writes).intersection(t2.reads):
                        continue
                    if not set(t2.writes).intersection(t1.reads):
                        continue
                    if not set(t1.writes).intersection(t2.writes):
                        graph.edge(t1.name, t2.name)

    # Afficher le graphe
        graph.view()




def error_message(lTask, dict):
    # Vérifier si les noms de tâches sont uniques
    task_names = [t.name for t in lTask]
    if len(task_names) != len(set(task_names)):
        print("Erreur: Les noms des tâches ne sont pas uniques")
        return False
    
    # Vérifier si toutes les tâches mentionnées dans le dictionnaire de précédence existent
    allTask_names = set(task_names)
    for t, deps in dict.items():
        if t not in allTask_names:
            print(f"Erreur: La tâche {t} n'existe pas")
            return False
        for dep in deps:
            if dep not in allTask_names:
                print(f"Erreur: La tâche {dep} mentionnée comme dépendance de {t} est inexistante")
                return False
    
    # Vérifier si le système de tâches est déterminé
    parcouru = set()
    for t in allTask_names:
        if t not in parcouru:
            deps = TaskSystem(lTask, dict).getDependencies(t)
            parcouru.update(deps)
    if parcouru != allTask_names:
        print("Erreur: Le système de tâches est indéterminé")
        return False
    
    return True        