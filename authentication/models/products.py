import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.products_categories_xref import products_categories_xref


class Products(db.Model):
    __tablename__ = "Products"

    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    price = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Companies.company_id", ondelete="CASCADE"), nullable=False)

    company = db.relationship('Companies', back_populates='products', cascade='all')
    categories = db.relationship('Categories', secondary=products_categories_xref, back_populates='products')
    warranty = db.relationship('Warranties', back_populates='product', uselist=False, cascade='all')

    def __init__(self, product_name, description, price, company_id, active=True):
        self.product_name = product_name
        self.description = description
        self.price = price
        self.company_id = company_id
        self.active = active

    def new_product_obj():
        return Products("", "", 0.0, "", True)


class ProductsSchema(ma.Schema):
    class Meta:
        fields = ['product_id', 'product_name', 'description', 'price', 'company', 'categories', 'active']
    company = ma.fields.Nested("CompaniesSchema", exclude=['products'])
    categories = ma.fields.Nested("CategoriesSchema", many=True)
    warranty = ma.fields.Nested("WarrantiesSchema", exclude=['product'])


product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)
