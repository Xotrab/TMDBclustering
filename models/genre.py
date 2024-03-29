from marshmallow import Schema, fields, post_load
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f'<Genre id={self.id}, name={self.name}>'

class GenreSchema(Schema):
    id = fields.Integer()
    name = fields.String()

    @post_load
    def make_custom_object(self, data, **kwargs):
        return Genre(**data)
