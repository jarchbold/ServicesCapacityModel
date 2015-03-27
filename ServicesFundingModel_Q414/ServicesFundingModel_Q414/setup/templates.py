# import global modules
import sys
sys.path.append('globalResources')
from importModules import *

from django.http import HttpResponse, HttpResponseRedirect

#need StringIO for Python 2 and Python 3 compatibility to access the dictionary
try:
	import cStringIO as StringIO
except ImportError:
	import StringIO

#creates the in memory file	
output = StringIO.StringIO()

def TemplateBuild(request,doc,headers):
	
	# set up workbook
	#output is the in memory file being passed to the workbook
	wb = xlsxwriter.Workbook(output)
	sh_1 = wb.add_worksheet()
	sh_2 = wb.add_worksheet()
	
	#Gives the workbook the ability to be locked
	locked = wb.add_format()
	locked.set_locked(True)
	
	#Format the headers of the work book
	header_format = wb.add_format({'bold':True,'bottom':2})
	header_format.set_text_wrap()
	header_format.set_align('center')
	header_format.set_align('vcenter')
	
	#formats row 0, i.e. the headers to be in larger cells
	sh_1.set_row(0,30)
	
	#Enables the second sheet to be locked; leverages the 'locked' format
	sh_2.protect()

	col = 0
	sh_1.set_column(col,col,15)
	
	#Checks each header passed from the template
	for header in headers:
		#writes the headers to both sheets
		sh_1.write(0,col,header,header_format)
		sh_2.write(0,col,header)
		list_row = 1
		#Checks if the header is in Dictionary
		if header in headerToModelDic:
			#if the header is in the dictionary, create a list of the entries
			list = listFunction(headerToModelDic[header])
			#write each entry in the list to the 2nd excel sheet
			for entry in list:
				sh_2.write(list_row,col,entry)
				list_row += 1
			#Ensure data validation in sheet 1 for headers that have choices
			sh_1.data_validation(1,col,50,col,{'validate':'list','source':rangeString('Sheet2',col,2,len(list)+1)})
		col += 1
	
	#activate sheet 1 as the sheet that will opened to allow hide feature
	sh_1.activate()
	#Hide the second sheet from users
	sh_2.hide()
	
	#close workbook
	wb.close()
	#finds the top of the file
	output.seek(0)
	
	# return file extract
	response = HttpResponse(output.read(),content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment;filename=%s_TEMPLATE.xlsx" % doc
	
	return response	

def FrcstTemplateBuild(request,doc,headers):
	# build components
	years = YearOrder(str)
	qtrs = QtrOrder(str)
	
	# set up workbook
	wb = xlsxwriter.Workbook(output)
	sh_1 = wb.add_worksheet()
	sh_2 = wb.add_worksheet()
	
	#Gives the workbook the ability to be locked
	locked = wb.add_format()
	locked.set_locked(True)
	
	#Format the headers of the work book
	header_format = wb.add_format({'bold':True,'bottom':2})
	header_format.set_text_wrap()
	header_format.set_align('center')
	header_format.set_align('vcenter')
	
	#formats row 1, i.e. the headers to be in larger cells
	sh_1.set_row(1,30)
	
	#Enables the second sheet to be locked; leverages the 'locked' format
	sh_2.protect()
	
	col = 0
	row = 2
	sh_1.set_column(col,col,15)
	
	#Checks each header passed from the template
	for header in headers:
		#writes the headers to both sheets
		sh_1.write(1,col,header,header_format)
		sh_2.write(0,col,header)
		list_row = 1
		#Checks if the header is in Dictionary
		if header in headerToModelDic:
			#if the header is in the dictionary, create a list of the entries
			list = listFunction(headerToModelDic[header])
			#write each entry in the list to the 2nd excel sheet
			for entry in list:
				sh_2.write(list_row,col,entry)
				list_row += 1
			#Ensure data validation in sheet 1 for headers that have choices
			sh_1.data_validation(2,col,50,col,{'validate':'list','source':rangeString('Sheet2',col,2,len(list)+1)})
		col += 1
	for year in years:
		for qtr in qtrs:
			sh_1.write(0,col,year)
			sh_1.write(1,col,qtr)
			col += 1
	
	#activate sheet 1 as the sheet that will opened to allow hide feature
	sh_1.activate()
	#Hide the second sheet from users
	sh_2.hide()
	
	#close the workbook
	wb.close()
	#finds the top of the file
	output.seek(0)
	
	#returns file extract
	response = HttpResponse(output.read(),content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment;filename=%s_TEMPLATE.xlsx" % doc
	
	return response	
	
#Blank template intended for admin use to upload new GDRATs
def BlankTemplateBuild(request,doc,headers):
	#set up workbook
	wb = xlsxwriter.Workbook(output)
	sh_1 = wb.add_worksheet()
	
	header_format = wb.add_format({'bold':True,'bottom':2})
	header_format.set_text_wrap()
	header_format.set_align('center')
	header_format.set_align('vcenter')
	
	sh_1.set_row(0,30)
	
	col = 0
	sh_1.set_column(col,len(headers),15)
	for header in headers:
		sh_1.write(0,col,header,header_format)
		col+=1
		
	wb.close()
	
	output.seek(0)
	# return extract
	
	response = HttpResponse(output.read(),content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment;filename=$s_TEMPLATE.xlsx" % doc
	
	return response
	
def GDRATTemplate(request,doc):
	headers = ['Geo','Division','Region','Area','Territory']
	return BlankTemplateBuild(request,doc,headers)
	
def FunctionTemplate(request,doc):
	headers = ['Role','BUR In Region','BUR Emerging','% in Region','% Emerging','Time to Productivity','Geo','Division','Region','Area','Territory']
	return TemplateBuild(request,doc,headers)

def HeadcountBISTemplate(request,doc):
	headers = ['Role','Geo','Division','Region','Area','Territory']
	return TemplateBuild(request,doc,headers)		

def HeadcountADJTemplate(request,doc):
	headers = ['Role','Geo','Division','Region','Area','Territory']
	return FrcstTemplateBuild(request,doc,headers,)	
	
def PlatformProductsTemplate(request,doc):
	headers = ['Platform Product','Hours Std Integration','Hours Mgd Integration','% Std','% Mdg','Time to Integrate (days)','Role','% Allocation','Role','% Allocation','CONTINUE ROLE AS NEEDED','CONTINUE ALLOCATION AS NEEDED']
	return TemplateBuild(request,doc,headers)
	
def ServicesMRRTemplate(request,doc):
	headers = ['GSS-Product','ARPU (USD)','ESR (USD)','Integration Delay (days)','Role','% Allocation','Role','% Allocation','Role','% Allocation','CONTINUE ROLE AS NEEDED','CONTINUE ALLOCATION AS NEEDED']
	return TemplateBuild(request,doc,headers)
		
def ServicesNRRTemplate(request,doc):
	headers = ['NRR Product','ESR (USD)','Role','% Allocation','Role','% Allocation','CONTINUE ROLE AS NEEDED','CONTINUE ALLOCATION AS NEEDED']
	return TemplateBuild(request,doc,headers)

def MRRContractTemplate(request,doc):
	headers = ['Account ID','Account Name','Marketing Product Name','MRR','GSS-Product','Geo','Division','Region','Area','Territory']
	return TemplateBuild(request,doc,headers)

def GSSMRRFrcstTemplate(request,doc):
	headers = ['Geo','Division','Region','Area','Territory','GSS-Product']
	return FrcstTemplateBuild(request,doc,headers)
	
def PlatformProductFrcstTemplate(request,doc):
	headers = ['Geo','Division','Region','Area','Territory','Platform Product']
	return FrcstTemplateBuild(request,doc,headers)

def GSSNRRFrcstTemplate(request,doc):
	headers = ['Geo','Division','Region','Area','Territory','NRR Product']
	return FrcstTemplateBuild(request,doc,headers)

# parameter dictionary
templateDic = {'GDRAT':GDRATTemplate,'Function':FunctionTemplate,'HeadcountBIS':HeadcountBISTemplate,'HeadcountADJ':HeadcountADJTemplate,'Product':PlatformProductsTemplate,'ServicesMRR':ServicesMRRTemplate,'ServicesNRR':ServicesNRRTemplate,'MRRContract':MRRContractTemplate,'PlatformProductFrcst':PlatformProductFrcstTemplate,'GSSMRRFrcst':GSSMRRFrcstTemplate,'GSSNRRFrcst':GSSNRRFrcstTemplate}
headerToModelDic = {'Geo':Geo,'Division':Division,'Region':Region,'Area':Area,'Territory':Territory,'Role':Role,'GSS-Product':GSSProduct,'NRR Product':TimeAndMaterials,'Platform Product':PlatformProduct}