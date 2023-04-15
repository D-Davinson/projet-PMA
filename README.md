# 🚀 _PROJECT_ - PARRALÉLISLM MAXIMAL AUTOMATIC

## 💫 Objective

The objective is the implementation of a library that allows a task system to be rendered according to the following condition:
- **Parralélism Maximal Automatic**
- Entered in **Python**

### Inside of libaries :

| Class | _Description_ |
|-|-|
| Task  | Initialize the reading, writing and execution of a task|

| Constructor | _Description_ |
|-|-|
| TaskSystem  | Takes a tasks list and a dependency dictionary as parameters|

| Methods | _Description_ |
|-|-|
|getDependencies(nomTache)|List the dependencies according to the maximum parallelism system|
|runSeq()|Sequential execution of the task system|
|run()|Parallelim execution of the task system|
|draw()|Setting up a previous graph according to the maximum parallelism system|
|error_message(TaskSystem)|Print some basics error about the task sytem|
|detTestRnd(nb_test)|Do some random test with comparaison of execution|
|parCost(nb_test)|Measure the execution time between runSeq and run. Give the average and the difference|


## 💫 Implementation

### Import
| Type of package | Import |
|-|-|
|Standard|thread,random,time|
|PyPi| graphviz|

### Install
- the standard imports are already in the pyhton library
- Here is the installation required to install graphviz :
    https://pip.pypa.io/en/stable/installation/
  - Download zip application :  https://bootstrap.pypa.io/pip/pip.pyz
  - Open a terminal/command prompt, cd to the folder containing the get-pip.py file and run:
```  
$ python get-pip.py

$ pip install graphviz
```
  

## 🧑🏽‍💻 Authors

- [@Davinson DOGLAS PRINCE](https://github.com/D-Davinson)
- [@Exaucé MAKELE](https://github.com/M-Exauce)
