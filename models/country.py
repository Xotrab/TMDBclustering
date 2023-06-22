from marshmallow import Schema, fields, post_load
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Country(Base):
    __tablename__ = 'countries'

    iso_3166_1: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f'<Country iso_3166_1={self.iso_3166_1}, name={self.name}>'

class CountrySchema(Schema):
    iso_3166_1 = fields.String()
    name = fields.String()

    @post_load
    def make_custom_object(self, data, **kwargs):
        return Country(**data)