from biblio import *

#fonction des differentes tâches
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

# lecture et ecriture dans les tâches
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

#lancement de la totalité des tâches
t1.run()
t2.run()
tSomme.run()

# initialisation du sysstème de tâches

s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]})

#lancement des differentes méthodes depuis la bibliothèque biblio.py -> Class TaskSystem


print(s1.getDependencies("somme"), "est la liste de dépendances de la tâche")


s1.runSeq()
s1.run()

#mettre en parametre le nombre de tests :

s1.detTestRnd(10)
s1.parCost(10)

#lancement de la méthode de validité d'entrée depuis la bibliothèque biblio.py

error_message([t1, t2, tSomme], {"T1": [], "T2": ["T70"], "somme": ["T1", "T2"]})



# methode draw mis en commentaire du fait d'un soucis lors de son exécution (problème directement liées dans la libraire de Graphviz)
# fonctionne lorsque l'on execute uniquement cette méthode. De plus ne donne pas une proposition de PMA valable.

#lancement de la méthodes draw depuis la bibliothèque biblio.py -> Class TaskSystem
#s1.draw()