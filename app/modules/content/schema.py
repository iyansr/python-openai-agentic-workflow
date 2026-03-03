from pydantic import BaseModel


class OutlineSection(BaseModel):
    heading: str
    points: list[str]


class ContentOutline(BaseModel):
    title: str
    meta_description: str
    sections: list[OutlineSection]


class SEOData(BaseModel):
    seo_title: str
    meta_description: str
    slug: str
    primary_keyword: str
    secondary_keywords: list[str]
    optimized_content: str


class PublishedPost(BaseModel):
    title: str
    slug: str
    meta_description: str
    primary_keyword: str
    secondary_keywords: list[str]
    markdown_content: str
    word_count: int
    reading_time_minutes: int


class ContentInput(BaseModel):
    topic: str
