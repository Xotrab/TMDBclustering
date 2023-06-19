from marshmallow import EXCLUDE, Schema, fields, post_load
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Language(Base):
    __tablename__ = 'languages'

    iso_639_1: Mapped[str] = mapped_column(primary_key=True)
    english_name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f'<Language iso_639_1={self.iso_639_1}, english_name={self.english_name}>'

class LanguageSchema(Schema):
    iso_639_1 = fields.String()
    english_name = fields.String()

    #Exclude the unknown JSON fields from the deserialization
    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_custom_object(self, data, **kwargs):
        return Language(**data)