#!/usr/bin/env python3
# -*- coding: utf8 -*-

import threading, time
from tkinter import *
from tkinter.messagebox import *

status = '' #Variable servant à la fois à indiquer si l'on peut poursuivre l'exécution du programme (càd si l'on a entré un (ou plusieurs, selon la situation) nom valide et cliqué sur OK) et à récupérer le (ou les) nom entré.

class simpleGUI(threading.Thread):
    '''
    Classe associée à l'interface demandant un seul nom.
    Voir la description de la classe GUI du fichier game.py pour l'explication quant au Thread (il s'agit en effet d'une situation semblable, où l'on doit faire tourner un autre programme en parallèle de l'interface)
    '''
    def __init__(self, attachTo = None, rootConsole = None):
        threading.Thread.__init__(self)
        self.attachTo = attachTo
        self.rootConsole = None
        
    def run(self):
        if self.attachTo is None:
            mainCon = Tk() 
        else:
            mainCon = self.attachTo #Même remarque que pour l'interface de game.py : on ne peut avoir qu'une seule fenêtre crée avec la fonction Tk() par application
        global status
        nom = StringVar("") #Les variables associées à des entrées Tkinter ne sont pas du même type que les variables Python traditionnelles. Pour les chaînes de caractères, ce sont des instances de la classe StringVar (définie dans le module Tkinter)
        status = '' #On réinitialise la variable status
        titleFrame = Frame(mainCon)
        title = Label(titleFrame, text = 'Veuillez entrer votre nom.', justify = CENTER) #On crée le message demandant le nom
        title.pack(fill = X, expand = Y, anchor = CENTER) #On fait en sorte que le label remplisse tout l'espace horizontal de la fenêtre, afin que le texte soit centré
        titleFrame.grid(row = 0, column = 0, columnspan = 8) #La méthode grid permet de placer les éléments selon un tableau, dont le fonctionnement peut rappeler celui d'un tableur. Ici, on place titleFrame dans la 'cellule' (0,0), et on lui fait occuper 8 colonnes.
        field = Entry(mainCon, textvariable = nom, justify = CENTER) #On crée le champ de texte dans lequel on va entrer le nom
        field.grid(row = 1, column = 2, columnspan = 4)
        def cancel():
            '''
            Fonction appelée lors du clic sur le bouton annuler
            '''
            global status
            status = None
            mainCon.destroy()
        def confirm():
            '''
            Fonction appelée lors du clic sur le bouton OK
            '''
            global status
            #NB : Afin de convertir une StringVar en une chaîne de caractère 'classique', on doit appeler la méthode get(). Sinon, si l'on récupère directement la valeur de la StringVar on obtient 'PY_VAR0'
            if nom.get() == "" or " " in nom.get():
                showerror('Saisie invalide', "Le nom ne doit pas contenir d'espace ou être vide")
                status = ''
            elif len(nom.get()) > 12:
                showerror('Saisie invalide', 'Le nom ne doit pas excéder 12 caractères')
                status = ''
            elif nom.get() == "None": #Artefact de développement : les anciennes versions utilisaient la chaîne de caractère 'None' plutôt que le 'symbole' spécial None pour l'annulation, à cause d'un problème dans la fonction askSimpleName. Ce problème a depuis été résolu, donc théoriquement avoir 'None' en chaîne de caractères pour nom ne devrait pas poser de problème, mais nous avons préféré garder cette condition au cas où.
                showerror('Saisie invalide', 'Le nom ne doit pas être "None"')
                status =  ''
            elif '\n' in nom.get() or chr(92) in nom.get(): #La fonction chr(92) renvoie le 92 ème caractère de la table ASCII, c'est à dire l'antislash (\). On ne peut en effet pas l'écrire directement, car c'est un symbole réservé à Python (associé à une lettre, il permet de modifier des chaînes de caractères, en ajoutant par exemple des retours à la ligne, et l'on ne souhaite pas avoir de telles choses dans nos noms afin de ne pas provoquer d'erreurs d'affichage)
                showerror('Saisie invalide', "Le nom ne doit pas contenir d'antislash")
            else: #Si aucune anomalie n'a été rencontrée
                status = nom.get() #La variable status prend la valeur entrée dans le champ de texte
                mainCon.destroy()
        buttonOk = Button(mainCon, text = 'OK', width = 5, command = confirm)
        buttonCancel = Button(mainCon, text = 'Annuler', width = 5, command = cancel)
        buttonOk.grid(row = 5, column = 1, columnspan = 3)
        buttonCancel.grid(row = 5, column = 4, columnspan = 3)
    
        colNum, rowNum = mainCon.grid_size() #On récupère la taille de la console dans laquelle on affiche l'interface en termes de lignes et colonnes (utilisées par la méthode grid())
        for x in range(colNum):
            mainCon.grid_columnconfigure(x, minsize = 25) #On fait en sorte que toutes les colonnes, mêmes vides, aient une largeur d'au moins 25 pixels. Cela empêche les colonnes vides d'être invisibles.
        for y in range(rowNum):
            mainCon.grid_rowconfigure(y, minsize = 5) #Même principe qu'au dessus, mais avec les lignes, et une hauteur minimale de 5 pixels
        if self.attachTo is None:
            mainCon.mainloop()
        else:
            mainCon.update() #Artefact de développement : Ne devrait plus être nécessaire en théorie (date en effet de lorsque nous avions essayé d'avoir plusieurs fenêtres crées avec Tk(), ce qui crée énormément d'erreurs et de problèmes, même après avoir rajouté cette ligne), mais gardé au cas où.
        if self.rootConsole is not None:
            self.rootConsole.update() #Même remarque que pour mainCon.update().
            
