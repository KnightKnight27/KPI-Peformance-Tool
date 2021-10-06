from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
Df=pd.DataFrame()
window = Tk()
chosenKpi= StringVar()
chosenCell=StringVar()
Sitechosen=StringVar()
chosenMultipleKpi=StringVar()
CellState=[]
SiteState=[]
KPIState=[]
ListOfCells=[]
ListOfSites=[]
ListOfKPIs=[]
colors=["blue","red",'green',"pink","orange","brown","maroon","darkvoilet","lime"]
def browseFiles():
	filename = filedialog.askopenfilename(initialdir = "/home/kartik/Downloads",title = "Select a File",filetypes = (("CSV Files","*.csv*"),("Excel Files","*.xls*")))
	global Df
	global CellState
	global KPIState
	for i in range(50):
		x=IntVar(0)
		CellState.append(x)
	for i in range(50):
		x=IntVar(0)
		SiteState.append(x)
	for i in range(150):
		x=IntVar(0)
		KPIState.append(x)
	Df=pd.read_csv(filename)
	button_plot1.grid(column=1,row=12)
	button_plot2.grid(column=1,row=13)
	button_plot3.grid(column=1,row=14)
	fileState= Label(window,text="CSV Uploaded").grid(column=1,row=3)
	KPIHeaders=[]  
	NonKPIHeaders=[] 
	for column in Df:
		flagCheckNumber=True
		ListToStoreValues=[]
		for row in Df[column].tolist():
			if(type(row)!=type("")):
				ListToStoreValues.append(row)
			else:
				value=''.join(row.split(","))
				if(value[0]=='-'):
					value=value[1:]
					if('.' in value):
						temp=''.join(value.split("."))
						if(temp.isnumeric()==False):
							flagCheckNumber=False
							break
						else:
							push=float(value)
							ListToStoreValues.append(-push)
					else:
						if(value.isnumeric()==False):
							flagCheckNumber=False
							break
						else:
							push=int(value)
							ListToStoreValues.append(-push)
				else:
					if('.' in value):
						temp=''.join(value.split("."))
						if(temp.isnumeric()==False):
							flagCheckNumber=False
							break
						else:
							push=float(value)
							ListToStoreValues.append(push)
					else:
						if(value.isnumeric()==False):
							flagCheckNumber=False
							break
						else:
							push=int(value)
							ListToStoreValues.append(push)

		if flagCheckNumber:
			KPIHeaders.append(column)
			Df[column]=ListToStoreValues
		else: 
			NonKPIHeaders.append(column)
	selectedKPI['values']= KPIHeaders
	for i in range(len(NonKPIHeaders)):
		original_name=NonKPIHeaders[i]
		modified = '_'.join(NonKPIHeaders[i].split(" "))
		NonKPIHeaders[i]= modified.upper()
		Df.rename(columns = {original_name:NonKPIHeaders[i]}, inplace = True)
	global ListOfCells
	global ListOfSites
	global ListOfKPIs
	ListOfSites=list(set(Df['SITE'].tolist()))
	cnt=0
	for i in ListOfSites:
		x= SiteState[cnt]
		selectedSite2.menu.add_checkbutton(label=i,variable = x)
		cnt+=1
	if('CELL' not in NonKPIHeaders):
		return 
	ListOfCells=list(set(Df['CELL'].tolist()))
	ListOfCells.sort()
	cnt=0
	for i in ListOfCells:
		x=CellState[cnt]
		selectedCell2.menu.add_checkbutton(label=i,variable = x)
		cnt+=1
	tempList=Df.columns.tolist()
	ListOfKPIs=[]
	f=["Period start time",	"REGION",	"MARKET",	"TAC","SITE",	"ENODEB",	"CELL"]

	for i in tempList:
		if i not in f:
			ListOfKPIs.append(i)
	print(ListOfKPIs)
	cnt=0
	for i in ListOfKPIs:
		x= KPIState[cnt]
		selectedkpi2.menu.add_checkbutton(label=i,variable=x)
		cnt+=1

