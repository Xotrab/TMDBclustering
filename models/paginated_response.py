from typing import List

from marshmallow import EXCLUDE, Schema, fields, post_load

from models.review import Review, ReviewSchema


class PaginatedResponse:
    def __init__(self, page: int, total_pages: int, total_results: int) -> None:
        self.page = page
        self.total_pages = total_pages
        self.total_results = total_results

class ReviewsPaginatedResponse(PaginatedResponse):
    def __init__(self, results: List[Review], page: int, total_pages: int, total_results: int) -> None:
        super().__init__(page, total_pages, total_results)
        self.results = results

class ReviewsPaginatedResponseSchema(Schema):
    results = fields.Nested(ReviewSchema, many=True)
    page = fields.Integer()
    total_pages = fields.Integer()
    total_results = fields.Integer()

    #Exclude the unknown JSON fields from the deserialization
    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_custom_object(self, data, **kwargs):
        return ReviewsPaginatedResponse(**data)
