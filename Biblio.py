#class
class Task:
    name = ""
    reads = []
    writes = []
    run = None
X = None
Y = None
Z = None

dicta={0:"1",1:"2"}

class TaskSystem:
    def __init__(self,lTaks=[Task],dict=dicta):
        self.lTaks = lTaks
        self.dict = dict




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

#compilaiton
t1.run()
t2.run()
tSomme.run()
print(X)
print(Y)
print(Z)