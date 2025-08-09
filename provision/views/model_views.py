# provision/views/model_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class ModelManagerViews(APIView):

    @swagger_auto_schema(responses={200: "OK"})
    def get(self, request):
        """Health check service"""
        return Response({"message": "OK"}, status=status.HTTP_200_OK)


class HealthModelCheckView(APIView):

    @swagger_auto_schema(responses={200: "OK"})
    def get(self, request):
        # TODO: health check model
        return Response({"message": "Model OK"}, status=status.HTTP_200_OK)


class TrainModelView(APIView):

    @swagger_auto_schema(responses={200: "Training started"})
    def post(self, request):
        # TODO: train model
        return Response({"message": "Training started"}, status=status.HTTP_200_OK)


class EvaluateModelView(APIView):

    @swagger_auto_schema(responses={200: "Evaluation complete"})
    def post(self, request):
        # TODO: evaluate model
        return Response({"message": "Evaluation complete"}, status=status.HTTP_200_OK)


class SaveModelView(APIView):

    @swagger_auto_schema(responses={200: "Model saved"})
    def post(self, request):
        # TODO: save model
        return Response({"message": "Model saved"}, status=status.HTTP_200_OK)


class SaveResultsView(APIView):

    @swagger_auto_schema(responses={200: "Results saved"})
    def post(self, request):
        # TODO: save results
        return Response({"message": "Results saved"}, status=status.HTTP_200_OK)
