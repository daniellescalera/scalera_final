import re
from datetime import datetime
from typing import List, Optional, Dict
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator, conint
from fastapi import Request

# Pagination Model
class Pagination(BaseModel):
    page: int = Field(..., description="Current page number.")
    per_page: int = Field(..., description="Number of items per page.")
    total_items: int = Field(..., description="Total number of items.")
    total_pages: int = Field(..., description="Total number of pages.")

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "per_page": 10,
                "total_items": 50,
                "total_pages": 5
            }
        }

class PaginationLink(BaseModel):
    rel: str
    href: HttpUrl
    method: str = "GET"

class EnhancedPagination(Pagination):
    links: List[PaginationLink] = []

    def add_link(self, rel: str, href: str):
        self.links.append(PaginationLink(rel=rel, href=href))

# Correct: generate_pagination_links at the top level (NOT inside a class)
def generate_pagination_links(request: Request, skip: int, limit: int, total: int) -> Dict[str, str]:
    """Generate pagination links for list endpoints."""
    base_url = str(request.url).split("?")[0]
    links = {}

    # Next page
    if skip + limit < total:
        next_skip = skip + limit
        links["next"] = f"{base_url}?skip={next_skip}&limit={limit}"

    # Previous page
    if skip > 0:
        prev_skip = max(0, skip - limit)
        links["previous"] = f"{base_url}?skip={prev_skip}&limit={limit}"

    return links
