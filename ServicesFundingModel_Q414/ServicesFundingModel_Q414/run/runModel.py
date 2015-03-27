# import global modules
import sys
sys.path.append('globalResources')
from importModules import *

# ! SA AT AMERICAS LEVEL COULD GET PUBLIC SECTOR ROLE PROPERTIES
# ! SHOULD PRINT TEMPLATES FOR FORECAST SO DONT HAVE GDRAT ISSUES (ON FRCST)
# ! COULD MOVE TO RAM (INSTEAD OF WRITING TO DB) TO IMPROVE PERFORMANCE

def MRRContractUpdate(MRR):
	
	product = MRR.product
	GDRAT = MRR.GDRAT
	USD = MRR.USD
	baseyear = MRR.year
	baseqtr = MRR.qtr
	ESR = GSSProductProperties.objects.get(product=product).ESR
	for workingvalue in GSSProductWorkingValue.objects.filter(product=product):
		role = workingvalue.role
		pct = workingvalue.pct
		roleproperties = GetRoleProperties(role,GDRAT)
		BUR = roleproperties.BURinRegion*roleproperties.pctinRegion + roleproperties.BUREmerging*roleproperties.pctEmerging
		fte = (USD/ESR*pct)/(BUR*173.33)
		for qtr in Qtr.objects.filter(qtr__gte=baseqtr.qtr):
			HeadcountRequirementsUpdate(HeadcountRequirements,role,GDRAT,baseyear,qtr,fte)
		for year in Year.objects.filter(year__gt=baseyear.year):
			for qtr in Qtr.objects.all():
				HeadcountRequirementsUpdate(HeadcountRequirements,role,GDRAT,year,qtr,fte)
					
def PlatformProductFrcstUpdate(unit):
	
	#! NEED TO BUILD TIME TO INTEGRATE FUNCTION	
	
	product = unit.product
	GDRAT = unit.GDRAT
	units = unit.units
	baseyear = unit.year
	baseqtr = unit.qtr
	properties = PlatformProductProperties.objects.get(product=product)
	integration = properties.HoursStdImplementation*properties.pctStd + properties.HoursMgdImplementation*properties.pctMgd
	timetointegrate = properties.TimeToIntegrate
	for workingvalue in PlatformProductWorkingValue.objects.filter(product=product):
		role = workingvalue.role
		pct = workingvalue.pct
		roleproperties = GetRoleProperties(role,GDRAT)	
		BUR = roleproperties.BURinRegion*roleproperties.pctinRegion + roleproperties.BUREmerging*roleproperties.pctEmerging
		fte = (integration*units*pct)/(BUR*520)	
		HeadcountRequirementsUpdate(HeadcountRequirements,role,GDRAT,baseyear,baseqtr,fte)
					
def GSSMRRFrcstUpdate(MRR):
	
	#! NEED TO BUILD IN INTEGRATION DELAY FUNCTION
	
	product = MRR.product
	GDRAT = MRR.GDRAT
	units = MRR.units
	baseyear = MRR.year
	baseqtr = MRR.qtr
	ESR = GSSProductProperties.objects.get(product=product).ESR
	ARPU = GSSProductProperties.objects.get(product=product).ARPU
	USD = units*ARPU
	for workingvalue in GSSProductWorkingValue.objects.filter(product=product):
		role = workingvalue.role
		pct = workingvalue.pct
		roleproperties = GetRoleProperties(role,GDRAT)
		BUR = roleproperties.BURinRegion*roleproperties.pctinRegion + roleproperties.BUREmerging*roleproperties.pctEmerging
		fte = (USD/ESR*pct)/(BUR*173.33)	
		# place holder for integration delay
		HeadcountRequirementsUpdate(HeadcountRequirements,role,GDRAT,baseyear,baseqtr,fte/3)
		for qtr in Qtr.objects.filter(qtr__gt=baseqtr.qtr):
			HeadcountRequirementsUpdate(HeadcountRequirements,role,GDRAT,baseyear,qtr,fte)
		for year in Year.objects.filter(year__gt=baseyear.year):
			for qtr in Qtr.objects.all():
				HeadcountRequirementsUpdate(HeadcountRequirements,role,GDRAT,year,qtr,fte)
					
