from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, EmbeddedDocumentListField




# ===========================
# Chat message / history item
# ===========================
class ChatHistory(EmbeddedDocument):
    role = StringField(required=True)
    response = StringField(required=True)
    timestamp = DateTimeField(required=True)

# ===========================
# Chat session
# ===========================
class ChatSession(Document):
    user_id = StringField(required=True)
    session_id = StringField(required=True)
    session_name = StringField(required=True)
    created_at = DateTimeField(required=True)
    data = EmbeddedDocumentListField(ChatHistory)  