from importModules import *

'------------------------------------------------------------------------------------------------------------'		
# FIRST TIER TABLES

def addNew(model,entry):
	if not model.objects.filter(name__iexact=entry):
		newEntry = model(name=entry)
		newEntry.save()
		print 'saved:',newEntry,'in',model
	else:
		print entry,'already exists'
'------------------------------------------------------------------------------------------------------------'	
# SECOND TIER TABLES

def checkModel(model,entry):
	if model.objects.filter(name__iexact=entry):
		instance = model.objects.get(name__iexact=entry)
	else:
		instance = None
	return instance
		
def checkValue(value,type):
	try:
		test = type(value)
	except ValueError:
		test = 'noneType'
	return test

def roleAllocation(rownum,col,sheet):
	roles = {}
	for colnum in range(sheet.ncols):
		if col+colnum < len(range(sheet.ncols)):
			roleName = sheet.cell(rownum,col+colnum)
			col += 1
			allocation = sheet.cell(rownum,col+colnum)
			if checkValue(allocation.value,float) != 'noneType' and Role.objects.filter(name__iexact=roleName.value):
				roles[Role.objects.get(name__iexact=roleName.value)] = allocation.value
	return roles
	
def workingValue(products,productName,product,index,Model):
	# ! DELETE ALL PREVIOUS WORKING VALUES - DEFAULT SHOULD OVERRIDE EXISTING PRODUCT INFO
	Model.objects.filter(product=product).delete()
	for role in products[productName][index]:
		newEntry = Model(product=product,role=role)
		newEntry.pct = float(products[productName][index][role])
		newEntry.save()
		
#Creates a list of entries in the template build under each header
def listFunction(model):
	list = []
	for option in model.objects.all():
		list.append(option.name)
	return sorted(list)
	
#Creates the Sheet value for the data validation
def rangeString(sheet,col,row,rowend):
	range = '='+sheet+'!$'+chr(col+ord('A'))+'$'+str(row)+':$'+chr(col+ord('A'))+'$'+str(rowend)
	return range
	
#Checks the WB Headers against the headers in the template
def checkWBHeaders(sheet,headers,index):
	WBHeaders = []
	for colnum in range(sheet.ncols):
		WBHeaders.append(sheet.cell(index,colnum).value)
	if WBHeaders[:len(headers)] == headers:
		return True
	else:
		return False
'------------------------------------------------------------------------------------------------------------'	
# THIRD TIER TABLES

def unitFrcst(rownum,col,sheet):
	units = []
	for colnum in range(sheet.ncols):
		if col+colnum < len(range(sheet.ncols)):
			year = sheet.cell(0,col+colnum)
			qtr = sheet.cell(1,col+colnum)
			unit = sheet.cell(rownum,col+colnum)
			if year.value != '' and qtr.value != '':
				if Year.objects.filter(year=year.value) and Qtr.objects.filter(qtr=qtr.value) and checkValue(unit.value,float) != 'noneType':
					units.append((Year.objects.get(year=year.value),Qtr.objects.get(qtr=qtr.value),unit.value))
	return units

def GDRATMenu(model):
	newList = []
	for entry in model.objects.all():
		newList.append(str(entry.name))
	newList = sorted(newList,key=str.lower)
	return(newList)

def GetRoleProperties(role,GDRAT):	
	# ! WILL DEFAULT TO FIRST ROLE PROPERTY, GEO LEVEL SHOULD BE INPUTTED FIRST, LOWER LEVELS LAST [should maintain role properties at a consistent level]
	if RoleProperties.objects.filter(role=role,GDRAT__territory=GDRAT.territory):	
		roleproperties = RoleProperties.objects.filter(role=role,GDRAT__territory=GDRAT.territory)[0]
	elif RoleProperties.objects.filter(role=role,GDRAT__area=GDRAT.area):
		roleproperties = RoleProperties.objects.filter(role=role,GDRAT__area=GDRAT.area)[0]
	elif RoleProperties.objects.filter(role=role,GDRAT__region=GDRAT.region):
		roleproperties = RoleProperties.objects.filter(role=role,GDRAT__region=GDRAT.region)[0]
	elif RoleProperties.objects.filter(role=role,GDRAT__division=GDRAT.division):
		roleproperties = RoleProperties.objects.filter(role=role,GDRAT__division=GDRAT.division)[0]
	elif RoleProperties.objects.filter(role=role,GDRAT__geo=GDRAT.geo):
		roleproperties = RoleProperties.objects.filter(role=role,GDRAT__geo=GDRAT.geo)[0]
	else:
		roleproperties = RoleProperties.objects.get(pk=1)
	return roleproperties

