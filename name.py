#!/usr/bin/env python3
# -*- coding: utf8 -*-

import threading, time
from tkinter import *
from tkinter.messagebox import *

status = ''

class simpleGUI(threading.Thread):

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
        nom = StringVar("")
        status = ''
        titleFrame = Frame(mainCon)
        title = Label(titleFrame, text = 'Veuillez entrer votre nom.', justify = CENTER)
        title.pack(fill = X, expand = Y, anchor = CENTER)
        titleFrame.grid(row = 0, column = 0, columnspan = 8)
        field = Entry(mainCon, textvariable = nom, justify = CENTER)
        field.grid(row = 1, column = 2, columnspan = 4)
        def cancel():
            global status
            status = None
            mainCon.destroy()
        def confirm():
            global status
            if nom.get() == "" or " " in nom.get():
                showerror('Saisie invalide', "Le nom ne doit pas contenir d'espace ou être vide")
                status = ''
            elif len(nom.get()) > 12:
                showerror('Saisie invalide', 'Le nom ne doit pas excéder 12 caractères')
                status = ''
            elif nom.get() == "None":
                showerror('Saisie invalide', 'Le nom ne doit pas être "None"')
                status =  ''
            else:
                status = nom.get()
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
            
class multiGUI(threading.Thread):

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
        P1label = Label(mainCon, text = "Joueur 1 :")
        P1field = Entry(mainCon, textvariable = nom1, justify = CENTER)
        P1label.grid(row = 2, column = 0, columnspan = 2)
        P1field.grid(row = 2, column = 2, columnspan = 6)
        P2label = Label(mainCon, text = "Joueur 2 :")
        P2field = Entry(mainCon, textvariable = nom2, justify = CENTER)
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
            else:
                status = (nom1.get(), nom2.get())
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
    global status
    status = ''
    asker = simpleGUI(attachTo, rootConsole)
    asker.start()
    time.sleep(3)
    while True:
        if status == '':
            #print('Weeeeeee')
            continue
        else:
            break
    
    return status

def askMultipleNames(attachTo = None, rootConsole = None):
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
    
    return status
if __name__ == '__main__':
    from tkinter.messagebox import *
    showerror('Erreur', 'Veuillez lancer main.pyw pour démarrer le programme')
    