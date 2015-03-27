# import global modules
import sys
sys.path.append('globalResources')
from importModules import *

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
import re

from ModelApp.models import *
from ModelApp.forms import DocumentForm

sys.path.append('setup')
sys.path.append('view')
sys.path.append('run')
#sys.path.append('/app01/webroot/python/django/ServicesFundingModel/view')

def home(request):
	return render_to_response('ModelApp/home.html',RequestContext(request))
	
def about(request):
	return render_to_response('ModelApp/about.html',RequestContext(request))

def setup(request):
	return render_to_response('ModelApp/setup.html',RequestContext(request))

def docUpload(request,doc):

	from setupFunctions import setupDic

	# Handle file upload
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.save()
			
			# save new doc in db
			match = re.search(r'(documents/)(.+)',str(newdoc.docfile))
			
			#Validating File type
			try:
				check_wb = xlrd.open_workbook(file_abs_path+'/'+match.group(2))
			except:
				messages.add_message(request,messages.ERROR,'UPLOAD UNSUCCESSFUL: The file type was incorrect, please be sure you are uploading an .xls or .xlsx file.')
				return HttpResponseRedirect(reverse(doc, args=(doc,)))
			if setupDic[doc](match.group(2)):
				#successful upload confirm
				messages.add_message(request,messages.SUCCESS,'Your document was uploaded successfully!')
				# Redirect to the document list after POST
				return HttpResponseRedirect(reverse(doc, args=(doc,)))
			else:
				messages.add_message(request,messages.ERROR,'UPLOAD UNSUCCESSFUL: Your file template does not match the %s template in the system.' % doc) 
				return HttpResponseRedirect(reverse(doc, args=(doc,)))
		else:
			messages.add_message(request,messages.ERROR,'UPLOAD UNSUCCESSFUL: *This field is Required.')
			# Redirect to the document list after POST
			return HttpResponseRedirect(reverse(doc, args=(doc,)))
	else:
		form = DocumentForm() # A empty, unbound form
			
	# Render list page with the documents and form
	return render_to_response(
		'ModelApp/docUpload.html',
		{'form':form, 'name':doc},
		context_instance=RequestContext(request)
	)

def templateDownload(request,doc):
		
	from templates import templateDic
	
	return(templateDic[doc](request,doc))
	
def instructions(request,doc):

	from setupFunctions import instructions	
	
	if doc in instructions:
		docInstructions = instructions[doc]
	else:
		docInstructions = {}
		value = 'Instructions for '+str(doc)+' are not currently available.'
		docInstructions['Opps!'] = value
	
	return render_to_response('ModelApp/uploadInstructions.html',{'name':doc,'instructions':docInstructions},RequestContext(request))

def documents(request):

	# Load documents for the list page
	documents = Document.objects.all()
	
	return render_to_response('ModelApp/documents.html',{'documents':documents},RequestContext(request))

def setup(request):
	return render_to_response('ModelApp/setup.html',RequestContext(request))

def view(request):
	return render_to_response('ModelApp/view.html',RequestContext(request))

def viewFunction(request,mapping):
	
	from HeadcountAssumptions import RoleAssumptions
		
	return RoleAssumptions(request,mapping)	

def viewHeadcount(request,mapping):	
	
	from viewModel import TableView

	return TableView(request,'headcount',mapping)
	
def viewProduct(request,prod):
	
	from ProductAssumptions import productDict
		
	return productDict[prod](request,prod)		

def viewWorkingValue(request,prod):
	
	from ProductAssumptions import RoleAssumptions, modelDict
		
	return RoleAssumptions(request,prod,modelDict[prod][0],modelDict[prod][1])	
	
def viewForecast(request,prod,mapping):

	from viewModel import TableView

	return TableView(request,prod,mapping)
	
def exportDetailsForecast(request,prod,mapping):
	
	from exportDetailsForecast import exportDetailsDict

	return exportDetailsDict[prod](request,mapping)
	
def run(request,prod,mapping):
	
	tablestakes = request.GET.get('tablestakes')
	contracted = request.GET.get('contracted')
	forecast = request.GET.get('forecast')
	
	from runModel import *

	gdrats = GetGDRAT(mapping)[0]
	
	for gdrat in gdrats:
		if gdrat in GDRAT.objects.all():
			# DELETE HEADCOUNT REQUIREMENTS
			HeadcountRequirements.objects.filter(GDRAT=gdrat).delete()
			# UPDATE HEADCOUNT REQUIREMENTS
			if tablestakes == '1':
				Bucket(PlatformProductForecast,gdrat,PlatformProductFrcstUpdate)
			if contracted == '1':
				Bucket(MRRContract,gdrat,MRRContractUpdate)
				Bucket(TimeAndMaterialsForecast,gdrat,GSSNRRFrcstUpdate)
			if forecast == '1':
				Bucket(GSSProductForecast,gdrat,GSSMRRFrcstUpdate)
			if not tablestakes and not contracted and not forecast:
				Bucket(MRRContract,gdrat,MRRContractUpdate)
				Bucket(PlatformProductForecast,gdrat,PlatformProductFrcstUpdate)
				Bucket(GSSProductForecast,gdrat,GSSMRRFrcstUpdate)
				Bucket(TimeAndMaterialsForecast,gdrat,GSSNRRFrcstUpdate)

	from viewModel import TableView
	
	return TableView(request,prod,mapping,tablestakes,contracted,forecast)

def exportDetailsRun(request,prod,mapping):

	from exportDetails import exportDetails

	return exportDetails(request,prod,mapping)

def runReqs(request,prod,mapping):

	from runModel import *
	
	gdrats = GetGDRAT(mapping)[0]
	
	for gdrat in gdrats:
		if gdrat in GDRAT.objects.all():
			# DELETE HEADCOUNT ADJUSTMENTS
			HeadcountAdjustments.objects.filter(GDRAT=gdrat).delete()
			
	# UPDATE HEADCOUNT ADJUSTMENTS 	
	HeadcountDict[prod](gdrats)
	
	from viewModel import TableView

	return TableView(request,prod,mapping)	
	
def sandbox(request):
	return render_to_response('ModelApp/sandbox.html',RequestContext(request))
	
def contact(request):
	return render_to_response('ModelApp/contact.html',RequestContext(request))