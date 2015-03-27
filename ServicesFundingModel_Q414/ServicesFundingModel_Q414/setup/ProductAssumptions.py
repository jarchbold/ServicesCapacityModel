# import global modules
import sys
sys.path.append('globalResources')
from importModules import *

def Percent(attribute):
	return str(attribute*100)+'%'
	
def PlatformProductAssumptions(request,prod):
	
	products = OrderedDict([])

	for productName in ModelOrder(PlatformProduct):
		product = PlatformProduct.objects.get(name=productName)
		
		attribute = PlatformProductProperties.objects.get(product=product)
		attributes = [
					attribute.HoursStdImplementation,
					attribute.HoursMgdImplementation,
					Percent(attribute.pctStd),
					Percent(attribute.pctMgd),
					attribute.HoursStdImplementation*attribute.pctStd+attribute.HoursMgdImplementation*attribute.pctMgd,
					attribute.TimeToIntegrate
					]
					
		products[product] = attributes
	
	labels = ['Hours Standard Integration','Hours Managed Integration','% Standard Integration','% Managed Integration','Hours Average Integration','Time to Integrate (days)']

	return render_to_response('ModelApp/product.html',{'labels':labels,'products':products,'product':prod},RequestContext(request))	
	
def GSSProductAssumptions(request,prod):
	
	locale.setlocale(locale.LC_ALL,'')
	
	products = OrderedDict([])
	
	for productName in ModelOrder(GSSProduct):
		product = GSSProduct.objects.get(name=productName)
		
		attribute = GSSProductProperties.objects.get(product=product)
		attributes = [
					locale.currency(attribute.ARPU,grouping=True),
					locale.currency(attribute.ESR,grouping=True),
					attribute.IntegrationDelay,
					]
		products[product] = attributes
	
	labels = ['Unit ARPU','Effective Sell Rate','Integration Delay (days)']
		
	return render_to_response('ModelApp/product.html',{'labels':labels,'products':products,'product':prod},RequestContext(request))

def TimeAndMaterialsAssumptions(request,prod):
	
	locale.setlocale(locale.LC_ALL,'')
	
	products = OrderedDict([])
	
	for productName in ModelOrder(TimeAndMaterials):
		product = TimeAndMaterials.objects.get(name=productName)
		
		attribute = TimeAndMaterialsProperties.objects.get(product=product)
		attributes = [
					locale.currency(attribute.ESR,grouping=True),
					]
		products[product] = attributes
	
	labels = ['Effective Sell Rate']
		
	return render_to_response('ModelApp/product.html',{'labels':labels,'products':products,'product':prod},RequestContext(request))	

def RoleAssumptions(request,prod,productModel,workingValueModel):
	
	products = OrderedDict([])
	
	for productName in ModelOrder(productModel):
		product = productModel.objects.get(name=productName)
		
		roles = OrderedDict([])
		
		for roleName in ModelOrder(Role):
			role = Role.objects.get(name=roleName)
		
			if workingValueModel.objects.filter(product=product,role=role):
				pct = workingValueModel.objects.get(product=product,role=role).pct
			else:
				pct = 0
			roles[role] = Percent(pct)
			products[product] = roles
			
	return render_to_response('ModelApp/workingValue.html',{'products':products,'roles':roles,'product':prod},RequestContext(request))		
	
# parameter dictionary
productDict = {'Platform':PlatformProductAssumptions,'Contract MRR':GSSProductAssumptions,'Services MRR':GSSProductAssumptions,'Services NRR':TimeAndMaterialsAssumptions}
modelDict = {'Platform':(PlatformProduct,PlatformProductWorkingValue),'Contract MRR':(GSSProduct,GSSProductWorkingValue),'Services MRR':(GSSProduct,GSSProductWorkingValue),'Services NRR':(TimeAndMaterials,TimeAndMaterialsWorkingValue)}

