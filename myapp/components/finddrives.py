from .jwt_auth import login, logout, is_authenticated, needs_authentication
from myapp.models import *
import psutil

def my_disks():
	return psutil.disk_partitions()