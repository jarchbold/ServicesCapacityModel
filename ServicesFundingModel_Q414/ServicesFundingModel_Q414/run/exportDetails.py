# import global modules
import sys
sys.path.append('globalResources')
from importModules import *

from django.http import HttpResponse

def exportDetails(request,prod,mapping):

	ModelDict = {'run':HeadcountRequirements,'runReqs':HeadcountAdjustments,'runGap':HeadcountAdjustments}
	fileName = {'run':'Requirements','runReqs':'Deployment','runGap':'Comparison'}
	Model = ModelDict[prod]
	
	gdrats = GetGDRAT(mapping)[0]
	
	# data aggregation
	headcounts = OrderedDict([])
	
	yearsOrdered = YearOrder(str)
	qtrsOrdered = QtrOrder(str)
	rolesOrdered = ModelOrder(Role)
	
	for yearNum in yearsOrdered:
		year = Year.objects.get(year=yearNum)
		qtrs = OrderedDict([])
		for qtrNum in qtrsOrdered:
			qtr = Qtr.objects.get(qtr=qtrNum)
			roles = OrderedDict([])
			for roleName in rolesOrdered:
				role = Role.objects.get(name=roleName)
				roles[role] = {}
				for gdrat in gdrats:
					roles[role][gdrat] = 0.0
					if gdrat in GDRAT.objects.all():
						for headcount in Model.objects.filter(year=year,qtr=qtr,role=role,GDRAT=gdrat):
							roles[role][gdrat] += headcount.fte
				roles[role][gdrat] = int(round(roles[role][gdrat]))
			qtrs[qtr] = roles
		headcounts[year] = qtrs
		
	# set up workbook
	wb = xlwt.Workbook()
	sh_1 = wb.add_sheet('Sheet1', cell_overwrite_ok=True)
	sh_1.write(0,0,'Geo')
	sh_1.write(0,1,'Division')
	sh_1.write(0,2,'Region')
	sh_1.write(0,3,'Area')
	sh_1.write(0,4,'Territory')
	sh_1.write(0,5,'Role')
	y = 6
	for year in headcounts:
		for qtr in headcounts[year]:
			x = 1
			yearqtr = str(year.year)+'Q'+str(qtr.qtr)
			sh_1.write(0,y,yearqtr)
			for role in headcounts[year][qtr]:
				for gdrat in headcounts[year][qtr][role]:
					sh_1.write(x,0,gdrat.geo.name)
					sh_1.write(x,1,gdrat.division.name)
					sh_1.write(x,2,gdrat.region.name)
					sh_1.write(x,3,gdrat.area.name)
					sh_1.write(x,4,gdrat.territory.name)
					sh_1.write(x,5,role.name)
					sh_1.write(x,y,headcounts[year][qtr][role][gdrat])
					x += 1
			y += 1
	
	# return extract
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Headcount_'+str(fileName[prod])+'_'+str(mapping)+'.xls'
	wb.save(response)
	return response