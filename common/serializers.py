from rest_framework import serializers

from common.models import Category, Choice, Quiz


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "answer", "is_correct", "votes", "percent"]


class ChoiceVoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()


class QuizSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "created_at", "choices"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]
