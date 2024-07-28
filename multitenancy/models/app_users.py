import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class AppUsers(db.Model):
  __tablename__ = "AppUsers"

  user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  first_name = db.Column(db.String(), nullable=False)
  last_name = db.Column(db.String(), nullable=False)
  email = db.Column(db.String(), nullable=False)
  password = db.Column(db.String(), nullable=False)
  phone = db.Column(db.String(), nullable=False)
  active = db.Column(db.Boolean(), nullable=False, default=True)
  role = db.Column(db.String(), nullable=False, default="user")
  org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Organizations.org_id'), nullable=False)

  org = db.relationship('Organizations', back_populates='users')
  auth = db.relationship('AuthTokens', back_populates='users')

  def __init__(self, first_name, last_name, email, password, org_id, phone=None, active=True, role="user"):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password
    self.phone = phone
    self.active = active
    self.role = role
    self.org_id = org_id
    

  def new_user_obj():
    return AppUsers('', '', '', '', '', None, True, "user")
  
class AppUsersSchema(ma.Schema):
  class Meta:
    fields = ['user_id', 'first_name', 'last_name', 'email', 'phone', 'org', 'active', 'role']

  org = ma.fields.Nested('OrganizationsSchema', exclude=['users'])

user_schema = AppUsersSchema()
users_schema = AppUsersSchema(many=True)