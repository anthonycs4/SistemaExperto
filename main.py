from ctypes import sizeof
from token import LEFTSHIFT
from logging import RootLogger
from operator import length_hint
from select import select
from tkinter import *
from tkinter import filedialog as fd
import shutil
import copy
import os
import tkinter
from turtle import width  
from PIL import ImageTk,Image
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import threading
import os
import random
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class graph_frame(Frame):
    def __init__(self):
        Frame.__init__(self,root)
       
    def add_graph(self,fig):
        self.mpl_canvas=FigureCanvasTkAgg(fig,self)
       
        self.mpl_canvas.get_tk_widget().pack(fill=BOTH,expand=True)
        self.mpl_canvas._tkcanvas.pack( fill=BOTH, expand=True)
    def remove_graph(self):
        self.mpl_canvas.get_tk_widget().pack_forget()
        self.mpl_canvas._tkcanvas.pack_forget()
        del self.mpl_canvas

class roedor:
    def __init__(self)->None:
        self.nombre = ""
        self.tamaño = ""
        self.color = ""
        self.habitat = ""
        self.descripcion = ""
        self.imagen = "sources/default.jpeg"
       
        # Características adicionales
        self.cola = ""
        self.orejas = ""
        self.patas = ""
        self.pelaje = ""

class visualizer:
    def __init__(self,menu,frame1,roedor,rules,classifier)->None:
        self.frame1=frame1
        self.classifier=classifier
        self.name=Label(self.frame1,text="ROEDOR",background='#353437')
        self.name.configure(font=("Arial",50))
       
        openImage=Image.open(roedor.imagen)
        img=openImage.resize((200,300))
        self.photo=ImageTk.PhotoImage(img)
        self.image=Label(self.frame1,image=self.photo)

        self.size=Label(self.frame1,text="TAMAÑO",background='#353437')
        self.size.configure(font=("Arial",40))
        self.description=Label(self.frame1,text="DESCRIPCIÓN",background='#353437')
        self.description.configure(font=("Arial",40))
        self.habitat=Label(self.frame1,text="HÁBITAT",background='#353437')
        self.habitat.configure(font=("Arial",40))
        self.explanation=Label(self.frame1,text="EXPLICACIÓN",background='#353437')
        self.explanation.configure(font=("Arial",40))
        self.menu_window=menu
        self.roedor=roedor
        self.rules=rules
        self.addButton=Button(self.frame1,text="Agregar Roedor",command=self.add_roedor,bg="#7a7b7c", fg="white")
        self.addButton.config(height=2,width=15)
        self.menuButton=Button(self.frame1,text="Menú Principal",command=self.main_window,bg="#7a7b7c", fg="white")
        self.menuButton.config(height=2,width=15)
        self.showRoedor()

    def add_roedor(self):
        self.addfunction=addRoedor(self.menu_window,self.frame1,self.classifier)
        self.hide()
        self.addfunction.show()

    def show(self):
        self.name.pack()
        self.image.pack()
        self.size.pack()
        self.description.pack()
        self.habitat.pack()
        self.explanation.pack()

        if(self.roedor.nombre=="Desconocido"):
            self.addButton.pack(side=TOP)
        self.menuButton.pack(side=TOP)
   
    def hide(self):
        self.name.pack_forget()
        self.image.pack_forget()
        self.size.pack_forget()
        self.description.pack_forget()
        self.habitat.pack_forget()
        self.explanation.pack_forget()
        if(self.roedor.nombre=="Desconocido"):
            self.addButton.pack_forget()
        self.menuButton.pack_forget()

    def showRoedor(self):
        self.name=Label(self.frame1,text=self.roedor.nombre,background='#353437',fg="white")
        self.name.configure(font=("Arial",35))

        openImage=Image.open(self.roedor.imagen)
        img=openImage.resize((200,200))
        self.photo=ImageTk.PhotoImage(img)      
        self.image=Label(self.frame1,image=self.photo)

        self.size=Label(self.frame1,text=self.roedor.tamaño,wraplength=1200,background='#353437',fg="white")
        self.size.configure(font=("Arial",14))
        self.description=Label(self.frame1,text=self.roedor.descripcion,wraplength=1200,background='#353437',fg="white")
        self.description.configure(font=("Arial",14))
        self.habitat=Label(self.frame1,text=self.roedor.habitat,wraplength=1200,background='#353437',fg="white")
        self.habitat.configure(font=("Arial",14))
        exp="\n\n\nEl roedor fue encontrado en base a las siguientes características:\n"
        for key in self.rules.keys():
            exp+=key+":"+self.rules[key]+"\n"

        self.explanation=Label(self.frame1,text=exp,wraplength=1200,background='#353437',fg="white")
        self.explanation.configure(font=("Arial",14))

    def main_window(self):
        self.hide()
        self.menu_window.show()
   
    def closing(self):
        del self

