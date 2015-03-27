# import global modules
import sys
sys.path.append('globalResources')
from importModules import *

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

# file path
file_abs_path = os.path.join(os.path.dirname(__file__),'C:\Users\jarchbol\Desktop\ServicesFundingModel_Q414\media\documents')
	
def GDRATUpdate(workbook):		
	
	# uncomment to delete existing GDRAT mapping
	
	GDRATmodels = [Geo, Division, Region, Area, Territory, Area]
	'''
	for model in GDRATmodels:
		model.objects.all().delete()
	'''
	source_wb = xlrd.open_workbook(file_abs_path+'/'+workbook)
	
	sh_1 = source_wb.sheet_by_index(0)

	headers = ['Geo','Division','Region','Area','Territory']	
	if checkWBHeaders(sh_1,headers,0):

		# data collection
		geos = []
		divisions = []
		regions = []
		areas = []
		territories = []
		gdrats = []

		for rownum in range(sh_1.nrows):
			geo = sh_1.cell(rownum,0)
			division = sh_1.cell(rownum,1)
			region = sh_1.cell(rownum,2)
			area = sh_1.cell(rownum,3)
			territory = sh_1.cell(rownum,4)
			gdrat = (geo.value, division.value, region.value, area.value, territory.value)
			geos.append(geo.value)
			divisions.append(division.value)
			regions.append(region.value)
			areas.append(area.value)
			territories.append(territory.value)
			gdrats.append(gdrat)
	
		Mapping = {Geo:geos, Division:divisions, Region:regions, Area:areas, Territory:territories}

		for key in Mapping:
			print '\n-----------------------------------\n'
			print key
			print '\n-----------------------------------\n'
			for entry in Mapping[key]:
				addNew(key,entry)

		for gdrat in gdrats:
			geo = Geo.objects.get(name__iexact=gdrat[0])
			division = Division.objects.get(name__iexact=gdrat[1])
			region = Region.objects.get(name__iexact=gdrat[2])
			area = Area.objects.get(name__iexact=gdrat[3])
			territory = Territory.objects.get(name__iexact=gdrat[4])
			if not GDRAT.objects.filter(territory=territory):
				newEntry = GDRAT(geo=geo, division=division, region=region, area=area, territory=territory)
				newEntry.save()
				print 'saved:',newEntry,'in',GDRAT
			else:
				print territory,'GDRAT already exists'
		
		return True
	else:
		return False
	
def GSSRolesUpdate(workbook):		
	
	# uncomment to delete existing GSS Roles
	# Role.objects.all().delete()

	source_wb = xlrd.open_workbook(file_abs_path+'/'+workbook)
	sh_1 = source_wb.sheet_by_index(0)

	# data collection
	roles = {}
	
	headers = ['Role','BUR In Region','BUR Emerging','% in Region','% Emerging','Time to Productivity','Geo','Division','Region','Area','Territory']
	if checkWBHeaders(sh_1,headers,0):
	
		for rownum in range(sh_1.nrows):
			roleName = sh_1.cell(rownum,0)
			BURinRegion = sh_1.cell(rownum,1)
			BUREmerging = sh_1.cell(rownum,2)
			pctinRegion = sh_1.cell(rownum,3)
			pctEmerging = sh_1.cell(rownum,4)
			TimeToProductivity = sh_1.cell(rownum,5)
			geo = checkModel(Geo,sh_1.cell(rownum,6).value)
			division = checkModel(Division,sh_1.cell(rownum,7).value)
			region = checkModel(Region,sh_1.cell(rownum,8).value)
			area = checkModel(Area,sh_1.cell(rownum,9).value)
			territory = checkModel(Territory,sh_1.cell(rownum,10).value)
			gdrat = (geo,division,region,area,territory)
			if checkValue(BURinRegion.value,float) != 'noneType' and checkValue(BUREmerging.value,float) != 'noneType' and checkValue(pctinRegion.value,float) != 'noneType' and checkValue(pctEmerging.value,float) != 'noneType' and checkValue(TimeToProductivity.value,int) != 'noneType':
				roles[(roleName.value,gdrat)] = (BURinRegion.value,BUREmerging.value,pctinRegion.value,pctEmerging.value,TimeToProductivity.value)

		# update roles
		for roleName in roles:
			addNew(Role,roleName[0])
		
		# update role properties
		for roleName in roles:
			role = Role.objects.get(name__iexact=roleName[0])
			gdrat = checkGDRAT(roleName[1],GDRAT)[0]
			if gdrat in GDRAT.objects.all():
				if RoleProperties.objects.filter(role=role,GDRAT=gdrat):
					newEntry = RoleProperties.objects.get(role=role,GDRAT=gdrat)
				else:
					newEntry = RoleProperties(role=role,GDRAT=gdrat)
				# add individual role properties
				newEntry.BURinRegion=float(roles[roleName][0])
				newEntry.BUREmerging=float(roles[roleName][1])
				newEntry.pctinRegion=float(roles[roleName][2])
				newEntry.pctEmerging=float(roles[roleName][3])
				newEntry.TimeToProductivity=int(roles[roleName][4])
				newEntry.save()
				print 'saved:',newEntry,'in',RoleProperties
		return True
	else:
		return False

