from mongoengine import Document, StringField, ListField, DictField, DateTimeField
from datetime import datetime

class KnowledgeBase(Document):
    user_id = StringField(required=True)  # nếu bạn muốn KB riêng cho từng user
    title = StringField(required=True)    # tiêu đề hoặc tên document
    content = StringField(required=True)  # nội dung chính
    metadata = DictField()                # thông tin thêm: nguồn, tag, category, language,...
    embeddings = ListField()              # vector embeddings nếu dùng cho RAG
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'knowledge_base',  # tên collection
        'indexes': ['user_id', 'title']  # index để truy vấn nhanh theo user hoặc title
    }
