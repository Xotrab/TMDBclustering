from typing import List
from marshmallow import EXCLUDE, Schema, fields, post_load, pre_load

from models.person import Person, PersonSchema

class Credits():
    def __init__(self, cast, crew) -> None:
        self.cast: List[Person] = cast
        self.crew: List[Person] = crew


class CreditsSchema(Schema):
    cast = fields.Nested(PersonSchema, many=True)
    crew = fields.Nested(PersonSchema, many=True)

    #Exclude the unknown JSON fields from the deserialization
    class Meta:
        unknown = EXCLUDE
    
    @pre_load
    def filter_directors(self, data, **kwargs):
        # Filter the crew list to include only directors
        data['crew'] = [crew for crew in data.get('crew', []) if crew.get('job') == 'Director']
        return data
    
    @post_load
    def make_custom_object(self, data, **kwargs):
        return Credits(**data)