class addRoedor:
    def __init__(self,menu,frame1,classifier)->None:
        self.frame1=frame1
        self.main_menu=menu
        self.classifier=classifier
        self.load_characteristics()
        self.labels = []
        self.entries = []

        for characteristic in self.characteristics:
            self.labels.append(Label(self.frame1,text=characteristic.capitalize(),background='#353437',fg="white"))
            if(characteristic=="descripcion" or characteristic=="habitat"):
                self.entries.append(Text(self.frame1, height=2, width=45))
            else:
                self.entries.append(Entry(self.frame1,width=60))
   
    def load_characteristics(self):
        self.characteristics = []
        self.characteristics.append("nombre")
        self.characteristics.append("tamaño")
        self.characteristics.append("color")
        self.characteristics.append("habitat")
        self.characteristics.append("descripcion")    
        self.characteristics.append("cola")
        self.characteristics.append("orejas")
        self.characteristics.append("patas")
        self.characteristics.append("pelaje")
   
    def show(self):
        self.title=Label(self.frame1,text="Agregar Roedor",background='#353437',fg="white")
        self.title.configure(font=("Arial",20))
        self.title.grid(column=1,row=1,columnspan=5)
        self.currentpos=3
        for i in range(len(self.labels)):
            self.labels[i].configure(font=("Arial",15))
            self.labels[i].grid(column=1,row=self.currentpos)
            self.entries[i].grid(column=2, row=self.currentpos)
            self.currentpos+=1

        self.filename=StringVar()
        self.image=Label(self.frame1,text="Imagen",background='#353437',fg="white")
        self.image.configure(font=("Arial",15))
        self.image.grid(column=1,row=23)
        self.showRute=Entry(self.frame1,textvariable=self.filename)
        self.showRute.config(state='disabled',width=60)
        self.showRute.grid(column=2,row=23)
        self.chooseImage=Button(self.frame1,text="Seleccionar Imagen",command=self.selectImage,bg="#7a7b7c",fg="white")
        self.chooseImage.config(height=1,width=15)
        self.chooseImage.grid(column=3,row=23)
        self.saveButton=Button(self.frame1,text="Guardar",command=self.save,bg="#7a7b7c",fg="white")
        self.saveButton.config(height=2,width=15)
        self.saveButton.grid(column=2,row=27)
        self.menuButton=Button(self.frame1,text="Menú Principal",command=self.main_window,bg="#7a7b7c", fg="white")
        self.menuButton.config(height=2,width=15)
        self.menuButton.grid(column=1,row=27)

    def selectImage(self):
        self.filename.set(fd.askopenfilename(initialdir = "/",title = "Seleccionar imagen",filetypes = (("jpeg files","*.jpg"),("all files","*.*"))))
       
    def hide(self):
        self.title.grid_remove()
        for i in range(len(self.labels)):
            self.labels[i].grid_remove()
            self.entries[i].grid_remove()
        self.chooseImage.grid_remove()
        self.image.grid_remove()
        self.showRute.grid_remove()
        self.saveButton.grid_remove()
        self.menuButton.grid_remove()
       
    def save(self):
        self.aux = roedor()
        for i in range(len(self.entries)):
            if(self.characteristics[i]=="descripcion" or self.characteristics[i]=="habitat"):
                if(self.characteristics[i]=="descripcion"):
                    self.aux.descripcion=self.entries[i].get(1.0,"end-1c")
                elif(self.characteristics[i]=="habitat"):
                    self.aux.habitat=self.entries[i].get(1.0,"end-1c")
            else:
                if(self.entries[i].get()!=""):
                    if(self.characteristics[i]=="nombre"):
                        self.aux.nombre=self.entries[i].get()
                    elif(self.characteristics[i]=="tamaño"):
                        self.aux.tamaño=self.entries[i].get()
                    elif(self.characteristics[i]=="color"):
                        self.aux.color=self.entries[i].get()
                    elif(self.characteristics[i]=="cola"):
                        self.aux.cola=self.entries[i].get()
                    elif(self.characteristics[i]=="orejas"):
                        self.aux.orejas=self.entries[i].get()
                    elif(self.characteristics[i]=="patas"):
                        self.aux.patas=self.entries[i].get()
                    elif(self.characteristics[i]=="pelaje"):
                        self.aux.pelaje=self.entries[i].get()
        self.currentpath = os.getcwd()
        self.currentpath+="\\sources\\"
        shutil.copy(self.filename.get(),self.currentpath)
        self.words=self.filename.get().split("/")
        self.aux.imagen="sources/"+self.words[-1]
        self.classifier.roedores.append(self.aux)
        self.hide()
        self.main_menu.show()
   
    def main_window(self):
        self.hide()
        self.main_menu.show()

