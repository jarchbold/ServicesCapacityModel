from django.db import models

# Create your models here.

# FILE UPLOAD MODEL
class Document(models.Model):
	docfile = models.FileField(upload_to='documents')

# FIRST TIER TABLES
class Year(models.Model):
	year = models.IntegerField(unique=True)
	def __unicode__(self):
		return unicode(self.year)
		
class Qtr(models.Model):
	qtr = models.IntegerField(unique=True)
	def __unicode__(self):
		return unicode(self.qtr)

class Role(models.Model):
	name = models.CharField(max_length=100, unique=True)
	def __unicode__(self):
		return unicode(self.name)
		
class Geo(models.Model):
	name = models.CharField(max_length=100, unique=True)
	def __unicode__(self):
		return unicode(self.name)
		
class Division(models.Model):
	name = models.CharField(max_length=100, unique=True)
	def __unicode__(self):
		return unicode(self.name)
		
class Region(models.Model):
	name = models.CharField(max_length=100, unique=True)
	def __unicode__(self):
		return unicode(self.name)
		
class Area(models.Model):
	name = models.CharField(max_length=100, unique=True)
	def __unicode__(self):
		return unicode(self.name)
		
class Territory(models.Model):
	name = models.CharField(max_length=100, unique=True)
	def __unicode__(self):
		return unicode(self.name)
		
class PlatformProduct(models.Model):
	name = models.CharField(max_length=100, unique=True)
	def __unicode__(self):
		return unicode(self.name)
	class Meta:
		verbose_name="Platform Product"
		
class GSSProduct(models.Model):
	name = models.CharField(max_length=100, unique=True)
	def __unicode__(self):
		return unicode(self.name)
	class Meta:
		verbose_name="Services MRR Product"
		
class TimeAndMaterials(models.Model):
	name = models.CharField(max_length=100, unique=True)
	def __unicode__(self):
		return unicode(self.name)		
	class Meta:
		verbose_name="Services NRR Product"
		
# SECOND TIER TABLES
class GDRAT(models.Model):
	geo = models.ForeignKey(Geo)
	division = models.ForeignKey(Division)
	region = models.ForeignKey(Region)
	area = models.ForeignKey(Area)
	territory = models.OneToOneField(Territory)
	def __unicode__(self):
		return unicode(str(self.geo.name)+' | '+str(self.division.name)+' | '+str(self.region.name)+' | '+str(self.area.name)+' | '+str(self.territory.name))
	class Meta:
		verbose_name="GDRAT Mapping"

class RoleProperties(models.Model):
	role = models.ForeignKey(Role)
	GDRAT = models.ForeignKey(GDRAT)
	BURinRegion = models.FloatField(default=.60, verbose_name="BUR In Region")
	BUREmerging = models.FloatField(default=.54, verbose_name ="BUR Emerging Region")
	pctinRegion = models.FloatField(default=1.0, verbose_name="Percent In Region")
	pctEmerging = models.FloatField(default=0, verbose_name="Percent Emerging Region")
	TimeToProductivity = models.IntegerField(default=0, verbose_name="Time to Productivity (days)")
	def __unicode__(self):
		return unicode(str(self.role.name)+' | '+str(self.GDRAT))
	class Meta:
		verbose_name="Role Attribute"

class PlatformProductProperties(models.Model):
	product = models.OneToOneField(PlatformProduct)
	HoursStdImplementation = models.IntegerField(default=10, verbose_name="Hours per Standard Implementation")
	HoursMgdImplementation = models.IntegerField(default=32, verbose_name="Hours per Mangaged Implementation")
	pctStd = models.FloatField(default=.60, verbose_name="Percent Standard")
	pctMgd = models.FloatField(default=.40, verbose_name="Percent Managed")
	TimeToIntegrate = models.IntegerField(default=40, verbose_name="Time to Integrate (days)")
	def __unicode__(self):
		return unicode(self.product)
	class Meta:
		verbose_name="Product Attribute"

class GSSProductProperties(models.Model):
	product = models.OneToOneField(GSSProduct)
	ARPU = models.IntegerField(default=3000)
	ESR = models.IntegerField(default=250)
	IntegrationDelay = models.IntegerField(default=30, verbose_name="Integration Delay (days)")
	def __unicode__(self):
		return unicode(self.product)
	class Meta:
		verbose_name="Product Attribute"