def HeadcountBISUpdate(workbook):		
	
	# uncomment to delete existing Headcount BIS
	HeadcountBIS.objects.all().delete()

	source_wb = xlrd.open_workbook(file_abs_path+'/'+workbook)
	sh_1 = source_wb.sheet_by_index(0)

	# data collection
	roles = {}
	
	headers = ['Role','Geo','Division','Region','Area','Territory']
	if checkWBHeaders(sh_1,headers,0):
		for rownum in range(sh_1.nrows):
			roleName = sh_1.cell(rownum,0)
			geo = checkModel(Geo,sh_1.cell(rownum,1).value)
			division = checkModel(Division,sh_1.cell(rownum,2).value)
			region = checkModel(Region,sh_1.cell(rownum,3).value)
			area = checkModel(Area,sh_1.cell(rownum,4).value)
			territory = checkModel(Territory,sh_1.cell(rownum,5).value)
			gdrat = (geo,division,region,area,territory)
			if Role.objects.filter(name__iexact=roleName.value):
				if (roleName.value,gdrat) in roles:
					roles[(roleName.value,gdrat)] += 1
				else:
					roles[(roleName.value,gdrat)] = 1
			
		for year in Year.objects.all():
			for qtr in Qtr.objects.all():
				for roleName in roles:
					role = Role.objects.get(name__iexact=roleName[0])
					gdrat = checkGDRAT(roleName[1],GDRAT)[0]
					HeadcountRequirementsUpdate(HeadcountBIS,role,gdrat,year,qtr,roles[roleName])
		return True
	else:
		return False

def HeadcountADJUpdate(workbook):		
	
	# uncomment to delete existing Headcount BIS
	# HeadcountBIS.objects.all().delete()

	source_wb = xlrd.open_workbook(file_abs_path+'/'+workbook)
	sh_1 = source_wb.sheet_by_index(0)

	# data collection
	frcst = {}
	
	headers = ['Role','Geo','Division','Region','Area','Territory']
	if checkWBHeaders(sh_1,headers,1):
		for rownum in range(sh_1.nrows):
			geo = checkModel(Geo,sh_1.cell(rownum,0).value)
			division = checkModel(Division,sh_1.cell(rownum,1).value)
			region = checkModel(Region,sh_1.cell(rownum,2).value)
			area = checkModel(Area,sh_1.cell(rownum,3).value)
			territory = checkModel(Territory,sh_1.cell(rownum,4).value)
			gdrat = (geo,division,region,area,territory)
			roleName = sh_1.cell(rownum,5)
			if Role.objects.filter(name__iexact=roleName.value):
				frcst[(Role.objects.get(name__iexact=roleName.value),gdrat)] = unitFrcst(rownum,6,sh_1)
		
		# update GSS Headcount Frcst
		for role in frcst:
			gdrat = checkGDRAT(role[1],GDRAT)[0]
			units = frcst[role]
			if gdrat in GDRAT.objects.all():
				for unit in units:
					for qtr in Qtr.objects.filter(qtr__gte=unit[1].qtr):
						HeadcountRequirementsUpdate(HeadcountBIS,role[0],gdrat,unit[0],qtr,unit[2])
					for year in Year.objects.filter(year__gt=unit[0].year):
						for qtr in Qtr.objects.all():
							HeadcountRequirementsUpdate(HeadcountBIS,role[0],gdrat,year,qtr,unit[2])
		return True
	else:
		return False
				