class multiGUI(threading.Thread):
    '''
    Classe associée à l'interface demandant deux noms.
    Comme elle possède beaucoup de similitudes avec la classe simpleGUI, la plupart des lignes redondantes ne sont pas commentées à nouveau dans cette classe.
    '''
    def __init__(self, attachTo = None, rootConsole = None):
        threading.Thread.__init__(self)
        self.attachTo = attachTo
        self.rootConsole = None
        
    def run(self):
        if self.attachTo is None:
            mainCon = Tk()
        else:
            mainCon = self.attachTo
        global status
        nom1 = StringVar("")
        nom2 = StringVar("")
        status = ''
        titleFrame = Frame(mainCon)
        title = Label(titleFrame, text = 'Veuillez entrer vos noms.', justify = CENTER)
        title.pack(fill = X, expand = Y, anchor = CENTER)
        titleFrame.grid(row = 0, column = 0, columnspan = 8)
        P1label = Label(mainCon, text = "Joueur 1 :") #Label situé à gauche du champ de texte du nom du joueur 1
        P1field = Entry(mainCon, textvariable = nom1, justify = CENTER) #Champ de texte du nom du joueur 1
        P1label.grid(row = 2, column = 0, columnspan = 2)
        P1field.grid(row = 2, column = 2, columnspan = 6)
        P2label = Label(mainCon, text = "Joueur 2 :") #Label situé à gauche du champ de texte du nom du joueur 2
        P2field = Entry(mainCon, textvariable = nom2, justify = CENTER) #Champ de texte du nom du joueur 2
        P2label.grid(row = 3, column = 0, columnspan = 2)
        P2field.grid(row = 3, column = 2, columnspan = 6)
        def cancel():
            global status
            status = None
            mainCon.destroy()
        def confirm():
            global status
            if (nom1.get() == "" or " " in nom1.get()) or (nom2.get() == "" or " " in nom2.get()):
                showerror('Saisie invalide', "Le nom ne doit pas contenir d'espace ou être vide")
                status = ''
            elif (len(nom1.get()) > 12) or (len(nom2.get()) > 12) :
                showerror('Saisie invalide', 'Le nom ne doit pas excéder 12 caractères')
                status = ''
            elif (nom1.get() == "None") or (nom2.get() == "None"):
                showerror('Saisie invalide', 'Le nom ne doit pas être "None"')
                status =  ''
            elif nom1.get() == nom2.get():
                showerror('Saisie invalide', 'Les deux noms ne doivent pas être identiques')
            elif ('\n' in nom1.get() or chr(92) in nom1.get()) or ('\n' in nom2.get() or chr(92) in nom2.get()): #La fonction chr(92) renvoie le 92 ème caractère de la table ASCII, c'est à dire l'antislash (\). On ne peut en effet pas l'écrire directement, car c'est un symbole réservé à Python (associé à une lettre, il permet de modifier des chaînes de caractères, en ajoutant par exemple des retours à la ligne, et l'on ne souhaite pas avoir de telles choses dans nos noms afin de ne pas provoquer d'erreurs d'affichage)
                showerror('Saisie invalide', "Le nom ne doit pas contenir d'antislash")
            else:
                status = (nom1.get(), nom2.get()) #La variable status prend la valeur d'un tuple (objet simillaire à une liste, mais non modifiable) contenant le nom du joueur 1 et celui du joueur 2
                mainCon.destroy()
        buttonOk = Button(mainCon, text = 'OK', width = 5, command = confirm)
        buttonCancel = Button(mainCon, text = 'Annuler', width = 5, command = cancel)
        buttonOk.grid(row = 5, column = 1, columnspan = 3)
        buttonCancel.grid(row = 5, column = 4, columnspan = 3)
    
        colNum, rowNum = mainCon.grid_size()
        for x in range(colNum):
            mainCon.grid_columnconfigure(x, minsize = 25)
        for y in range(rowNum):
            mainCon.grid_rowconfigure(y, minsize = 5)
        if self.attachTo is None:
            mainCon.mainloop()
        else:
            mainCon.update()
        if self.rootConsole is not None:
            self.rootConsole.update()
    
def askSimpleName(attachTo = None, rootConsole = None):
    '''
    Fonction permettant de demander un seul nom
    '''
    global status
    status = ''
    asker = simpleGUI(attachTo, rootConsole) #On crée une instance de simpleGUI
    asker.start() #On démarre le Thread de l'interface
    time.sleep(3) #On laisse le temps à l'interface de se charger
    while True:
        if status == '': #Si l'on a entré aucun nom
            continue #On continue la boucle (çad la fonction ne fait rien tant que l'interface n'a pas renvoyé de nom)
        else:
            break #Sinon, on sort de la boucle
    
    return status #On renvoie le nom entré

def askMultipleNames(attachTo = None, rootConsole = None):
    '''
    Fonction permettant de demander plusieurs noms
    Quasi identique à la fonction askSimpleName, les parties redondantes n'ont pas été commentées à nouveau
    '''
    global status
    status = ''
    asker = multiGUI(attachTo, rootConsole)
    asker.start()
    time.sleep(3)
    while True:
        if status == "":
            continue
        else:
            break
    
    return status #On renvoie les noms. Notez qu'il ne s'agit plus d'une chaîne de caractères comme dans askSimpleName, mais d'un tuple constitué de deux chaînes de caractères.

if __name__ == '__main__':
    from tkinter.messagebox import *
    showerror('Erreur', 'Veuillez lancer main.pyw pour démarrer le programme')
    