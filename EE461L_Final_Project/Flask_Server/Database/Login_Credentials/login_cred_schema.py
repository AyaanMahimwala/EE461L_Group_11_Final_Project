from marshmallow import Schema, fields

class LoginSetSchema(Schema):
    user_id = fields.Str(required=True)
    password = fields.Str(required=True)

