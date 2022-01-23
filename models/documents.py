import mongoengine as me


class Ticket(me.Document):
    chat_id: int = me.IntField()
    message_id: int = me.IntField()
    user_id: int = me.IntField()


class User(me.Document):
    id: int = me.IntField(primary_key=True)
    invited_users_ids: list[int] = me.ListField(me.IntField())


class WelcomeMessage(me.Document):
    message_id: int = me.IntField()