def PlatformProductsUpdate(workbook):		
	
	# uncomment to delete existing Platform Products
	# PlatformProduct.objects.all().delete()

	source_wb = xlrd.open_workbook(file_abs_path+'/'+workbook)
	sh_1 = source_wb.sheet_by_index(0)

	# data collection
	products = {}
	
	headers = ['Platform Product','Hours Std Integration','Hours Mgd Integration','% Std','% Mdg','Time to Integrate (days)','Role','% Allocation','Role','% Allocation','CONTINUE ROLE AS NEEDED','CONTINUE ALLOCATION AS NEEDED']
	if checkWBHeaders(sh_1,headers,0):
		for rownum in range(sh_1.nrows):
			productName = sh_1.cell(rownum,0)
			HoursStdImplementation = sh_1.cell(rownum,1)
			HoursMgdImplementation = sh_1.cell(rownum,2)
			pctStd = sh_1.cell(rownum,3)
			pctMdg = sh_1.cell(rownum,4)
			TimeToIntegrate = sh_1.cell(rownum,5)
			if checkValue(HoursStdImplementation.value,int) != 'noneType' and checkValue(HoursMgdImplementation.value,int) != 'noneType' and checkValue(pctStd.value,float) != 'noneType' and checkValue(pctMdg.value,float) != 'noneType' and checkValue(TimeToIntegrate.value,int) != 'noneType':
				products[productName.value] = [HoursStdImplementation.value,HoursMgdImplementation.value,pctStd.value,pctMdg.value,TimeToIntegrate.value,roleAllocation(rownum,6,sh_1)]

		# update Platform Products
		for productName in products:
			addNew(PlatformProduct,productName)
		
		# update Platform Product properties
		for productName in products:
			product = PlatformProduct.objects.get(name__iexact=productName)
			if PlatformProductProperties.objects.filter(product=product):
				newEntry = PlatformProductProperties.objects.get(product=product)
			else:
				newEntry = PlatformProductProperties(product=product)
			# add individual product properties
			newEntry.HoursStdImplementation=int(products[productName][0])
			newEntry.HoursMgdImplementation=int(products[productName][1])
			newEntry.pctStd=float(products[productName][2])
			newEntry.pctMgd=float(products[productName][3])
			newEntry.TimeToIntegrate=int(products[productName][4])
			newEntry.save()
			print 'saved:',newEntry,'in',PlatformProductProperties
		
			# update Platform Product Working Value
			workingValue(products,productName,product,5,PlatformProductWorkingValue)
		return True
	else:
		return False
			
def GSSMRRProductsUpdate(workbook):		
	
	# uncomment to delete existing GSS MRR Products
	# GSSProduct.objects.all().delete()

	source_wb = xlrd.open_workbook(file_abs_path+'/'+workbook)
	sh_1 = source_wb.sheet_by_index(0)

	# data collection
	products = {}
	
	headers = ['GSS-Product','ARPU (USD)','ESR (USD)','Integration Delay (days)','Role','% Allocation','Role','% Allocation','Role','% Allocation','CONTINUE ROLE AS NEEDED','CONTINUE ALLOCATION AS NEEDED']
	if checkWBHeaders(sh_1,headers,0):
		for rownum in range(sh_1.nrows):
			productName = sh_1.cell(rownum,0)
			ARPU = sh_1.cell(rownum,1)
			ESR = sh_1.cell(rownum,2)
			IntegrationDelay = sh_1.cell(rownum,3)
			if checkValue(ARPU.value,int) != 'noneType' and checkValue(ESR.value,int) != 'noneType' and checkValue(IntegrationDelay.value,int) != 'noneType':
				products[productName.value] = [ARPU.value,ESR.value,IntegrationDelay.value,roleAllocation(rownum,4,sh_1)]

		# update GSS MRR Products
		for productName in products:
			addNew(GSSProduct,productName)
		
		# update GSS MRR Product properties
		for productName in products:
			product = GSSProduct.objects.get(name__iexact=productName)
			if GSSProductProperties.objects.filter(product=product):
				newEntry = GSSProductProperties.objects.get(product=product)
			else:
				newEntry = GSSProductProperties(product=product)
			# add individual product properties
			newEntry.ARPU=int(products[productName][0])
			newEntry.ESR=int(products[productName][1])
			newEntry.IntegrationDelay=int(products[productName][2])
			newEntry.save()
			print 'saved:',newEntry,'in',GSSProductProperties
		
			# update GSS MRR Working Value
			workingValue(products,productName,product,3,GSSProductWorkingValue)
		return True
	else:
		return False

