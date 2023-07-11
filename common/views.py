from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from common.models import Quiz, Choice, Category
from common.serializers import QuizSerializer, ChoiceVoteSerializer, CategorySerializer


# Create your views here.


class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class ChoiceCreateView(generics.CreateAPIView):
    @swagger_auto_schema(request_body=ChoiceVoteSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ChoiceVoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        choice_id = serializer.validated_data.get('choice_id')
        choice = Choice.objects.get(id=choice_id)
        choice.votes += 1
        choice.save()

        if choice.is_correct == True:
            return Response({"detail": "togri javob"}, status=200)
        else:
            return Response({"detail": "notogri javob"}, status=400)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
