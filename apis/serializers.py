from rest_framework import serializers
from authentication.models import ACModel 

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ACModel
        fields = ('url','articleid','title','author','isvalid',)
