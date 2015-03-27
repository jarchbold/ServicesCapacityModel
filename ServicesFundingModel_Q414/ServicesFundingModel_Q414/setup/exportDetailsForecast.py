# import global modules
import sys
sys.path.append('globalResources')
from importModules import *

from django.http import HttpResponse

# ! THESE FUNCTIONS ALL EXPORT DETAILS FOR PRODUCT FORECAST - PROBABLY SHOULD LOOK TO CONSOLIDATE TO ONE FUNCTION IN THE FUTURE

yearsOrdered = YearOrder(str)
qtrsOrdered = QtrOrder(str)

def MRRonContract(request,mapping):

	gdrats = GetGDRAT(mapping)[0]
	productsOrdered = ModelOrder(GSSProduct)
	
	# data aggregation
	MRR = OrderedDict([])
	
	for yearNum in yearsOrdered:
		year = Year.objects.get(year=yearNum)
		qtrs = OrderedDict([])
		for qtrNum in qtrsOrdered:
			qtr = Qtr.objects.get(qtr=qtrNum)
			products = OrderedDict([])
			for productName in productsOrdered:
				product = GSSProduct.objects.get(name=productName)
				products[product] = {}
				for gdrat in gdrats:
					products[product][gdrat] = 0.0
					if gdrat in GDRAT.objects.all():
						for forecast in MRRContract.objects.filter(year=year,qtr=qtr,product=product,GDRAT=gdrat):
							products[product][gdrat] += forecast.USD
				products[product][gdrat] = int(round(products[product][gdrat]))
			qtrs[qtr] = products
		MRR[year] = qtrs
		
	# set up workbook
	wb = xlwt.Workbook()
	sh_1 = wb.add_sheet('Sheet1', cell_overwrite_ok=True)
	sh_1.write(0,0,'Geo')
	sh_1.write(0,1,'Division')
	sh_1.write(0,2,'Region')
	sh_1.write(0,3,'Area')
	sh_1.write(0,4,'Territory')
	sh_1.write(0,5,'Product')
	y = 6
	for year in MRR:
		for qtr in MRR[year]:
			x = 1
			yearqtr = str(year.year)+'Q'+str(qtr.qtr)
			sh_1.write(0,y,yearqtr)
			for product in MRR[year][qtr]:
				for gdrat in MRR[year][qtr][product]:
					sh_1.write(x,0,gdrat.geo.name)
					sh_1.write(x,1,gdrat.division.name)
					sh_1.write(x,2,gdrat.region.name)
					sh_1.write(x,3,gdrat.area.name)
					sh_1.write(x,4,gdrat.territory.name)
					sh_1.write(x,5,product.name)
					sh_1.write(x,y,MRR[year][qtr][product][gdrat])
					x += 1
			y += 1
	
	# return extract
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=ContractMRR_'+mapping+'.xls'
	wb.save(response)
	return response

def PlatformProductFrcst(request,mapping):

	gdrats = GetGDRAT(mapping)[0]
	productsOrdered = ModelOrder(PlatformProduct)
	
	# data aggregation
	unit = OrderedDict([])
	
	for yearNum in yearsOrdered:
		year = Year.objects.get(year=yearNum)
		qtrs = OrderedDict([])
		for qtrNum in qtrsOrdered:
			qtr = Qtr.objects.get(qtr=qtrNum)
			products = OrderedDict([])
			for productName in productsOrdered:
				product = PlatformProduct.objects.get(name=productName)
				products[product] = {}
				for gdrat in gdrats:
					products[product][gdrat] = 0.0
					if gdrat in GDRAT.objects.all():
						for forecast in PlatformProductForecast.objects.filter(year=year,qtr=qtr,product=product,GDRAT=gdrat):
							products[product][gdrat] += forecast.units
				products[product][gdrat] = int(round(products[product][gdrat]))
			qtrs[qtr] = products
		unit[year] = qtrs
		
	# set up workbook
	wb = xlwt.Workbook()
	sh_1 = wb.add_sheet('Sheet1', cell_overwrite_ok=True)
	sh_1.write(0,0,'Geo')
	sh_1.write(0,1,'Division')
	sh_1.write(0,2,'Region')
	sh_1.write(0,3,'Area')
	sh_1.write(0,4,'Territory')
	sh_1.write(0,5,'Product')
	y = 6
	for year in unit:
		for qtr in unit[year]:
			x = 1
			yearqtr = str(year.year)+'Q'+str(qtr.qtr)
			sh_1.write(0,y,yearqtr)
			for product in unit[year][qtr]:
				for gdrat in unit[year][qtr][product]:
					sh_1.write(x,0,gdrat.geo.name)
					sh_1.write(x,1,gdrat.division.name)
					sh_1.write(x,2,gdrat.region.name)
					sh_1.write(x,3,gdrat.area.name)
					sh_1.write(x,4,gdrat.territory.name)
					sh_1.write(x,5,product.name)
					sh_1.write(x,y,unit[year][qtr][product][gdrat])
					x += 1
			y += 1
	
	# return extract
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=PlatformFrcst_'+mapping+'.xls'
	wb.save(response)
	return response

