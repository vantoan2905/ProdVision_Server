from mongoengine import Document, StringField, ListField, DictField

class ChatHistory(Document):
    user_id = StringField(required=True)

    sessions = ListField(
        DictField()     
    )

    meta = {
        'collection': 'vantoan'
    }