class TimeAndMaterialsProperties(models.Model):
	product = models.OneToOneField(TimeAndMaterials)
	ESR = models.IntegerField(default=225)
	def __unicode__(self):
		return unicode(self.product)
	class Meta:
		verbose_name="Product Attribute"

class PlatformProductWorkingValue(models.Model):
	product = models.ForeignKey(PlatformProduct)
	role = models.ForeignKey(Role)
	pct = models.FloatField(default=0.0, verbose_name="Allocation (%)")
	def __unicode__(self):
		return unicode(self.product)
	class Meta:
		verbose_name="Product Functional Alignment"
		
class GSSProductWorkingValue(models.Model):
	product = models.ForeignKey(GSSProduct)
	role = models.ForeignKey(Role)
	pct = models.FloatField(default=0.0, verbose_name="Allocation (%)")
	def __unicode__(self):
		return unicode(self.product)
	class Meta:
		verbose_name="Product Functional Alignment"
		
class TimeAndMaterialsWorkingValue(models.Model):
	product = models.ForeignKey(TimeAndMaterials)
	role = models.ForeignKey(Role)
	pct = models.FloatField(default=0.0, verbose_name="Allocation (%)")
	def __unicode__(self):
		return unicode(self.product)
	class Meta:
		verbose_name="Product Functional Alignment"

# THIRD TIER TABLES		
class MRRContract(models.Model):
	product = models.ForeignKey(GSSProduct)
	GDRAT = models.ForeignKey(GDRAT)
	USD = models.FloatField(default=0.0)
	year = models.ForeignKey(Year)
	qtr = models.ForeignKey(Qtr)

class PlatformProductForecast(models.Model):
	product = models.ForeignKey(PlatformProduct)
	GDRAT = models.ForeignKey(GDRAT)
	units = models.FloatField(default=0.0)
	year = models.ForeignKey(Year)
	qtr = models.ForeignKey(Qtr)
	'''
	def __unicode__(self):
		return unicode(str(self.product.name)+' | '+str(self.GDRAT)+' | '+str(self.year.year)+':'+str(self.qtr.qtr))
	class Meta:
		verbose_name="Platform Forecast"
	'''
	
class GSSProductForecast(models.Model):
	product = models.ForeignKey(GSSProduct)
	GDRAT = models.ForeignKey(GDRAT)
	units = models.FloatField(default=0.0)
	year = models.ForeignKey(Year)
	qtr = models.ForeignKey(Qtr)
	class Meta:
		verbose_name="Services MRR Forecast"
	
class TimeAndMaterialsForecast(models.Model):
	product = models.ForeignKey(TimeAndMaterials)
	GDRAT = models.ForeignKey(GDRAT)
	USD = models.FloatField(default=0.0)
	year = models.ForeignKey(Year)
	qtr = models.ForeignKey(Qtr)
	class Meta:
		verbose_name="Services NRR Forecast"

class HeadcountBIS(models.Model):
	role = models.ForeignKey(Role)
	GDRAT = models.ForeignKey(GDRAT)
	year = models.ForeignKey(Year)
	qtr = models.ForeignKey(Qtr)
	fte = models.FloatField(default=0.0)
	'''
	def __unicode__(self):
		return unicode(str(self.role.name)+' | '+str(self.GDRAT)+' | '+self.fte)
	class Meta:
		verbose_name="Headcount B.I.S."
	'''
	
class HeadcountAdjustments(models.Model):
	role = models.ForeignKey(Role)
	GDRAT = models.ForeignKey(GDRAT)
	year = models.ForeignKey(Year)
	qtr = models.ForeignKey(Qtr)
	fte = models.FloatField(default=0.0)
	notes = models.CharField(max_length=100, blank=True, null=True)
	'''
	def __unicode__(self):
		return unicode(str(self.role.name)+' | '+str(self.GDRAT)+' | '+self.fte)
	class Meta:
		verbose_name="Headcount Adjustments"
	'''
	
class HeadcountRequirements(models.Model):
	role = models.ForeignKey(Role)
	GDRAT = models.ForeignKey(GDRAT)
	year = models.ForeignKey(Year)
	qtr = models.ForeignKey(Qtr)
	fte = models.FloatField(default=0.0)
	'''
	def __unicode__(self):
		return unicode(str(self.role.name)+' | '+str(self.GDRAT)+' | '+self.fte)
	class Meta:
		verbose_name="Headcount Requirements"
	'''


	