def GSSNRRFrcstUpdate(NRR):
	
	product = NRR.product
	GDRAT = NRR.GDRAT
	USD = NRR.USD
	baseyear = NRR.year
	baseqtr = NRR.qtr
	ESR = TimeAndMaterialsProperties.objects.get(product=product).ESR
	for workingvalue in TimeAndMaterialsWorkingValue.objects.filter(product=product):
		role = workingvalue.role
		pct = workingvalue.pct
		roleproperties = GetRoleProperties(role,GDRAT)
		BUR = roleproperties.BURinRegion*roleproperties.pctinRegion + roleproperties.BUREmerging*roleproperties.pctEmerging
		fte = (USD/ESR*pct)/(BUR*520)	
		HeadcountRequirementsUpdate(HeadcountRequirements,role,GDRAT,baseyear,baseqtr,fte)
		
def HeadcountGap(gdrats):
	
	supply = {}
	demand = {}
	reqs = {}
	
	for gdrat in gdrats:	
		for role in Role.objects.all():
			newGDRAT = GetHeadcountGDRAT(role,gdrat)
			
			for headcountBIS in HeadcountBIS.objects.filter(role=role,GDRAT=newGDRAT):
				supply[headcountBIS.role,headcountBIS.GDRAT,headcountBIS.year,headcountBIS.qtr] = headcountBIS.fte
				
			for headcount in HeadcountRequirements.objects.filter(role=role,GDRAT=gdrat):
				if (headcount.role,newGDRAT,headcount.year,headcount.qtr) in demand:
					demand[headcount.role,newGDRAT,headcount.year,headcount.qtr] += headcount.fte
				else:
					demand[headcount.role,newGDRAT,headcount.year,headcount.qtr] = headcount.fte
		
	for entry in demand:
		if entry in supply:
			reqs[entry] = round(demand[entry] - supply[entry])
		else:
			reqs[entry] = round(demand[entry])
			
	for entry in supply:
		if entry not in demand:
			reqs[entry] = supply[entry]*-1
	
	for req in reqs:
		HeadcountRequirementsUpdate(HeadcountAdjustments,req[0],req[1],req[2],req[3],reqs[req])	
	
def HiringSchedule(gdrats):

	# ensure years are presented in chronological order
	yearsOrdered = YearOrder(str)
		
	# ensure qtrs are presented in chronological order
	qtrsOrdered = QtrOrder(str)

	supply = {}
	demand = {}
	reqs = {}
	
	for gdrat in gdrats:	
		for role in Role.objects.all():
			newGDRAT = GetHeadcountGDRAT(role,gdrat)
			
			for headcountBIS in HeadcountBIS.objects.filter(role=role,GDRAT=newGDRAT):
				supply[headcountBIS.role,headcountBIS.GDRAT,headcountBIS.year,headcountBIS.qtr] = headcountBIS.fte
				
			for headcount in HeadcountRequirements.objects.filter(role=role,GDRAT=gdrat):
				if (headcount.role,newGDRAT,headcount.year,headcount.qtr) in demand:
					demand[headcount.role,newGDRAT,headcount.year,headcount.qtr] += headcount.fte
				else:
					demand[headcount.role,newGDRAT,headcount.year,headcount.qtr] = headcount.fte
		
	# create req requirements
	for entry in demand:
		if entry in supply:
			reqs[entry] = max(round(demand[entry] - supply[entry]),0)
		else:
			reqs[entry] = round(demand[entry])
			
	# create req deployment schedule (cumulative)
	year_qtr = OrderedDict([])
	for yearNum in yearsOrdered:
		for qtrNum in qtrsOrdered:
			year_qtr[(yearNum,qtrNum)] = yearNum**2+qtrNum

	for year_qtrNum in year_qtr:
		yearNum = year_qtrNum[0]
		qtrNum = year_qtrNum[1]
		year = Year.objects.get(year=yearNum)
		qtr = Qtr.objects.get(qtr=qtrNum)
		for role in Role.objects.all():
			for gdrat in gdrats:
				for req in reqs:	
					if req[0] == role and req[1] == gdrat and (req[2].year**2+req[3].qtr) < year_qtr[year_qtrNum]:
						if (role,gdrat,year,qtr) in reqs:
							reqs[(role,gdrat,year,qtr)] = max(reqs[(role,gdrat,year,qtr)] - reqs[req],0)
	
	for req in reqs:
		HeadcountRequirementsUpdate(HeadcountAdjustments,req[0],req[1],req[2],req[3],reqs[req])	
					
HeadcountDict = {'runReqs':HiringSchedule,'runGap':HeadcountGap}	