# import global modules
import sys
sys.path.append('globalResources')
from importModules import *


def MRROnContract(entry):
	mrr = entry.USD
	return mrr

def PlatformFrcst(entry):
	units = entry.units
	return units

def ServMRRFrcst(entry):
	units = entry.units
	ARPU = GSSProductProperties.objects.get(product=entry.product).ARPU
	mrr = units*ARPU
	return mrr

def ServNRRFrcst(entry):
	nrr = entry.USD
	return nrr	

def HeadcountFrcst(entry):
	headcount = entry.fte
	return headcount
	
	
### ALL PURPOSE YEAR/QTR VIEW FUNCTION ###

def TableView(request,prod,mapping,*args):
	
	ProductDict = {'Contract MRR':GSSProduct,'Platform':PlatformProduct,'Services MRR':GSSProduct,'Services NRR':TimeAndMaterials,'run':Role,'runReqs':Role,'runGap':Role,'headcount':Role}
	ModelDict = {'Contract MRR':MRRContract,'Platform':PlatformProductForecast,'Services MRR':GSSProductForecast,'Services NRR':TimeAndMaterialsForecast,'run':HeadcountRequirements,'runReqs':HeadcountAdjustments,'runGap':HeadcountAdjustments,'headcount':HeadcountBIS}
	FieldDict = {'Contract MRR':MRROnContract,'Platform':PlatformFrcst,'Services MRR':ServMRRFrcst,'Services NRR':ServNRRFrcst,'run':HeadcountFrcst,'runReqs':HeadcountFrcst,'runGap':HeadcountFrcst,'headcount':HeadcountFrcst}
	TypeDict = {'Contract MRR':'TypeProduct','Platform':'TypeProduct','Services MRR':'TypeProduct','Services NRR':'TypeProduct','run':'TypeRole','runReqs':'TypeRole','runGap':'TypeRole','headcount':'TypeRole'}
	currency = ['Contract MRR','Services MRR','Services NRR']
	TemplateDict = {'Contract MRR':'ModelApp/forecast.html','Platform':'ModelApp/forecast.html','Services MRR':'ModelApp/forecast.html','Services NRR':'ModelApp/forecast.html','run':'ModelApp/run.html','runReqs':'ModelApp/runReqs.html','runGap':'ModelApp/runReqs.html','headcount':'ModelApp/forecast.html'}
	HeadcountDict = {'Contract MRR':'','Platform':'','Services MRR':'','Services NRR':'','run':'Headcount Requirements','runReqs':'Headcount Deployment','runGap':'Headcount Comparison','headcount':''}
	
	Product = ProductDict[prod]
	Model = ModelDict[prod]
	field = FieldDict[prod]
	headcount = HeadcountDict[prod]
	
	if args:
		tablestakes = args[0]
		contracted = args[1]
		forecast = args[2]
	else:
		tablestakes = ''
		contracted = ''
		forecast = ''
	
	locale.setlocale(locale.LC_ALL,'')
	
	gdrats = GetGDRAT(mapping)[0]
	level = GetGDRAT(mapping)[1]
	
	forecasts = OrderedDict([])
	totals = OrderedDict([])
	
	yearsOrdered = []
	qtrsOrdered = []

	# ensure products/roles are presented in alphabetical order
	productsOrdered = ModelOrder(Product)
	
	# ensure years are presented in chronological order
	yearsOrdered = YearOrder(str)
		
	# ensure qtrs are presented in chronological order
	qtrsOrdered = QtrOrder(str)
		
	for productName in productsOrdered:
		product = Product.objects.get(name=productName)
		years = OrderedDict([])
		for yearNum in yearsOrdered:
			year = Year.objects.get(year=yearNum)
			qtrs = OrderedDict([])
			for qtrNum in qtrsOrdered:
				qtr = Qtr.objects.get(qtr=qtrNum)
				qtrs[qtr] = 0.0
				for gdrat in gdrats:
					if gdrat in GDRAT.objects.all():
						if TypeDict[prod] == 'TypeProduct':
							if Model.objects.filter(year=year,qtr=qtr,product=product,GDRAT=gdrat):
								entry = Model.objects.get(year=year,qtr=qtr,product=product,GDRAT=gdrat)
								qtrs[qtr] += field(entry)
						elif TypeDict[prod] == 'TypeRole':	
							if Model.objects.filter(year=year,qtr=qtr,role=product,GDRAT=gdrat):
								entry = Model.objects.get(year=year,qtr=qtr,role=product,GDRAT=gdrat)
								qtrs[qtr] += field(entry)
				qtrs[qtr] = round(qtrs[qtr])
				if prod in currency:
					qtrs[qtr] = locale.currency(qtrs[qtr],grouping=True)
			years[year] = qtrs
		forecasts[product] = years							

	for yearNum in yearsOrdered:
		year = Year.objects.get(year=yearNum)
		totalQtrs = OrderedDict([])
		for qtrNum in qtrsOrdered:
			qtr = Qtr.objects.get(qtr=qtrNum)
			totalQtrs[qtr] = 0.0
			for gdrat in gdrats:
				if gdrat in GDRAT.objects.all():
					for product in Product.objects.all():
						if TypeDict[prod] == 'TypeProduct':	
							if Model.objects.filter(year=year,qtr=qtr,product=product,GDRAT=gdrat):
								entry = Model.objects.get(year=year,qtr=qtr,product=product,GDRAT=gdrat)
								totalQtrs[qtr] += field(entry)
						elif TypeDict[prod] == 'TypeRole':	
							if Model.objects.filter(year=year,qtr=qtr,role=product,GDRAT=gdrat):
								entry = Model.objects.get(year=year,qtr=qtr,role=product,GDRAT=gdrat)
								totalQtrs[qtr] += field(entry)
			totalQtrs[qtr] = round(totalQtrs[qtr])
			if prod in currency:
				totalQtrs[qtr] = locale.currency(totalQtrs[qtr],grouping=True)
		totals[year] = totalQtrs
		
	geos = GDRATMenu(Geo)
	divisions = GDRATMenu(Division)
	regions = GDRATMenu(Region)
	areas = GDRATMenu(Area)
	territories = GDRATMenu(Territory)
	
	return render_to_response(TemplateDict[prod],{'product':prod,'years':years,'forecasts':forecasts,'totals':totals,'geos':geos,'divisions':divisions,'regions':regions,'areas':areas,'territories':territories,'level':level,'mapping':mapping,'tablestakes':tablestakes,'contracted':contracted,'forecast':forecast,'headcount':headcount},RequestContext(request))		