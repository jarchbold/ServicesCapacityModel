import sys
sys.path.insert(0, '../')

import os

# enable interaction with sqliteDB
os.environ['DJANGO_SETTINGS_MODULE'] = 'ServicesFundingModel.settings'

# Django models
from ModelApp.models import *

# Global functions used by Services Model
from functions import *
'''
# stats/graphics packages
sys.path.append('C:/Anaconda/Lib/site-packages')
import math
import numpy as np
import matplotlib.pyplot as plt
'''
# reading/writing excel modules
import xlrd, xlwt
from xlrd import open_workbook
import xlsxwriter

# python standard libraries
from datetime import datetime, timedelta
import re
import copy
from collections import OrderedDict
import threading
import math
import locale

# Django view modules
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from collections import OrderedDict