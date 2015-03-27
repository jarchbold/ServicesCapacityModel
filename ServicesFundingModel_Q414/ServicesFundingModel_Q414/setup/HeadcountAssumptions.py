# import global modules
import sys
sys.path.append('globalResources')
from importModules import *

def RoleAssumptions(request,mapping):
	
	gdrats = GetGDRAT(mapping)[0]
	level = GetGDRAT(mapping)[1]
	
	roles = OrderedDict([])
	instances = []
	
	def Percent(attribute):
		return str(attribute*100)+'%'
	
	for roleName in ModelOrder(Role):	
		role = Role.objects.get(name=roleName)
		
		count = 0
		for gdrat in gdrats:
			if gdrat in GDRAT.objects.all():
				
				if RoleProperties.objects.filter(role=role,GDRAT=gdrat):
					count += 1
				
				attribute = GetRoleProperties(role,gdrat)
				attributes = [
							Percent(attribute.BURinRegion),
							Percent(attribute.BUREmerging),
							Percent(attribute.pctinRegion),
							Percent(attribute.pctEmerging),
							Percent(attribute.BURinRegion*attribute.pctinRegion+attribute.BUREmerging*attribute.pctEmerging),
							#attribute.TimeToProductivity
							]
							
		# count num of role properties
		if count > 1:
			instances.append(str(role.name))
		
		roles[role] = attributes
	
	labels = ['BUR in Region','BUR Emerging','% in Region','% Emerging','Effective BUR']
	
	geos = GDRATMenu(Geo)
	divisions = GDRATMenu(Division)
	regions = GDRATMenu(Region)
	areas = GDRATMenu(Area)
	territories = GDRATMenu(Territory)
		
	return render_to_response('ModelApp/function.html',{'labels':labels,'roles':roles,'instances':instances,'geos':geos,'divisions':divisions,'regions':regions,'areas':areas,'territories':territories,'level':level,'mapping':mapping},RequestContext(request))	

# parameter dictionary