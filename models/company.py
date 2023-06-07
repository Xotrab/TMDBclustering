from marshmallow import EXCLUDE, Schema, fields, post_load
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Company(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    origin_country: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f'<Company id={self.id}, name={self.name}, origin_country={self.origin_country}>'

class CompanySchema(Schema):
    id = fields.Integer()
    name = fields.String()
    origin_country = fields.String()

    #Exclude the unknown JSON fields from the deserialization
    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_custom_object(self, data, **kwargs):
        return Company(**data)