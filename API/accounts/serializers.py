from rest_framework import serializers 
from .models import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser , IsAuthenticated



class HesabhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hesabha
        fields = ('code_hesab' , 'name_hesab' , )

    # har yek az commend haye zir ra az comment biron avarid field ha ovveride mishavad

    code_hesab = serializers.CharField()
    name_hesab = serializers.CharField()
    # title= serializers.CharField(max_length=200)
    # price_rial = serializers.SerializerMethodField()
    # category = serializers.StringRelatedField()
    # category = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name='name url ke neveshti vasash ke ye view behesh vasl kardi ke category ba hamin id ro bargardone'
    # )

    # read_only_fields = []

    # def get_price_rial(self , product):
    #     return product.price * 10

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.save()
    #     return product



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    # har yek az commend haye zir ra az comment biron avarid field ha ovveride mishavad


class AsnadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asnad
        fields = "__all__"

    # har yek az commend haye zir ra az comment biron avarid field ha ovveride mishavad