def GSSNRRProductsUpdate(workbook):		
	
	# uncomment to delete existing GSS NRR Products
	# TimeAndMAterials.objects.all().delete()

	source_wb = xlrd.open_workbook(file_abs_path+'/'+workbook)
	sh_1 = source_wb.sheet_by_index(0)

	# data collection
	products = {}
	
	headers = ['NRR Product','ESR (USD)','Role','% Allocation','Role','% Allocation','CONTINUE ROLE AS NEEDED','CONTINUE ALLOCATION AS NEEDED']
	if checkWBHeaders(sh_1,headers,0):
		for rownum in range(sh_1.nrows):
			productName = sh_1.cell(rownum,0)
			ESR = sh_1.cell(rownum,1)
			if checkValue(ESR.value,int) != 'noneType':
				products[productName.value] = [ESR.value,roleAllocation(rownum,2,sh_1)]

		# update GSS NRR Products
		for productName in products:
			addNew(TimeAndMaterials,productName)
		
		# update GSS NRR Product properties
		for productName in products:
			product = TimeAndMaterials.objects.get(name__iexact=productName)
			if TimeAndMaterialsProperties.objects.filter(product=product):
				newEntry = TimeAndMaterialsProperties.objects.get(product=product)
			else:
				newEntry = TimeAndMaterialsProperties(product=product)
			# add individual product properties
			newEntry.ESR=int(products[productName][0])
			newEntry.save()
			print 'saved:',newEntry,'in',TimeAndMaterialsProperties
		
			# update GSS NRR Working Value
			workingValue(products,productName,product,1,TimeAndMaterialsWorkingValue)
		return True
	else:
		return False
			
def MRRContractUpdate(workbook):
	
	# delete existing MRRContract
	MRRContract.objects.all().delete()

	source_wb = xlrd.open_workbook(file_abs_path+'/'+workbook)
	sh_1 = source_wb.sheet_by_index(0)

	# data collection
	years = []
	qtrs = []
	
	headers = ['Account ID','Account Name','Marketing Product Name','MRR','GSS-Product','Geo','Division','Region','Area','Territory']
	if checkWBHeaders(sh_1,headers,0):
		for rownum in range(sh_1.nrows):
			USD = sh_1.cell(rownum,3)
			product = sh_1.cell(rownum,4)
			territory = checkModel(Territory,sh_1.cell(rownum,9).value)
			gdrat = GDRAT.objects.get(territory=territory)
			if checkValue(USD.value,float) != 'noneType' and GSSProduct.objects.filter(name__iexact=product.value):
				product = GSSProduct.objects.get(name__iexact=product.value)
				for year in Year.objects.all():
					years.append(year.year)
				for qtr in Qtr.objects.all():
					qtrs.append(qtr.qtr)
				baseYear = Year.objects.get(year=min(years))
				baseQtr = Qtr.objects.get(qtr=min(qtrs))
				if MRRContract.objects.filter(product=product,GDRAT=gdrat,year=baseYear,qtr=baseQtr):
					newEntry = MRRContract.objects.get(product=product,GDRAT=gdrat,year=baseYear,qtr=baseQtr)
				else:
					newEntry = MRRContract(product=product,GDRAT=gdrat,year=baseYear,qtr=baseQtr)
				newEntry.USD += USD.value
				newEntry.save()
				print 'saved:',newEntry.product,newEntry.GDRAT,newEntry.USD
		return True
	else:
		return False

def GSSMRRFrcst(workbook):		
	
	# uncomment to delete existing GSS Roles
	# GSSProductForecast.all().delete()

	source_wb = xlrd.open_workbook(file_abs_path+'/'+workbook)
	sh_1 = source_wb.sheet_by_index(0)

	# data collection
	frcst = {}
	gdrats = []
	
	headers = ['Geo','Division','Region','Area','Territory','GSS-Product']
	if checkWBHeaders(sh_1,headers,1):
		for rownum in range(sh_1.nrows):
			geo = checkModel(Geo,sh_1.cell(rownum,0).value)
			division = checkModel(Division,sh_1.cell(rownum,1).value)
			region = checkModel(Region,sh_1.cell(rownum,2).value)
			area = checkModel(Area,sh_1.cell(rownum,3).value)
			territory = checkModel(Territory,sh_1.cell(rownum,4).value)
			gdrat = (geo,division,region,area,territory)
			productName = sh_1.cell(rownum,5)
			if GSSProduct.objects.filter(name__iexact=productName.value):
				frcst[(GSSProduct.objects.get(name__iexact=productName.value),gdrat)] = unitFrcst(rownum,6,sh_1)
			for value in checkGDRAT(gdrat,GDRAT)[1]:
				if value not in gdrats:
					gdrats.append(value)
		
		# delete existing GSS Product Frcst (possibly change to only delete year being updated?)
		for value in gdrats:
			GSSProductForecast.objects.filter(GDRAT=value).delete()
		
		# update GSS Product Frcst
		for product in frcst:
			gdrat = checkGDRAT(product[1],GDRAT)[0]
			units = frcst[product]
			if gdrat in GDRAT.objects.all():
				for unit in units:
					if GSSProductForecast.objects.filter(product=product[0],GDRAT=gdrat,year=unit[0],qtr=unit[1]):
						newEntry = GSSProductForecast.objects.get(product=product[0],GDRAT=gdrat,year=unit[0],qtr=unit[1])
					else:
						newEntry = GSSProductForecast(product=product[0],GDRAT=gdrat,year=unit[0],qtr=unit[1])
					# add units
					newEntry.units=float(unit[2])
					newEntry.save()
					print 'saved:',newEntry.product,newEntry.units,newEntry.year,newEntry.qtr
		return True
	else:
		return False

