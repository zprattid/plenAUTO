from tika import parser
import os
import re
import pdfkit ##wkhtmltopdf

kit = pdfkit.configuration(wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

fPath = "fullPLENOIL03.pdf"

def parseTXTfromPDF(fPath):
	file_data = parser.from_file(fPath)
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

def genHTMLheader(cuenta,direccion,fecha):
	return "<body style = 'font-family: sans-serif'>"\
	+"<h1>Reporte histórico de eventos</h1>"\
	+"<hr>"\
	+"<img src='logodiamond.png' width = '125px' height= '100px' style = 'float: left; margin: 50px'>"\
	+"<h2>PLENOIL (RED DE ESTACIONES DE SERVICIO)</h2>"\
	+"<div style=''><p style ='font-weight: bold; display: inline-block'>Cuenta:</p><p style ='display: inline-block'> "\
	+cuenta+"</p></div>"\
	+"<div style=''><p style ='font-weight: bold; display: inline-block'>Direccion:</p><p style ='display: inline-block'> "\
	+direccion+"</p></div>"\
	+"<div style=''><p style ='font-weight: bold; display: inline-block'>Rango fecha del reporte:</p><p style ='display: inline-block'> "\
	+fecha+" - "+fecha+"</p></div>\n<hr>"

def genHTMLfromTXT(fArray):
	hArray = []
	for f in fArray:
		target = f[:-3]+"html"
		hArray.append(target)
		src = open(f,"r")
		out = open(target, "w")
		lines = src.read().split("\n")
		htHEADER = genHTMLheader(lines[0],lines[1],lines[2][:10])
		out.write(htHEADER)
		for line in lines:
			if line is not "":
				if line == lines[0] or line == lines[1]:
					pass
				else:
					eventTitle = re.search(r'\d\d/\d\d/\d\d\d\d',line[:10])
					try:
						if line[:10] == eventTitle.group():
							if "SISTEMA ARMADO" in line or "Conexión" in line:
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
							elif "Alarma de Robo" in line:
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
							elif "REST." in line:
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
		
def genPDFfromHTML(hArray):
	for ht in hArray:
		pdfkit.from_file(ht,ht[:-4]+"pdf",configuration=kit)
		os.remove(ht)
		
files = parseTXTfromPDF(fPath)
htmls = genHTMLfromTXT(files)
genPDFfromHTML(htmls)
