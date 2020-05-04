from tika import parser

fPath = "fullPLENOIL03.pdf"

file_data = parser.from_file(fPath, xmlContent=True)
target = ""
targetF = None
text = file_data['content']
for line in text.split("\n"):
	if line is not "":
		if "OIL-" in line:
			target = line[3:]
			#print(target)
			if targetF == None:
				targetF = open(target+".html","w")
			else:
				targetF.close()
				targetF = open(target+".html","w")
			if "(REED MARC)" in line:
				targetF.write("<h1>"+line[3:]+"</h1>")
		else:
			if targetF is not None:
				if line is not "<p></p>":
					targetF.write(line)
		