def GSSNRRFrcst(workbook):		
	
	# uncomment to delete existing GSS Roles
	# TimeAndMaterialsForecast.all().delete()

	source_wb = xlrd.open_workbook(file_abs_path+'/'+workbook)
	sh_1 = source_wb.sheet_by_index(0)

	# data collection
	frcst = {}
	gdrats = []
	
	headers = ['Geo','Division','Region','Area','Territory','NRR Product']
	if checkWBHeaders(sh_1,headers,1):
		for rownum in range(sh_1.nrows):
			geo = checkModel(Geo,sh_1.cell(rownum,0).value)
			division = checkModel(Division,sh_1.cell(rownum,1).value)
			region = checkModel(Region,sh_1.cell(rownum,2).value)
			area = checkModel(Area,sh_1.cell(rownum,3).value)
			territory = checkModel(Territory,sh_1.cell(rownum,4).value)
			gdrat = (geo,division,region,area,territory)
			productName = sh_1.cell(rownum,5)
			if TimeAndMaterials.objects.filter(name__iexact=productName.value):
				frcst[(TimeAndMaterials.objects.get(name__iexact=productName.value),gdrat)] = unitFrcst(rownum,6,sh_1)
			for value in checkGDRAT(gdrat,GDRAT)[1]:
				if value not in gdrats:
					gdrats.append(value)
				
		# delete existing GSS NRR Frcst (possibly change to only delete year being updated?)
		for value in gdrats:
			TimeAndMaterialsForecast.objects.filter(GDRAT=value).delete()
		
		# update GSS NRR Frcst
		for product in frcst:
			gdrat = checkGDRAT(product[1],GDRAT)[0]
			units = frcst[product]
			if gdrat in GDRAT.objects.all():
				for unit in units:
					if TimeAndMaterialsForecast.objects.filter(product=product[0],GDRAT=gdrat,year=unit[0],qtr=unit[1]):
						newEntry = TimeAndMaterialsForecast.objects.get(product=product[0],GDRAT=gdrat,year=unit[0],qtr=unit[1])
					else:
						newEntry = TimeAndMaterialsForecast(product=product[0],GDRAT=gdrat,year=unit[0],qtr=unit[1])
					# add units
					newEntry.USD=float(unit[2])
					newEntry.save()
					print 'saved:',newEntry.product,newEntry.USD,newEntry.year,newEntry.qtr
		return True
	else:
		return False

