from rest_framework import serializers
from authentication.models import ACModel 

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ACModel
        fields = ('articleid','title','author','isvalid',)
