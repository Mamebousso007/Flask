from marshmallow import Schema, ValidationError, fields, validate, validates

from app.models import User

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50, error="Username must be between 1 and 50 characters."))
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6, error="Password must be at least 6 characters long."))
    #role = fields.Str(required=True)
    role = fields.Str(required=True, validate=validate.OneOf(["ADMIN", "USER"]))  

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    user_id = fields.Int(required=True)

    @validates('user_id')
    def validate_user_id(self, user_id):
        if not User.query.get(user_id):
            raise ValidationError("User ID does not exist.")
