from django.db import models



class FileRecord(models.Model):
    file_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    file_name = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'files'




import numpy as np
from mongoengine import (
    Document, StringField, ListField, DictField, FloatField
)

class KnowledgeChunk(Document):
    meta = {
        "collection": "knowledge_db"
    }

    id = StringField(primary_key=True)
    text = StringField()
    embedding = ListField(FloatField())
    title = StringField()
    metadata = DictField()

