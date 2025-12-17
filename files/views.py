import os
import logging
import cv2
import numpy as np

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from files.service.service import Service
from files.models import KnowledgeChunk



class ImageProcessingView(APIView):
    """
    Upload an image and extract text via OCR.
    """
    service = Service()

    @swagger_auto_schema(
        operation_description="Upload an image and extract text via OCR.",
        manual_parameters=[
            openapi.Parameter(
                'image',
                openapi.IN_FORM,
                description="Image file (JPEG, PNG, GIF)",
                type=openapi.TYPE_FILE,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                'Text extracted',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'documents': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)),
                    },
                ),
            ),
            400: openapi.Response('Missing or invalid file'),
            413: openapi.Response('File too large'),
            415: openapi.Response('Unsupported file type'),
            500: openapi.Response('Processing failed'),
        },
        consumes=['multipart/form-data'],
        produces=['application/json'],
    )
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({"error": "No image uploaded"}, status=400)

        
        file_bytes = image_file.read()
        np_bytes = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(np_bytes, cv2.IMREAD_COLOR)
        if img is None:
            return Response({"error": "Invalid image format"}, status=400)

        data_in_image = self.service.process_image(img, image_file.name)
        chunks = self.service.split_text(data_in_image["text"])
        vectors = self.service.vectorize_texts(chunks)

        # Build documents
        documents = [
            {
                "id": f"{data_in_image['id']}-{i}",
                "text": chunk,
                "embedding": vector,
                "metadata": {
                    "file_name": data_in_image["file_name"],
                    "original_id": data_in_image["id"],
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "ocr_metadata": data_in_image.get("metadata", {}),
                },
            }
            for i, (chunk, vector) in enumerate(zip(chunks, vectors))
        ]

        # Save to KnowledgeChunk model
        for doc in documents:
            KnowledgeChunk.objects.create(
                id=doc["id"],
                text=doc["text"],
                embedding=doc["embedding"],
                metadata=doc["metadata"]
            )

        return Response({"documents": documents}, status=200)


class HistoryFilesView(APIView):
    """
    List all uploaded files.
    """
    @swagger_auto_schema(
        operation_description="Load and list files uploaded by users.",
        responses={
            200: openapi.Response(
                'List of files',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'files': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'file_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'upload_time': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                                },
                            ),
                        ),
                    },
                ),
            ),
            500: openapi.Response('Failed to load files'),
        },
        produces=['application/json'],
    )
    def get(self, request, *args, **kwargs):
        try:
            from files.models import FileRecord
            files_data = [
                {
                    "file_id": record.file_id,
                    "user_id": record.user_id,
                    "file_name": record.file_name,
                    "upload_time": record.upload_time,
                }
                for record in FileRecord.objects.all()
            ]
            return Response({"files": files_data}, status=200)
        except Exception as e:
            return Response({"error": "Failed to load files"}, status=500)


class ProcessPDFView(APIView):
    """
    Upload a PDF and extract text.
    """
    service = Service()

    @swagger_auto_schema(
        operation_description="Upload a PDF file and extract text.",
        manual_parameters=[
            openapi.Parameter(
                'pdf',
                openapi.IN_FORM,
                description="PDF file",
                type=openapi.TYPE_FILE,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                'List of documents',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'documents': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)),
                    },
                ),
            ),
            400: openapi.Response('No PDF file uploaded'),
            500: openapi.Response('Failed to process PDF'),
        },
        consumes=['multipart/form-data'],
        produces=['application/json'],
    )
    def post(self, request, *args, **kwargs):
        pdf_file = request.FILES.get('pdf')
        if not pdf_file:
            return Response({"error": "No PDF file uploaded"}, status=400)

        # Save temporary PDF file
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)
        with open(pdf_path, "wb") as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        try:
            data_in_pdf = self.service.process_pdf(pdf_path)
            chunks = self.service.split_text_pdf(data_in_pdf["text"])
            vectors = self.service.vectorize_texts(chunks)

            documents = [
                {
                    "id": f"{data_in_pdf['id']}-{i}",
                    "text": chunk,
                    "embedding": vector,
                    "metadata": {
                        "file_name": data_in_pdf["file_name"],
                        "original_id": data_in_pdf["id"],
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "ocr_metadata": data_in_pdf.get("metadata", {}),
                    },
                }
                for i, (chunk, vector) in enumerate(zip(chunks, vectors))
            ]
            return Response({"documents": documents}, status=200)
        except Exception as e:
            return Response({"error": "Failed to process PDF"}, status=500)
        finally:
            # Clean up temp file
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
