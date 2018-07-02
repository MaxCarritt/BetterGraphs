def addGraphPoint(tp,label,description):
	window = system.nav.openWindow('BetterGraphs/BG_Add_Pen', {'label' : label, 'tp' : tp, 'description' : description})
	system.nav.centerWindow(window)


def deleteGraphPoint(tp):
	data = system.tag.read("[Client]BetterGraphs/BG_activeTagPens")
	data = data.value
	for row in range(data.getRowCount()):
		if tp == data.getValueAt(row,"TAG_PATH"):
			newdata = system.dataset.deleteRow(data, row)
	system.tag.write("[Client]BetterGraphs/BG_activeTagPens",newdata)
	project.BetterGraphs.updateGraph()
	
	
def clearGraphPoints():
	data = system.tag.read("[Client]BetterGraphs/BG_activeTagPens")
	data = data.value
	newdata = system.dataset.clearDataset(data)
	system.tag.write("[Client]BetterGraphs/BG_activeTagPens",newdata)
	project.BetterGraphs.updateGraph()
	
def clearAxisPoints():
	data = system.tag.read("[Client]BetterGraphs/BG_activeAxis")
	data = data.value
	newdata  = system.dataset.clearDataset(data)
	system.tag.write("[Client]BetterGraphs/BG_activeAxis",newdata)
	project.BetterGraphs.updateGraph()

def clearSubplotPoints():
	data = system.tag.read("[Client]BetterGraphs/BG_activeSubplots")
	data = data.value
	newdata  = system.dataset.clearDataset(data)
	system.tag.write("[Client]BetterGraphs/BG_activeSubplots",newdata)
	project.BetterGraphs.updateGraph()

def updateGraph():
	try:
		window = system.gui.getWindow("BetterGraphs/BG_Graph")
		if window != None:
			data = system.tag.read("[Client]BetterGraphs/BG_activeTagPens")
			data = data.value
			window = system.gui.getWindow("BetterGraphs/BG_Graph")
			window.rootContainer.Data = data
	except:
		pass
	
	
	try:
		window2 = system.gui.getWindow("BetterGraphs/BG_Graph_Config")
		if window2 != None:
			data = system.tag.read("[Client]BetterGraphs/BG_activeTagPens")
			data = data.value
			window2 = system.gui.getWindow("BetterGraphs/BG_Graph_Config")
			window2.rootContainer.Data = data
	except: 
		pass
	

#creates dropdown menu to either add or remove pen
def showPopup(event):
	tp = event.source.getPropertyValue("tagPath") # defined at object
	menuNames = []
	menuFunctions = []
	def fake(event):
		pass
	
	menuNames.append("<html><i>%s" % tp)
	menuFunctions.append(fake)
	menuNames.append("sep")
	menuFunctions.append(None)
	penlist= system.tag.read("[Client]BetterGraphs/BG_activeTagPens")
	penlist = penlist.value
	probe  = False
	
	#check if taglist already has tag
	if penlist.getRowCount() == 0:
		probe = False
	else:	
		for row in range(penlist.getRowCount()):
			if penlist.getValueAt(row,"TAG_PATH") == tp:
				probe = True
		
	if probe == True:
		def subFromCGraph(event):
				project.BetterGraphs.deleteGraphPoint(tp)
		menuNames.append("<html>(-)  Remove from Graph")
		menuFunctions.append(subFromCGraph)
	else:
		def addToCGraph(event):
				tp = event.source.getPropertyValue("tagPath")
				label = event.source.getPropertyValue("label")
				description = event.source.getPropertyValue("description")
				project.BetterGraphs.addGraphPoint(tp,label,description)
		menuNames.append("<html>(+) Add to Graph")
		menuFunctions.append(addToCGraph)
		
	menuNames.append("sep")
	menuFunctions.append(None)

	def clearGraph(event):
		project.BetterGraphs.clearGraphPoints()

	def openGraph(event):
		project.BetterGraphs.openCurrentGraph()

	menuNames.append("Open Current Graph")
	menuFunctions.append(openGraph)

	popupMenu = system.gui.createPopupMenu(menuNames, menuFunctions)
	popupMenu.show(event)


# Opens the graph window
def openCurrentGraph():
	system.nav.openWindow("BetterGraphs/BG_Graph")
	system.nav.centerWindow("BetterGraphs/BG_Graph")



# Gets a list of VALID datasources and databases
def getDataSources():
	connections = system.dataset.toPyDataSet(system.db.getConnections())	
	databases = []
	datasources = []
	index = 0
	for con in connections:
		if con["Status"].upper() == "VALID" or con["Status"] == "":
			datasources.append([index, con["Name"]])
			try:
				if con["DBType"] == "MYSQL":
					databases.append([index, system.db.runScalarQuery("SELECT DATABASE()", con["Name"]) + "."])
				elif con["DBType"] == "MSSQL":
					databases.append([index, system.db.runScalarQuery("SELECT DB_NAME()", con["Name"]) + ".dbo."])	
			except:
				print "Error getting DBName"
			index += 1
	return (datasources, databases)

# Updates properties with database info
def initializeDataSources(window):
	win = system.gui.getWindow(window)
	data = project.BetterGraphs.getDataSources()
	win.rootContainer.datasources = system.db.toDataSet(["Index", "DataSource"], data[0])
	win.rootContainer.databases = system.db.toDataSet(["Index", "Database"], data[1])
	return 1
