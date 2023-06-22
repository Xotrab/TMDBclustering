from marshmallow import EXCLUDE, Schema, fields, post_load
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Person(Base):
    __tablename__ = 'people'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[int] = mapped_column(nullable=False)
    adult: Mapped[bool] = mapped_column(nullable=False)
    popularity: Mapped[float] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f'<Person id={self.id}, name={self.name}>'

class PersonSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    gender = fields.Integer()
    adult = fields.Boolean()
    popularity = fields.Float()

    #Exclude the unknown JSON fields from the deserialization
    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_custom_object(self, data, **kwargs):
        return Person(**data)
