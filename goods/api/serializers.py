from rest_framework import serializers

from goods.models import Categories, Products


class CategoryInternalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    slug  = serializers.SlugField()



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = (
            'id', 'name', 'slug',
        )
        read_only_fields = ('slug', )
        


class ProductSerializer(serializers.ModelSerializer):
     category = CategoryInternalSerializer(read_only=True)


     class Meta:
        model = Products
        fields = (
            'id', 'name', 'slug', 'description',
            'image', 'price', 'discount', 'quantity',
            'category',
        )
        read_only_fields = ('slug', 'category', )

         
         


# class CategorySerializer(serializers.Serializer):     # Simple serializer
#     name = serializers.CharField(max_length=150)

#     def to_internal_value(self, data):
#         validated = super().to_internal_value(data)
#         validated['test'] = 123
#         return validated
    

#     def to_representation(self, instance):
#         validated = super().to_representation(instance)
#         ...
#         return validated
    