def PlatformProductFrcst(workbook):		
	
	# uncomment to delete existing GSS Roles
	# PlatformProductForecast.all().delete()

	source_wb = xlrd.open_workbook(file_abs_path+'/'+workbook)
	sh_1 = source_wb.sheet_by_index(0)

	# data collection
	frcst = {}
	gdrats = []
	
	headers = ['Geo','Division','Region','Area','Territory','Platform Product']
	if checkWBHeaders(sh_1,headers,1):
		for rownum in range(sh_1.nrows):
			geo = checkModel(Geo,sh_1.cell(rownum,0).value)
			division = checkModel(Division,sh_1.cell(rownum,1).value)
			region = checkModel(Region,sh_1.cell(rownum,2).value)
			area = checkModel(Area,sh_1.cell(rownum,3).value)
			territory = checkModel(Territory,sh_1.cell(rownum,4).value)
			gdrat = (geo,division,region,area,territory)
			productName = sh_1.cell(rownum,5)
			if PlatformProduct.objects.filter(name__iexact=productName.value):
				frcst[(PlatformProduct.objects.get(name__iexact=productName.value),gdrat)] = unitFrcst(rownum,6,sh_1)
			for value in checkGDRAT(gdrat,GDRAT)[1]:
				if value not in gdrats:
					gdrats.append(value)
		
		# delete existing Platform Product Frcst (possibly change to only delete year being updated?)
		for value in gdrats:
			PlatformProductForecast.objects.filter(GDRAT=value).delete()	
		
		# update Platform Product Frcst
		for product in frcst:
			gdrat = checkGDRAT(product[1],GDRAT)[0]
			units = frcst[product]
			if gdrat in GDRAT.objects.all():
				for unit in units:
					if PlatformProductForecast.objects.filter(product=product[0],GDRAT=gdrat,year=unit[0],qtr=unit[1]):
						newEntry = PlatformProductForecast.objects.get(product=product[0],GDRAT=gdrat,year=unit[0],qtr=unit[1])
					else:
						newEntry = PlatformProductForecast(product=product[0],GDRAT=gdrat,year=unit[0],qtr=unit[1])
					# add units
					newEntry.units=float(unit[2])
					newEntry.save()
					print 'saved:',newEntry.product,newEntry.units,newEntry.year,newEntry.qtr
		return True
	else:
		return False
				
# parameter dictionary
setupDic = {'GDRAT':GDRATUpdate,'Function':GSSRolesUpdate,'HeadcountBIS':HeadcountBISUpdate,'HeadcountADJ':HeadcountADJUpdate,'Product':PlatformProductsUpdate,'ServicesMRR':GSSMRRProductsUpdate,'ServicesNRR':GSSNRRProductsUpdate,'MRRContract':MRRContractUpdate,'GSSMRRFrcst':GSSMRRFrcst,'GSSNRRFrcst':GSSNRRFrcst,'PlatformProductFrcst':PlatformProductFrcst}
# template instructions
instructions = {
'GDRAT':OrderedDict([('column A','Geography'),('column B','Division'),('column C','Region'),('column D','Area'),('column E','Territory')]),
'Function':OrderedDict([('column A','Role Name'),('column B','BUR in Region'),('column C','BUR Emerging'),('column D','% in Regiong'),('column E','% Emerging'),('column F','Time to Productivity'),('column G','Geography'),('column H','Division'),('column I','Region'),('column J','Area'),('column K','Territory')]),
'ServicesMRR':OrderedDict([('column A','Product Name'),('column B','ARPU'),('column C','ESR'),('column D','Integration Delay (days)'),('column E','Role'),('column F','% Role Allocation'),('column ##','repeat columns "E" & "F" as necessary')]),
'Product':OrderedDict([('column A','Product Mapping'),('column B','Hours Standard Integration'),('column C','Hours Managed Integration'),('column D','Standard %'),('column E','Managed 5'),('column F','Time to Integrate (days)'),('column G','Role'),('column H','% Allocation'),('column I','Role'),('column J','% Allocation')]),
'ServicesNRR':OrderedDict([('column A','Product Mapping'),('column B','ESR (USD)'),('column C','Role'),('column D','% Allocation'),('column E','Role'),('column F','% Allocation')]),
'MRRContract':OrderedDict([('column A','Account ID'),('column B','Account Name'),('column C','Marketing'),('column D','MRR'),('column E','Product MAPPING'),('column F','Geo'),('column G','Division'),('column H','Region'),('column I','Area'),('column J','Territory')]),
'PlatformProductFrcst':OrderedDict([('column A','Geo'),('column B','Division'),('column C','Region'),('column D','Area'),('column E','Territory'),('column F','List of Products'),('column G','Quarter 1'),('column H','Quarter 2'),('column I','Quarter 3'),('column J','Quarter 4')]),
'GSSMRRFrcst':OrderedDict([('column A','Geo'),('column B','Division'),('column C','Region'),('column D','Area'),('column E','Territory'),('column F','List of Products'),('column G','Quarter 1'),('column H','Quarter 2'),('column I','Quarter 3'),('column J','Quarter 4')]),
'GSSNRRFrcst':OrderedDict([('column A','Geo'),('column B','Division'),('column C','Region'),('column D','Area'),('column E','Territory'),('column F','List of Products'),('column G','Quarter 1'),('column H','Quarter 2'),('column I','Quarter 3'),('column J','Quarter 4')]),
}