def plot1():
	KPI=chosenKpi.get()
	GRAPH=Graphchosen.get()
	ToBePlotted=[]
	for i in range(len(ListOfCells)):
		if( CellState[i].get()==1):
			CELL= ListOfCells[i]
			ToBePlotted.append(CELL) 
	max_dates=0
	base_index=0
	for i in range(len(ToBePlotted)):
		CELL  = ToBePlotted[i]
		DF    = Df.loc[(Df["CELL"]==CELL)]
		dates = len(DF.index)
		if max_dates<dates:
			max_dates= dates
			base_index=i 
	CELL= ToBePlotted[base_index]
	DF=Df.loc[(Df["CELL"]==CELL)]
	BasePlot= DF.plot(kind=GRAPH,x="PERIOD_START_TIME",y=KPI)
	Dates=DF['PERIOD_START_TIME'].tolist()
	plt.ylabel(KPI)
	indexes=[i for i in range(len(DF.index))]
	DF['TempCol']=indexes
	DF.set_index('TempCol',inplace=True)
	plt.xticks(DF.index, DF['PERIOD_START_TIME'],rotation=90)
	Legends=[CELL]
	for i in range(len(ToBePlotted)):
		if(i==base_index):
			continue
		CELL = ToBePlotted[i]
		DF   = Df.loc[(Df["CELL"]==CELL)]
		DF.plot(kind=GRAPH,x="PERIOD_START_TIME",y=KPI,ax=BasePlot,color=colors[i]) 
		plt.legend([CELL],loc='upper left')
		indexes=[i for i in range(len(DF.index))]
		DF['TempCol']=indexes
		DF.set_index('TempCol',inplace=True)
		plt.xticks(DF.index, DF['PERIOD_START_TIME'],rotation=90)
		Legends.append(CELL)
	plt.legend(Legends,loc='upper left')
	plt.gcf().subplots_adjust(bottom=0.15)
	plt.show()
	chosenKpi.set("")
	chosenCell.set("")
	Graphchosen.set("")
	Sitechosen.set("")
def plot3():
	GRAPH=Graphchosen.get()
	ToBePlotted=[]
	for i in range(len(ListOfKPIs)):
		if(KPIState[i].get()==1):
			KPI= ListOfKPIs[i]
			ToBePlotted.append(KPI)
	CELL=""
	for i in range(len(ListOfCells)):
		if(CellState[i].get()==1):
			CELL = ListOfCells[i]
			break
	if(CELL==""):
		DF=Df.loc[(Df["CELL"]==CELL)]
		BasePlot= DF.plot(kind=GRAPH,x="PERIOD_START_TIME",y=ToBePlotted[0])
		Dates=DF['PERIOD_START_TIME'].tolist()
		plt.ylabel(CELL)
		indexes=[i for i in range(len(DF.index))]
		DF['TempCol']=indexes
		DF.set_index('TempCol',inplace=True)
		plt.xticks(DF.index, DF['PERIOD_START_TIME'],rotation=90)
		Legends=[ToBePlotted[0]]
		for i in range(1,len(ToBePlotted)):
			DF.plot(kind=GRAPH,x="PERIOD_START_TIME",y=ToBePlotted[i],ax=BasePlot,color=colors[i]) 
			plt.legend([ToBePlotted[i]],loc='upper left')
			indexes=[i for i in range(len(DF.index))]
			DF['TempCol']=indexes
			DF.set_index('TempCol',inplace=True)
			plt.xticks(DF.index, DF['PERIOD_START_TIME'],rotation=90)
			Legends.append(ToBePlotted[i])
		plt.legend(Legends,loc='upper left')
		plt.gcf().subplots_adjust(bottom=0.15)
		plt.show()
		chosenKpi.set("")
		chosenCell.set("")
		Graphchosen.set("")
		Sitechosen.set("")
	else:
		for i in range(len(ListOfSites)):
			if(SiteState[i].get()==1):
				CELL = ListOfSites[i]
				break
		DF=Df.loc[(Df["CELL"]==CELL)]
		BasePlot= DF.plot(kind=GRAPH,x="PERIOD_START_TIME",y=ToBePlotted[0])
		Dates=DF['PERIOD_START_TIME'].tolist()
		plt.ylabel(CELL)
		indexes=[i for i in range(len(DF.index))]
		DF['TempCol']=indexes
		DF.set_index('TempCol',inplace=True)
		plt.xticks(DF.index, DF['PERIOD_START_TIME'],rotation=90)
		Legends=[ToBePlotted[0]]
		for i in range(1,len(ToBePlotted)):
			DF.plot(kind=GRAPH,x="PERIOD_START_TIME",y=ToBePlotted[i],ax=BasePlot,color=colors[i]) 
			plt.legend([ToBePlotted[i]],loc='upper left')
			indexes=[i for i in range(len(DF.index))]
			DF['TempCol']=indexes
			DF.set_index('TempCol',inplace=True)
			plt.xticks(DF.index, DF['PERIOD_START_TIME'],rotation=90)
			Legends.append(ToBePlotted[i])
		plt.legend(Legends,loc='upper left')
		plt.gcf().subplots_adjust(bottom=0.15)
		plt.show()
		chosenKpi.set("")
		chosenCell.set("")
		Graphchosen.set("")
		Sitechosen.set("")

