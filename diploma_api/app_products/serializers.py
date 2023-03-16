from rest_framework import serializers

from .models import Product, PropertyProduct, ImageProduct, Review


class PropertySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name.title')

    class Meta:
        model = PropertyProduct
        fields = ['name', 'value']


class ImageSerializer(serializers.ModelSerializer):
    src = serializers.FileField(source='pic')

    class Meta:
        model = ImageProduct
        fields = ['src']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['author', 'email', 'date', 'rate', 'text']


class ProductSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(many=True)
    # images = serializers.FileField(source='images.pic.url')
    reviews = ReviewSerializer(many=True)
    specifications = PropertySerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price', 'count', 'date',
            'title', 'description', 'fullDescription', 'href',
            'freeDelivery', 'images', 'tags', 'reviews',
            'rating', 'specifications',
        ]
