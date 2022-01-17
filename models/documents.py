import mongoengine as me


class Ticket(me.Document):
    chat_id: int = me.IntField()
    message_id: int = me.IntField()
    user_id: int = me.IntField()
