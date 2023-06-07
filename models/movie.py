from marshmallow import EXCLUDE, Schema, fields, post_load
import marshmallow
from sqlalchemy.types import Enum
from typing import List
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.country import Country, CountrySchema

from models.genre import Genre, GenreSchema
from models.language import Language, LanguageSchema
from models.movie_genre import movie_genre_table
from models.movie_company import movie_company_table
from models.movie_country import movie_country_table
from models.movie_language import movie_language_table
from models.company import Company, CompanySchema
from models.status_enum import StatusEnum

class Movie(Base):
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    original_title: Mapped[str] = mapped_column(nullable=False)
    original_language: Mapped[str] = mapped_column(nullable=False)
    overview: Mapped[str] = mapped_column(nullable=True)
    tagline: Mapped[str] = mapped_column(nullable=True)
    release_date: Mapped[str] = mapped_column(nullable=False)
    budget: Mapped[int] = mapped_column(nullable=False)
    popularity: Mapped[float] = mapped_column(nullable=False)
    revenue: Mapped[int] = mapped_column(nullable=False)
    vote_average: Mapped[float] = mapped_column(nullable=False)
    vote_count: Mapped[int] = mapped_column(nullable=False)
    runtime: Mapped[int] = mapped_column(nullable=True)
    adult: Mapped[bool] = mapped_column(nullable=False)
    video: Mapped[bool] = mapped_column(nullable=False)
    status = mapped_column(Enum(StatusEnum), nullable=False)
    poster_path: Mapped[str] = mapped_column(nullable=True)
    backdrop_path: Mapped[str] = mapped_column(nullable=True)

    genres: Mapped[List[Genre]] = relationship(secondary=movie_genre_table)
    production_companies: Mapped[List[Company]] = relationship(secondary=movie_company_table)
    production_countries: Mapped[List[Country]] = relationship(secondary=movie_country_table)
    spoken_languages: Mapped[List[Language]] = relationship(secondary=movie_language_table)
    
    def __repr__(self) -> str:
        return f'<Movie id={self.id}, title={self.title}, spoken_languages={self.spoken_languages}>'

class MovieSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    original_title = fields.String()
    original_language = fields.String()
    overview = fields.String(allow_none=True)
    tagline = fields.String(allow_none=True)
    release_date = fields.String()
    budget = fields.Integer()
    popularity = fields.Float()
    revenue = fields.Integer()
    vote_average = fields.Float()
    vote_count = fields.Integer()
    runtime = fields.Raw(allow_none=True)
    adult = fields.Boolean()
    video = fields.Boolean()
    status = fields.Raw()
    poster_path = fields.String(allow_none=True)
    backdrop_path = fields.String(allow_none=True)

    genres = fields.Nested(GenreSchema, many=True)
    production_companies = fields.Nested(CompanySchema, many=True)
    production_countries = fields.Nested(CountrySchema, many=True)
    spoken_languages = fields.Nested(LanguageSchema, many=True)

    #Exclude the unknown JSON fields from the deserialization
    class Meta:
        unknown = EXCLUDE
    
    @post_load
    def make_custom_object(self, data, **kwargs):
        return Movie(**data)
    
    def load_enum_field(self, value):
        try:
            return StatusEnum[value.upper()]
        except KeyError:
            raise ValueError(f"Invalid enum value: {value}")

    @marshmallow.pre_load
    def preprocess_data(self, data, **kwargs):
        data['status'] = self.load_enum_field(data.get('status'))
        return data