class classifier:
    def __init__(self,menu,frame1) -> None:
        self.menu_window=menu
        self.frame1=frame1
        self.title=Label(self.frame1,text="Clasificador de Roedores",background='#353437',fg="white")
        self.title.configure(font=("Arial",35))

        self.menuButton=Button(self.frame1,text="Menú Principal",command=self.main_window,bg="#7a7b7c",fg="white")
        self.menuButton.config(height=10,width=50)
        self.roedores=[]
        self.default_roedor=roedor()
        self.load_roedores()
        self.loadall()
       
    def loadall(self):      
        self.good=False
        self.doing=True
       
        self.rules={}
        self.decision=self.roedores[0]
        self.visual=visualizer(self.menu_window,self.frame1,self.decision,self.rules,self)
        self.possible_rules={}
        self.possible_roedores=[]
       
    def load_roedores(self):
        self.default_roedor.nombre="Desconocido"
        self.default_roedor.imagen="sources/default.jpeg"
       
        self.aux = roedor()
        self.aux.nombre = "Ratón casero"
        self.aux.tamaño = "Pequeño"
        self.aux.color = "Gris"
        self.aux.habitat = "Áreas urbanas y rurales"
        self.aux.descripcion = "Roedor común en hogares y edificios"
        self.aux.cola = "Larga y escamosa"
        self.aux.orejas = "Grandes y redondeadas"
        self.aux.patas = "Pequeñas"
        self.aux.pelaje = "Corto y suave"
        self.aux.imagen = "sources/raton_casero.jpg"
        self.roedores.append(self.aux)
       
        self.aux = roedor()
        self.aux.nombre = "Rata noruega"
        self.aux.tamaño = "Grande"
        self.aux.color = "Marrón grisáceo"
        self.aux.habitat = "Áreas urbanas, alcantarillas, basureros"
        self.aux.descripcion = "Rata grande y robusta, considerada una plaga"
        self.aux.cola = "Larga y escamosa"
        self.aux.orejas = "Pequeñas"
        self.aux.patas = "Fuertes"
        self.aux.pelaje = "Áspero"
        self.aux.imagen = "sources/rata_noruega.jpg"
        self.roedores.append(self.aux)
       
        self.aux = roedor()
        self.aux.nombre = "Ardilla roja"
        self.aux.tamaño = "Mediano"
        self.aux.color = "Rojizo"
        self.aux.habitat = "Bosques de coníferas y caducifolios"
        self.aux.descripcion = "Ardilla arborícola con cola espesa"
        self.aux.cola = "Larga y espesa"
        self.aux.orejas = "Prominentes con penachos"
        self.aux.patas = "Fuertes y con garras afiladas"
        self.aux.pelaje = "Denso y suave"
        self.aux.imagen = "sources/ardilla_roja.jpg"
        self.roedores.append(self.aux)
       
        self.aux = roedor()
        self.aux.nombre = "Hámster"
        self.aux.habitat = "Mascotas domesticadas, originarios de Siria"
        self.aux.descripcion = "Roedor pequeño y popular como mascota"
        self.aux.cola = "Corta"
        self.aux.orejas = "Pequeñas y redondeadas"
        self.aux.patas = "Cortas"
        self.aux.pelaje = "Corto y suave"
        self.aux.imagen = "sources/hamster.jpg"
        self.roedores.append(self.aux)

        self.aux = roedor()
        self.aux.nombre = "Cobaya"
        self.aux.tamaño = "Mediano"
        self.aux.color = "Variado (blanco, negro, marrón, rojizo)"
        self.aux.habitat = "Mascotas domesticadas, originarias de Sudamérica"
        self.aux.descripcion = "Roedor dócil y sociable, también conocido como cuy o conejillo de indias"
        self.aux.cola = "Ausente"
        self.aux.orejas = "Pequeñas y redondeadas"
        self.aux.patas = "Cortas"
        self.aux.pelaje = "Corto, liso o crespo"
        self.aux.imagen = "sources/cobaya.jpg"
        self.roedores.append(self.aux)
       
    def question(self,q,opt):
        options=[]
        options.append("Otro")
        for key in opt.keys():
            options.append(key)
        self.selection=StringVar()
        self.chooses=StringVar()
        self.chooses.set("Otro")
        self.instructions=Label(self.frame1,text="Seleccione la característica correspondiente al roedor:\n\n",background='#353437',fg="white")
        self.instructions.configure(font=("Arial",25))
        self.instructions.pack()
        self.caracteristica=Label(self.frame1,text=q,background='#353437',fg="white")
        self.caracteristica.configure(font=("Arial",25))
        self.caracteristica.pack()
        self.drop=OptionMenu(self.frame1,self.chooses,*options)