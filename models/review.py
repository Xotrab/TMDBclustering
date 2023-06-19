from marshmallow import EXCLUDE, Schema, fields, post_load
from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[str] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))


    def __repr__(self) -> str:
        return f'<Review id={self.id}, content={self.content if len(self.content) < 21 else self.content[:20]}...>'

class ReviewSchema(Schema):
    id = fields.String()
    content = fields.String()

    #Exclude the unknown JSON fields from the deserialization
    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_custom_object(self, data, **kwargs):
        return Review(**data)