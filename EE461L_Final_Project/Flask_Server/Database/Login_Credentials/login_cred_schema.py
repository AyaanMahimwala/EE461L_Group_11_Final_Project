from marshmallow import Schema, fields

class LoginSetSchema(Schema):
    user_name = fields.Str(required=True)
    user_password = fields.Str(required=True)
    user_active = fields.Boolean(required=True)
    user_email = fields.Email(required=False)
