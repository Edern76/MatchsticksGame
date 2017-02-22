from tkinter import *
from tkinter.messagebox import *

def askName(attachTo = None):
    if attachTo is None:
        mainCon = Tk()
    else:
        mainCon = attachTo
    while True:
        nom = StringVar("")
        status = None
        titleFrame = Frame(mainCon)
        title = Label(titleFrame, text = 'Veuillez entrer votre nom.', justify = CENTER)
        title.pack(fill = X, expand = Y, anchor = CENTER)
        titleFrame.grid(row = 0, column = 0, columnspan = 8)
        field = Entry(mainCon, textvariable = nom, justify = CENTER)
        field.grid(row = 1, column = 2, columnspan = 4)
        def annuler():
            mainCon.destroy()
        def confirmer():
            global status
            if nom.get() == "" or " " in nom.get():
                showerror('Saisie invalide', "Le nom ne doit pas contenir d'espace ou etre vide")
                status = 'None'
            elif len(nom.get()) > 12:
                showerror('Saisie invalide', 'Le nom ne doit pas exceder 12 caracteres')
                status = 'None'
            elif nom.get() == "None":
                showerror('Saisie invalide', 'Le nom ne doit pas etre "None"')
                status =  'None'
            else:
                print('Went here')
                status = nom.get()
            print('Updating')
            mainCon.update()
        buttonOk = Button(mainCon, text = 'OK', width = 5, command = confirmer)
        buttonCancel = Button(mainCon, text = 'Annuler', width = 5, command = annuler)
        buttonOk.grid(row = 5, column = 1, columnspan = 3)
        buttonCancel.grid(row = 5, column = 4, columnspan = 3)
    
        colNum, rowNum = mainCon.grid_size()
        for x in range(colNum):
            mainCon.grid_columnconfigure(x, minsize = 25)
        for y in range(rowNum):
            mainCon.grid_rowconfigure(y, minsize = 5)
        if status is not None and status != 'None':
            print(status is not None and status != 'None')
            break
        else:
            #print('wololo')
            continue
    return status
    

if __name__ == '__main__':
    name = askName()
    if name != '':
        print(name)
    else:
        print("La variable name n'est pas correctement definie")
    