#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
plenAUTO

Esta aplicación está cedida temporalmente a DIAMOND SEGURIDAD S.L.
PROPIEDAD DE D.GOMEZ CALLES
Todos los derechos reservados.'''

#Librería de interfaz
from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from tkinter import messagebox
from tkinter import ttk

#Utilizado solo para mostrar los logos.
from PIL import Image, ImageTk

#Imports necesarios varios
from tika import parser
import os
import re
import math

#Librería para generar PDF's
import pdfkit ##wkhtmltopdf
#Ruta de configuración a wkhtmltopdf
kit = pdfkit.configuration(wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

class Aplicacion():
	''' Clase monolitica que encapsula la interfaz y las funciones necesarias para su
	correcto desarrollo.'''
	def __init__(self):
		''' Creación de la interfaz y todas sus variables asociadas'''
		self.raiz = Tk()
		self.raiz.geometry('') 		#La línea de geometría sin definir ningún tamaño hace que la interfaz sea autoadaptable.
		self.fontTITLE = Font(size = 30)
		self.font = Font(size = 16)
		buttStyle = ttk.Style()
		buttStyle.configure("size.TButton", font = ("Helvetica",16))
		self.raiz.configure(bg = 'white')
		self.raiz.title('Incidencias Diarias plenoil')
		self.adjunto = None #Variable que almacena el archivo adjunto
		self.initDIR = "\\\\192.168.102.5\\t. de noche"
		##################
		##LOGOS y TITULO##
		##################
		diamondLOGO = ImageTk.PhotoImage(Image.open("logodiamond.png").resize((120,120)))
		plenoilLOGO = ImageTk.PhotoImage(Image.open("logoplenoil.png").resize((120,120)))
		self.diamondLOGO = ttk.Label(self.raiz, image = diamondLOGO)
		self.diamondLOGO.grid(column=5, row = 0, columnspan = 2)
		self.plenoilLOGO = ttk.Label(self.raiz, image = plenoilLOGO)
		self.plenoilLOGO.grid(column=0, row = 0, columnspan = 2)
		self.titleLABEL = ttk.Label(self.raiz, text= "INCIDENCIAS DIARIAS PLENOIL", font = self.fontTITLE)
		self.titleLABEL.grid(column = 2, row = 0, columnspan = 3)
		###########
		##BOTONES##
		###########
		self.sendBUTTON = ttk.Button(self.raiz, text="PROCESAR",
										command=self.procesar, style = "size.TButton")
		self.adjBUTTON = ttk.Button(self.raiz, text="ADJUNTAR",
										command=self.adjuntar, style = "size.TButton")
		self.incNAME = ttk.Label(self.raiz, text="", font = self.font)
		####################################
		##DISPOSICION INTERFAZ BASICA FIJA##
		####################################
		self.adjBUTTON.grid(column=1, row = 11, columnspan = 3, pady = 20)
		self.sendBUTTON.grid(column=3, row = 11, columnspan = 3, pady = 20)
		self.incNAME.grid(column=2, row = 1, columnspan = 3, pady = 20)
		##INICIO DEL BUCLE PRINCIPAL##
		self.raiz.mainloop()
	def parseTXTfromPDF(self):
		file_data = parser.from_file(self.adjunto)
		target = ""
		targetF = None
		text = file_data['content']
		filesArray = []
		for line in text.split("\n"):
			if line is not "":
				if "OIL-" in line:
					target = line
					filesArray.append(target+".txt")
					if targetF == None:
						targetF = open(target+".txt","w")
					else:
						targetF.close()
						targetF = open(target+".txt","w")
					targetF.write(line+"\n")
				else:
					if targetF is not None:
						if "Fecha" not in line:
							targetF.write(line+"\n")
		if targetF is not None:
			targetF.close()
		return filesArray
	def genHTMLheader(self,cuenta,direccion,fecha):
		return "<body style = 'font-family: sans-serif; font-size: 60%'>"\
		+"<div style='margin-bottom: 20px;'><h1>Reporte histórico de eventos</h1>"\
		+"<hr>"\
		+"<img src='logodiamond.png' width = '125px' height= '100px' style = 'float: left; margin: 50px; margin-bottom: 0px; margin-top: 20px'>"\
		+"<h2>PLENOIL (RED DE ESTACIONES DE SERVICIO)</h2>"\
		+"<div style=''><p style ='font-weight: bold; display: inline-block'>Cuenta:</p><p style ='display: inline-block'> "\
		+cuenta+"</p></div>"\
		+"<div style=''><p style ='font-weight: bold; display: inline-block'>Direccion:</p><p style ='display: inline-block'> "\
		+direccion+"</p></div>"\
		+"<div style=''><p style ='font-weight: bold; display: inline-block'>Rango fecha del reporte:</p><p style ='display: inline-block'> "\
		+fecha+" - "+fecha+"</p></div>\n<hr></div>"
	def genHTMLfromTXT(self,fArray):
		hArray = []
		for f in fArray:
			target = f[:-3]+"html"
			hArray.append(target)
			src = open(f,"r")
			out = open(target, "w")
			lines = src.read().split("\n")
			htHEADER = self.genHTMLheader(lines[0],lines[1],lines[2][:10])
			out.write(htHEADER)
			for line in lines:
				if line is not "":
					if line == lines[0] or line == lines[1]:
						pass
					else:
						eventTitle = re.search(r'\d\d/\d\d/\d\d\d\d',line[:10])
						try:
							if line[:10] == eventTitle.group():
								if "SISTEMA ARMADO" in line or "CONEXIÓN" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: #CDB796'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
								elif "SISTEMA DESARMADO" in line or "Desconexión" in line or "Apertura Fuera" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: #338CF9'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
								elif "EVENTO GENERADO" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: #00CCFF'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
								elif "130E" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: #FF80C0'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
								elif "ACCESO BIDIRECCIONAL" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: #FFFF99'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
								elif "REST." in line or "130R" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: #33CCCC'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
								elif "RONDA VIRTUAL" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style =''>"
											+"<h2 style ='padding-left: 1em; color: #0000FF; margin: 0px'>"
											+line+"</h2></div>\n")
								elif "Anulacion de zona" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: #C0C0C0'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
								elif "FALLO DE COMUNICACIÓN" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: #00FF80'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
								elif "625R" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: #CC99FF'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
								elif "Test periódico Recibido" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: #18BAEF'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
								elif "Aun No Cerro" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: #cc99ff'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
								elif "Hora Auto-Armado" in line:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: ##ff8080'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
								else:
									out.write("</div>\n"
											+"<div style= 'border: 1px solid black; margin: 1em'>"
											+"<div style ='background-color: white'>"
											+"<h2 style ='padding-left: 1em; margin: 0px'>"
											+line+"</h2></div>\n")
						except:
							if "Observación" in line:
								out.write("<p style ='padding-left: 1em; font-weight: bold'>"+line+"</p>\n")
							else:
								out.write("<p style ='padding-left: 1em'>"+line+"</p>\n")
			src.close()
			os.remove(f)
			out.close()
		return hArray
	def genPDFfromHTML(self,hArray):
		for ht in hArray:
			print(ht[:-4])
			pdfkit.from_file(ht,ht[:-4]+"pdf",configuration=kit)
			os.remove(ht)
	def adjuntar(self):
		self.adjunto = filedialog.askopenfile(initialdir=self.initDIR, parent=self.raiz,mode='rb',title='Examinar...')
		if self.adjunto == None:
			pass
		else:
			self.incNAME["text"] = self.adjunto.name.split("/")[-1]
	def procesar(self):
		if self.adjunto == None:
			messagebox.showerror("ERROR","NO HAY INFORME ADJUNTO")
		else:
			files = self.parseTXTfromPDF()
			htmls = self.genHTMLfromTXT(files)
			self.genPDFfromHTML(htmls)
			self.incNAME["text"] = "TERMINADO"

def main():
	mi_app = Aplicacion()
	return 0


if __name__ == '__main__':
	main()
