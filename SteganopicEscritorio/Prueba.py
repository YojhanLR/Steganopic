# -*- coding: utf-8 -*-

from Tkinter import *
from stegapy import decode, encode
#importamos la opción para seleccionar archivos
import Tkinter, Tkconstants, tkFileDialog
import sys


from tkFileDialog   import askopenfilename
from tkFileDialog   import asksaveasfile
from PIL import Image
from ScrolledText import *



vent = Tk()
#tamaño a la vntana geometry()
vent.geometry("500x300")
#titulo de la ventana1
vent.title("Proyecto de Fourier")
#scrollbar texto



#-------------------------------
#abrir la otra ventana 2
def abrirventana2():
    #cierro la ventana 1
    vent.withdraw()

    #Abro la nueva ventana
    vent2=Toplevel()
    vent2.geometry("500x300")

    
    #titulo de la ventana2
    vent2.title("Proyecto de Fourier")

    lblAnuncio = Label(vent2,text="Selecciona el archivo que ocultará tu mensaje y luego dale un nuevo nombre " ).place(x=50, y=40)
    #lblNombre = Label(vent2,text="Ingrese el nombre del archivo en donde vas a guardar el mensaje: ").place(x=50, y=50)
    #entradaN = StringVar()
    #txtNombre = Entry(vent2, textvariable=entradaN,width=30).place(x=50, y=70)
    #lbl1 = Label(vent2,text=".JPG").place(x=240, y=70)


    lblMensaje = Label(vent2,text="Ingrese el mensaje a ocultar: ").place(x=50, y=80)
    entrada = StringVar()
    txtArchivo = Entry(vent2, textvariable=entrada,width=60).place(x=50, y=120)


    lblNuevo = Label(vent2,text="Ingrese el nombre del nuevo archivo: ").place(x=50, y=150)
    entradaNu = StringVar()
    txtNuevo = Entry(vent2, textvariable=entradaNu,width=30).place(x=50, y=170)
    lbl3 = Label(vent2,text=".PNG").place(x=240, y=170)



    def stegano():
                    
        info = entrada.get()
        lblMensaje1 = Label(vent2,text= entrada.get()).place(x=200, y=0)
            
             
        img_stegana = askopenfilename(filetypes=[("Imagem PNG","*.jpg")])
        print img_stegana
        encode(entrada.get(),img_stegana,entradaNu.get()+".png")
        #encode(entrada.get(),"",entradaNu.get()+".png")
        lblMensajeS = Label(vent2,text= "El mensaje ha sido guardado con éxito!!").place(x=50, y=240)

    def regresar():
        #cierro la ventana 2 Y REGRESO 
        vent2.withdraw()
        vent.deiconify()        
        
        
    
        
        
    #Botón ocultar mensaje
    btnOcultar = Button(vent2,text="Ocultar mensaje",command = stegano).place(x=50, y=200)

    btnRegresar = Button(vent2,text="Regresar", command = regresar).place(x=400, y=250)
    

#------------ Abrir ventana de mostrar (3)
    
def abrirventana3():
    #cierro la ventana 1
    vent.withdraw()

    #Abro la nueva ventana
    vent3=Toplevel()
    vent3.geometry("500x300")

    
    #titulo de la ventana2
    vent3.title("Proyecto de Fourier")
    
    #img_stegana = askopenfilename(filetypes=[("Imagem PNG","*.jpg")])
       
    #im = Image.open(img_stegana)

   # lblArchivo = Label(vent3,text="Ingrese el nombre del archivo: ").place(x=50, y=40)
    #entradaA = StringVar()
    #txtArchivo = Entry(vent3, textvariable=entradaA,width=30).place(x=50, y=70)
    #lbl1 = Label(vent3,text=".PNG").place(x=240, y=70)
 
   
    def decodi ():

        img_steg = askopenfilename(filetypes=[("Imagem PNG","*.png")])
        print img_steg
        
        decode(img_steg)
        a = decode(img_steg)

        textPad = ScrolledText(vent3, width=30, height=10)
        textPad.pack()

        textPad.insert(INSERT, "El mensaje oculto es: \n\n"  + a )
        textPad.place(x=50, y=100)
        
        #lbl3 = Label(vent3,text="El mensaje oculto es: '" + a + "'").place(x=50, y=100)


    def regresar2():
        #cierro la ventana  Y REGRESO 
        vent3.withdraw()
        vent.deiconify()        
             
    
    #Botón mostrar mensaje
    btnM = Button(vent3,text="Seleccione el archivo",command = decodi).place(x=50, y=40)

    btnRegresar = Button(vent3,text="Regresar", command = regresar2).place(x=400, y=250)

    
botonN=Button(vent,text=" Esteganografia ",command=abrirventana2).place(x=200, y=30)

btnMostrar = Button(vent,text=" Mostrar mensaje ",command = abrirventana3).place(x=195, y=70)

    
#----------------------------------------------------



    
vent.mainloop()
