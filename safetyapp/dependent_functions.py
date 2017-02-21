import csv, pdb
import urllib.request
from decimal import Decimal
from io import TextIOWrapper

from safetyapp.models import Employee, SafetyCourse
from safetyapp.functions import *


# functions placed in this file are downstream of model definitions and thus cannot be loaded into model definition files
# they are for tasks that require explicit calls to model classes
# with proper coding of functions, very few functions should be needed here
# example: p.measure_set.all() instead of Measure.objects.filter(project = p)


