from rest_framework import serializers
from .models import *

class HistorySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = History
		fields = '__all__'