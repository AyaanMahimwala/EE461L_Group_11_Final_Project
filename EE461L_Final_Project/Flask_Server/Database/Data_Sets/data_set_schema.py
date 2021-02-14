from marshmallow import Schema, fields

class DataSetSchema(Schema):
    id = fields.Int(required=True)
    data_set_name = fields.Str()
    file_size = fields.Str()
    description = fields.Str()
    data_set_url = fields.URL()

class UserDataSetSchema(DataSetSchema):
    user_id = fields.Email(required=True)
