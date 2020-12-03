from rest_framework import serializers
from .models import Element, Category, Type
# importamos un modelo de otra aplicacion:
from comment.models import Comment




class CommentSerializer(serializers.ModelSerializer):

    count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        # fields = ['text','id'] # para que solo muestre algunos elementos
        fields = '__all__'

    def get_count(self, obj):
        print(obj)

        return Comment.objects.filter(element_id = obj.element_id).count()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class ElementSerializer(serializers.ModelSerializer):
    category =  CategorySerializer(read_only=True)
    type =  TypeSerializer(read_only=True)
    # comments = serializers.StringRelatedField(many=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Element
        fields = '__all__'