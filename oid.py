from ctypes import alignment
from tkinter import ANCHOR, END, RAISED, Tk, Label, Entry, Button, Text, ttk, PhotoImage
from numpy import source

from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDF
from rdflib.namespace import FOAF

import matplotlib.pyplot as plt
import numpy as np
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
import os


source = ""
target = ""
add = ""
diff = ""
inter = ""
xor = ""

X_BOX = 85
Y_BOX = 15


root = Tk()
#root.attributes("-fullscreen", True)
root.geometry("1900x750")

# Entry 
label_source = Label(text="Fichier source : ", anchor='w')
label_source.grid(row=0, column=0)

entry_source = Entry(width=25)
entry_source.insert(END, "source.ttl")
entry_source.grid(row=1, column=0)

label_target = Label( text="Fichier cible : ", anchor='w')
label_target.grid(row=0, column=1)

entry_target = Entry(width=25)
entry_target.insert(END, "target.ttl")
entry_target.grid(row=1, column=1)

# Compare button function
def open_source(): 
    global source
    source = str(entry_source.get())
    source = Graph().parse(source, format="ttl")

    source_output.delete('1.0', END)
    #affichage(source)
    for subj, pred, obj in source:
        source_output.insert(END, "---------------------------------------------------\n")
        source_output.insert(END, "subj : " + subj + "\n") 
        source_output.insert(END, "pred : " + pred + "\n") 
        source_output.insert(END, "obj : " + obj + "\n") 

        if (subj, pred, obj) not in source:
            raise Exception("It better be!")

def open_target(): 
    global target
    # Recuperer le text des deux entry 
    target = str(entry_target.get())
    target = Graph().parse(target, format="ttl")

    target_output.delete('1.0', END)
    #affichage(target)
    for subj, pred, obj in target:
        target_output.insert(END, "---------------------------------------------------\n")
        target_output.insert(END, "subj : " + subj + "\n" ) 
        target_output.insert(END, "pred : " + pred + "\n") 
        target_output.insert(END, "obj : " + obj + "\n") 

        if (subj, pred, obj) not in target:
            raise Exception("It better be!")

def bilan(): 
    global source
    global target
    global add
    global diff
    global inter
    global xor

    if source == "" : 
        source = str(entry_source.get())
        source = Graph().parse(source, format="ttl")

    if target == "": 
        target = str(entry_target.get())
        target = Graph().parse(target, format="ttl")

    add = source + target
    diff = source - target
    inter = source & target
    xor = target ^ source

    bilan_output.delete('1.0', END)
    #Print the number of "triples" in the Graph
    bilan_output.insert(END, "      Graph source : " + str(len(source)) + " statements.\n")
    bilan_output.insert(END, "      Graph target : " + str(len(target)) + " statements.\n")
    bilan_output.insert(END, "       Graph union : " + str(len(add)) + " statements.\n")
    bilan_output.insert(END, "  Graph difference : " + str(len(diff)) + " statements.\n")
    bilan_output.insert(END, "Graph intersection : " + str(len(inter)) + " statements.\n")
    bilan_output.insert(END, "         Graph XOR : " + str(len(xor)) + " statements.\n")
    
source_button = Button(root, text="Ouvrir", command=open_source)
source_button.grid(row=2, column=0)

target_button = Button(root, text="Ouvrir", command=open_target)
target_button.grid(row=2, column=1)

bilan_button = Button(root, text="Bilan", command=bilan)
bilan_button.grid(row=2, column=2)

# Output
source_output = Text(width=X_BOX, height=Y_BOX, border=4, relief=RAISED)
source_output.insert(END, "")
source_output.grid(row=3, column=0)

target_output = Text(width=X_BOX, height=Y_BOX, border=4, relief=RAISED)
target_output.insert(END, "")
target_output.grid(row=3, column=1)

bilan_output = Text(width=X_BOX, height=Y_BOX, border=4, relief=RAISED)
bilan_output.insert(END, "")
bilan_output.grid(row=3, column=2)

# ------------------------ Frequences ---------------------------------
def printAllFrequences(graph):
    subjects_output.delete('1.0', END)
    predicates_output.delete('1.0', END)
    objects_output.delete('1.0', END)

    subjects = {}
    predicates = {}
    objects = {}

    subjectsOrdered = {}
    predicatesOrdered = {}
    objectsOrdered = {}

    for s, p, o in graph.triples((None,  None, None)):
        s = str(s)
        p = str(p)
        o = str(o)
        
        if s in subjects :
            subjects[s] += 1
        else :
            subjects[s] = 0 
            
        if p in predicates :
            predicates[p] += 1
        else :
            predicates[p] = 0 
            
        if o in objects :
            objects[o] += 1
        else :
            objects[o] = 0 

    for i in sorted(subjects, key=subjects.get, reverse=True):
        subjectsOrdered[i] = subjects[i]
        
    for i in sorted(predicates, key=predicates.get, reverse=True):
        predicatesOrdered[i] = predicates[i]

    for i in sorted(objects, key=objects.get, reverse=True):
        objectsOrdered[i] = objects[i]

    for w in subjectsOrdered: 
        subjects_output.insert(END, str(subjectsOrdered[w]) + " : " + str(w) + "\n")

    for w in predicatesOrdered: 
        predicates_output.insert(END, str(predicatesOrdered[w]) + " : " +  str(w)+ "\n")

    for w in objectsOrdered: 
        objects_output.insert(END, str(objectsOrdered[w]) + " : " +  str(w)+ "\n")