def ServMRRFrcst(request,mapping):

	gdrats = GetGDRAT(mapping)[0]
	productsOrdered = ModelOrder(GSSProduct)
	
	# data aggregation
	MRR = OrderedDict([])

	for yearNum in yearsOrdered:
		year = Year.objects.get(year=yearNum)
		qtrs = OrderedDict([])
		for qtrNum in qtrsOrdered:
			qtr = Qtr.objects.get(qtr=qtrNum)
			products = OrderedDict([])
			for productName in productsOrdered:
				product = GSSProduct.objects.get(name=productName)
				products[product] = {}
				for gdrat in gdrats:
					products[product][gdrat] = 0.0
					if gdrat in GDRAT.objects.all():
						for forecast in GSSProductForecast.objects.filter(year=year,qtr=qtr,product=product,GDRAT=gdrat):
							ARPU = GSSProductProperties.objects.get(product=product).ARPU
							products[product][gdrat] += forecast.units*ARPU
				products[product][gdrat] = int(round(products[product][gdrat]))
			qtrs[qtr] = products
		MRR[year] = qtrs
		
	# set up workbook
	wb = xlwt.Workbook()
	sh_1 = wb.add_sheet('Sheet1', cell_overwrite_ok=True)
	sh_1.write(0,0,'Geo')
	sh_1.write(0,1,'Division')
	sh_1.write(0,2,'Region')
	sh_1.write(0,3,'Area')
	sh_1.write(0,4,'Territory')
	sh_1.write(0,5,'Product')
	y = 6
	for year in MRR:
		for qtr in MRR[year]:
			x = 1
			yearqtr = str(year.year)+'Q'+str(qtr.qtr)
			sh_1.write(0,y,yearqtr)
			for product in MRR[year][qtr]:
				for gdrat in MRR[year][qtr][product]:
					sh_1.write(x,0,gdrat.geo.name)
					sh_1.write(x,1,gdrat.division.name)
					sh_1.write(x,2,gdrat.region.name)
					sh_1.write(x,3,gdrat.area.name)
					sh_1.write(x,4,gdrat.territory.name)
					sh_1.write(x,5,product.name)
					sh_1.write(x,y,MRR[year][qtr][product][gdrat])
					x += 1
			y += 1
	
	# return extract
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=ServMRRFrcst_'+mapping+'.xls'
	wb.save(response)
	return response

def ServNRRFrcst(request,mapping):

	gdrats = GetGDRAT(mapping)[0]
	productsOrdered = ModelOrder(TimeAndMaterials)	
	
	# data aggregation
	NRR = OrderedDict([])
	
	for yearNum in yearsOrdered:
		year = Year.objects.get(year=yearNum)
		qtrs = OrderedDict([])
		for qtrNum in qtrsOrdered:
			qtr = Qtr.objects.get(qtr=qtrNum)
			products = OrderedDict([])
			for productName in productsOrdered:
				product = TimeAndMaterials.objects.get(name=productName)
				products[product] = {}
				for gdrat in gdrats:
					products[product][gdrat] = 0.0
					if gdrat in GDRAT.objects.all():
						for forecast in TimeAndMaterialsForecast.objects.filter(year=year,qtr=qtr,product=product,GDRAT=gdrat):
							products[product][gdrat] += forecast.USD
				products[product][gdrat] = int(round(products[product][gdrat]))
			qtrs[qtr] = products
		NRR[year] = qtrs
		
	# set up workbook
	wb = xlwt.Workbook()
	sh_1 = wb.add_sheet('Sheet1', cell_overwrite_ok=True)
	sh_1.write(0,0,'Geo')
	sh_1.write(0,1,'Division')
	sh_1.write(0,2,'Region')
	sh_1.write(0,3,'Area')
	sh_1.write(0,4,'Territory')
	sh_1.write(0,5,'Product')
	y = 6
	for year in NRR:
		for qtr in NRR[year]:
			x = 1
			yearqtr = str(year.year)+'Q'+str(qtr.qtr)
			sh_1.write(0,y,yearqtr)
			for product in NRR[year][qtr]:
				for gdrat in NRR[year][qtr][product]:
					sh_1.write(x,0,gdrat.geo.name)
					sh_1.write(x,1,gdrat.division.name)
					sh_1.write(x,2,gdrat.region.name)
					sh_1.write(x,3,gdrat.area.name)
					sh_1.write(x,4,gdrat.territory.name)
					sh_1.write(x,5,product.name)
					sh_1.write(x,y,NRR[year][qtr][product][gdrat])
					x += 1
			y += 1
	
	# return extract
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=ServNRRFrcst_'+mapping+'.xls'
	wb.save(response)
	return response	
	
	
#paramter dict
exportDetailsDict = {'Contract MRR':MRRonContract,'Platform':PlatformProductFrcst,'Services MRR':ServMRRFrcst,'Services NRR':ServNRRFrcst}	
	