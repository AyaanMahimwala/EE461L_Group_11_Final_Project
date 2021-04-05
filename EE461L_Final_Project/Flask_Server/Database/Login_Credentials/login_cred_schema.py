from marshmallow import Schema, fields

class LoginSetSchema(Schema):
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)
