from marshmallow import Schema, fields

class DataSetSchema(Schema):
    data_set_name = fields.Str()
    file_size = fields.Str()
    description = fields.Str()
    data_set_url = fields.URL()
    private = fields.Boolean(required=True)

class UserDataSetSchema(DataSetSchema):
    user_name = fields.Str(required=True)
