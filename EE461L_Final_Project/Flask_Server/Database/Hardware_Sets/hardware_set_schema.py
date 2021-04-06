from marshmallow import Schema, fields

class HardwareSetSchema(Schema):
    hardware_set_name = fields.Str()
    # Availability is in form "cluster_name" = units_available
    # Will subtract units from this field, with error checks of course
    availability = fields.Dict(keys=fields.Str(), values=fields.Int())
    description = fields.Str()
    # As of now all clusters have the same unit price
    price_per_unit = fields.Float()