def plot2():
	KPI=chosenKpi.get()
	GRAPH=Graphchosen.get()
	ToBePlotted=[]
	for i in range(len(ListOfSites)):
		if( SiteState[i].get()==1):
			SITE= ListOfSites[i]
			ToBePlotted.append(SITE) 
	max_dates=0
	base_index=0
	for i in range(len(ToBePlotted)):
		SITE  = ToBePlotted[i]
		DF    = Df.loc[(Df["SITE"]==SITE)]
		dates = len(DF.index)
		if max_dates<dates:
			max_dates= dates
			base_index=i 
	SITE= ToBePlotted[base_index]
	DF=Df.loc[(Df["SITE"]==SITE)]
	BasePlot= DF.plot(kind=GRAPH,x="PERIOD_START_TIME",y=KPI)
	plt.ylabel(KPI)
	indexes=[i for i in range(len(DF.index))]
	DF['TempCol']=indexes
	DF.set_index('TempCol',inplace=True)
	plt.xticks(DF.index, DF['PERIOD_START_TIME'],rotation=90)
	Legends=[SITE]
	for i in range(len(ToBePlotted)):
		if(i==base_index):
			continue
		SITE = ToBePlotted[i]
		DF   = Df.loc[(Df["SITE"]==SITE)]
		DF.plot(kind=GRAPH,x="PERIOD_START_TIME",y=KPI,ax=BasePlot,color=colors[i]) 
		plt.legend([SITE],loc='upper left')
		indexes=[i for i in range(len(DF.index))]
		DF['TempCol']=indexes
		DF.set_index('TempCol',inplace=True)
		plt.xticks(DF.index, DF['PERIOD_START_TIME'],rotation=90)
		Legends.append(SITE)
	plt.legend(Legends,loc='upper left')
	plt.gcf().subplots_adjust(bottom=0.15)
	plt.show()
	chosenKpi.set("")
	chosenCell.set("")
	Graphchosen.set("")
	Sitechosen.set("")
window.title('File Explorer')
window.geometry("500x500")
window.config(background = "white")
label_file_explorer = Label(window,text = "Upload your CSV ",width = 100, height = 4,fg = "blue")	
button_explore = Button(window,text = "Browse Files",command = browseFiles)
button_plot1=Button(window,text="plot on Selected Cells",command=plot1)
button_plot2=Button(window,text="plot on Selected Sites",command=plot2)
button_plot3=Button(window,text="plot on Multiple Kpis",command=plot3)

label_file_explorer.grid(column = 1, row = 1)
button_explore.grid(column = 1, row =2)
ttk.Label(window, text = "KPI PERFORMANCE MONITORING TOOL",
		background = 'green', foreground ="white",
		font = ("Times New Roman", 15)).grid(row = 0, column = 1)
ttk.Label(window, text = "Select The KPI for which you want to plot:",
		font = ("Times New Roman", 10)).grid(column = 0,
		row = 7, padx = 10, pady = 25)
ttk.Label(window, text = "Select The CELL for which you want to plot:",
		font = ("Times New Roman", 10)).grid(column = 0,
		row = 6, padx = 10, pady = 25)



selectedCell2 = Menubutton (window,text="DropDown Menu to Select CELL", relief=RAISED,direction=RIGHT,width=27)
selectedCell2.menu= Menu(selectedCell2,tearoff=0)
selectedCell2["menu"]= selectedCell2.menu



ttk.Label(window, text = "Select The Multiple KPI for which you want to plot:",
		font = ("Times New Roman", 10)).grid(column = 0,
		row = 9, padx = 10, pady = 25)



selectedkpi2 = Menubutton (window,text="DropDown Menu to Select KPI", relief=RAISED,direction=RIGHT,width=27)
selectedkpi2.menu= Menu(selectedkpi2,tearoff=0)
selectedkpi2["menu"]= selectedkpi2.menu

                         

ttk.Label(window, text = "Select The Site for which you want to plot:",
		font = ("Times New Roman", 10)).grid(column = 0,
		row = 5, padx = 10, pady = 25)

selectedSite2 = Menubutton (window,text="DropDown Menu to Select SITE", relief=RAISED,direction=RIGHT,width=27)
selectedSite2.menu= Menu(selectedSite2,tearoff=0)
selectedSite2["menu"]= selectedSite2.menu

ttk.Label(window, text = "Select The Graph for which you want to plot:",
		font = ("Times New Roman", 10)).grid(column = 0,
		row = 8, padx = 10, pady = 25)


Graphchosen=StringVar()
selectedGraph = ttk.Combobox(window, width = 27, textvariable = Graphchosen)
selectedGraph['values'] = ('bar','line','scatter')
selectedKPI = ttk.Combobox(window, width = 27, textvariable = chosenKpi)
selectedKPI['values'] = ['Upload Your CSV First']
selectedSite2.grid(column =1 ,row = 5)
selectedCell2.grid(column =1,row = 6)
selectedKPI.grid(column = 1, row=7)
selectedGraph.grid(column  = 1, row=8)
selectedkpi2.grid(column=1,row=9)
window.mainloop()