def GetHeadcountGDRAT(role,GDRAT):	
	# ! WILL DEFAULT TO FIRST ROLE PROPERTY, GEO LEVEL SHOULD BE INPUTTED FIRST, LOWER LEVELS LAST [should maintain role properties at a consistent level]
	if HeadcountBIS.objects.filter(role=role,GDRAT__territory=GDRAT.territory):	
		headcountGDRAT = HeadcountBIS.objects.filter(role=role,GDRAT__territory=GDRAT.territory)[0]
		newGDRAT = headcountGDRAT.GDRAT
	elif HeadcountBIS.objects.filter(role=role,GDRAT__area=GDRAT.area):
		headcountGDRAT = HeadcountBIS.objects.filter(role=role,GDRAT__area=GDRAT.area)[0]
		newGDRAT = headcountGDRAT.GDRAT
	elif HeadcountBIS.objects.filter(role=role,GDRAT__region=GDRAT.region):
		headcountGDRAT = HeadcountBIS.objects.filter(role=role,GDRAT__region=GDRAT.region)[0]
		newGDRAT = headcountGDRAT.GDRAT
	elif HeadcountBIS.objects.filter(role=role,GDRAT__division=GDRAT.division):
		headcountGDRAT = HeadcountBIS.objects.filter(role=role,GDRAT__division=GDRAT.division)[0]
		newGDRAT = headcountGDRAT.GDRAT
	elif HeadcountBIS.objects.filter(role=role,GDRAT__geo=GDRAT.geo):
		headcountGDRAT = HeadcountBIS.objects.filter(role=role,GDRAT__geo=GDRAT.geo)[0]
		newGDRAT = headcountGDRAT.GDRAT
	else:
		newGDRAT = GDRAT
	return newGDRAT		
		
def HeadcountRequirementsUpdate(Model,role,GDRAT,year,qtr,fte):
	if not Model.objects.filter(role=role,GDRAT=GDRAT,year=year,qtr=qtr):
		newEntry = Model(role=role,GDRAT=GDRAT,year=year,qtr=qtr)
	else:
		newEntry =  Model.objects.get(role=role,GDRAT=GDRAT,year=year,qtr=qtr)
	newEntry.fte += fte
	newEntry.save()

def GetGDRAT(mapping):	
	if Territory.objects.filter(name=mapping):
		gdrats = GDRAT.objects.filter(territory=Territory.objects.get(name=mapping))
		level = 'Territory'
	elif Area.objects.filter(name=mapping):
		gdrats = GDRAT.objects.filter(area=Area.objects.get(name=mapping))
		level = 'Area'
	elif Region.objects.filter(name=mapping):
		gdrats = GDRAT.objects.filter(region=Region.objects.get(name=mapping))
		level = 'Region'
	elif Division.objects.filter(name=mapping):
		gdrats = GDRAT.objects.filter(division=Division.objects.get(name=mapping))
		level = 'Division'
	elif Geo.objects.filter(name=mapping):
		gdrats = GDRAT.objects.filter(geo=Geo.objects.get(name=mapping))
		level = 'Geography'
	else:
		gdrats = GDRAT.objects.all()
		level = 'Global'
	return(gdrats,level)
	
def checkGDRAT(list,model):
	if list[4] in Territory.objects.all():
		gdrat = model.objects.filter(territory=list[4])[0]
		gdrats = GetGDRAT(list[4])[0]
	elif list[3] in Area.objects.all():
		gdrat = model.objects.filter(area=list[3])[0]
		gdrats = GetGDRAT(list[3])[0]
	elif list[2] in Region.objects.all():
		gdrat = model.objects.filter(region=list[2])[0]
		gdrats = GetGDRAT(list[2])[0]
	elif list[1] in Division.objects.all():
		gdrat = model.objects.filter(division=list[1])[0]
		gdrats = GetGDRAT(list[1])[0]
	elif list[0] in Geo.objects.all():
		gdrat = model.objects.filter(geo=list[0])[0]
		gdrats = GetGDRAT(list[0])[0]
	else:
		gdrat = None
		gdrats = []
	return (gdrat, gdrats)

def Bucket(Model,gdrat,ModelUpdate):
	for entry in Model.objects.filter(GDRAT=gdrat):
		ModelUpdate(entry)
		
# ensure model instances are presented in alphabetical order
def ModelOrder(Model):	
	fieldsOrdered = []
	for instance in Model.objects.all():
		fieldsOrdered.append(instance.name)
	return sorted(fieldsOrdered)
	
# ensure years are presented in chronological order
def YearOrder(str):	
	yearsOrdered = []
	for year in Year.objects.all():
		yearsOrdered.append(year.year)
	return sorted(yearsOrdered)
	
# ensure qtrs are presented in chronological order
def QtrOrder(str):	
	qtrsOrdered = []
	for qtr in Qtr.objects.all():
		qtrsOrdered.append(qtr.qtr)
	return sorted(qtrsOrdered)