def analyse(): 
    graphSelected = str(listeCombo.get())

    if graphSelected == "Source": 
        printAllFrequences(source)
    elif graphSelected == "Cible": 
        printAllFrequences(target)
    elif graphSelected == "Union": 
        printAllFrequences(add)
    elif graphSelected == "Difference": 
        printAllFrequences(diff)
    elif graphSelected == "Intersection": 
        printAllFrequences(inter)
    elif graphSelected == "XOR": 
        printAllFrequences(xor)

title_frequences = Label(text="Fréquences : ", anchor='w')
title_frequences.grid(row=6, column=0)

listeGraph=["Source", "Cible", "Union", "Difference", "Intersection", "XOR"]
listeCombo = ttk.Combobox(root, values=listeGraph)
listeCombo.current(0)
listeCombo.grid(row=7, column=0)

analyse_button = Button(root, text="Analyse", command=analyse)
analyse_button.grid(row=8, column=0)


subjects_output = Text(width=X_BOX, height=Y_BOX, border=4, relief=RAISED)
subjects_output.insert(END, "")
subjects_output.grid(row=9, column=0)

predicates_output = Text(width=X_BOX, height=Y_BOX, border=4, relief=RAISED)
predicates_output.insert(END, "")
predicates_output.grid(row=9, column=1)

objects_output = Text(width=X_BOX, height=Y_BOX, border=4, relief=RAISED)
objects_output.insert(END, "")
objects_output.grid(row=9, column=2)


label_graphe = Label(text="Graphe : ", anchor='w')
label_graphe.grid(row=10, column=0, sticky='e')

liste_graphe = ttk.Combobox(root, values=listeGraph)
liste_graphe.current(0)
liste_graphe.grid(row=10, column=1, sticky='w')

label_triplet = Label(text="Triplet : ", anchor='w')
label_triplet.grid(row=11, column=0, sticky='e')

liste_triplet = ttk.Combobox(root, values=["Sujets", "Prédicats", "Objets"])
liste_triplet.current(0)
liste_triplet.grid(row=11, column=1, sticky='w')

label_uri = Label(text="URI : ", anchor='w')
label_uri.grid(row=12, column=0, sticky='e')

entry_uri = Entry(width=60)
entry_uri.insert(END, "http://...")
entry_uri.grid(row=12, column=1, sticky='w')

label_precision = Label(text="Précision : ", anchor='w')
label_precision.grid(row=13, column=0, sticky='e')

entry_precision = Entry(width=25)
entry_precision.insert(END, "10")
entry_precision.grid(row=13, column=1, sticky='w')

def simCompare(graph, uri, precision):
    subjects = {}
    predicates = {}
    objects = {}

    subjectsOrdered = {}
    predicatesOrdered = {}
    objectsOrdered = {}

    for s, p, o in graph.triples((None,  None, None)):
        s = str(s)
        p = str(p)
        o = str(o)
        
        if s in subjects :
            subjects[s] += 1
        else :
            subjects[s] = 0 
            
        if p in predicates :
            predicates[p] += 1
        else :
            predicates[p] = 0 
            
        if o in objects :
            objects[o] += 1
        else :
            objects[o] = 0 

    for i in sorted(subjects, key=subjects.get, reverse=True):
        subjectsOrdered[i] = subjects[i]
        
    for i in sorted(predicates, key=predicates.get, reverse=True):
        predicatesOrdered[i] = predicates[i]

    for i in sorted(objects, key=objects.get, reverse=True):
        objectsOrdered[i] = objects[i]


    normalized_levenshtein = NormalizedLevenshtein()
    sameAs = 0
    x = []
    y = []

    tripletSelected = str(liste_triplet.get())
    #dimTriplet = subjectsOrdered

    if tripletSelected == "Sujets": 
        dimTriplet = subjectsOrdered
    elif tripletSelected == "Prédicats": 
        dimTriplet = predicatesOrdered
    elif tripletSelected == "Objets": 
        dimTriplet = objectsOrdered

    for i in np.linspace(0,1,precision,endpoint=True):
        for t in dimTriplet: 
            if normalized_levenshtein.distance(str(uri), str(t)) < i: 
                sameAs += 1

        x.append(i)
        y.append(sameAs)
        sameAs=0
    
    fig = plt.figure()
    ax = plt.axes()
    plt.xlabel("Seuil")
    plt.ylabel("Nombre d'ocurrence")
    ax.plot(x, y)

    plt.savefig('autoSave.png')

    os.system("python plot.py")
    

def calculer(): 
    graphSelected = str(liste_graphe.get())

    if graphSelected == "Source": 
        simCompare(graph=source, uri=str(entry_uri.get()), precision=int(entry_precision.get()))
    elif graphSelected == "Cible": 
        simCompare(graph=target, uri=str(entry_uri.get()), precision=int(entry_precision.get()))
    elif graphSelected == "Union": 
        simCompare(graph=add, uri=str(entry_uri.get()), precision=int(entry_precision.get()))
    elif graphSelected == "Difference": 
        simCompare(graph=diff, uri=str(entry_uri.get()), precision=int(entry_precision.get()))
    elif graphSelected == "Intersection": 
        simCompare(graph=inter, uri=str(entry_uri.get()), precision=int(entry_precision.get()))
    elif graphSelected == "XOR": 
        simCompare(graph=xor, uri=str(entry_uri.get()), precision=int(entry_precision.get()))

    
calculer_button = Button(root, text="Calculer", command=calculer)
calculer_button.grid(row=14, column=0, sticky='e')


root.mainloop() 