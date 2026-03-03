import json
import logging

from app.modules.content.prompt import (
    DRAFT_SYSTEM_PROMPT,
    OUTLINE_SYSTEM_PROMPT,
    PUBLISH_SYSTEM_PROMPT,
    SEO_SYSTEM_PROMPT,
)
from app.modules.content.schema import ContentOutline, PublishedPost, SEOData
from app.utils.openai import open_ai_client
from app.utils.tavily import tavily_client

logger = logging.getLogger(__name__)


def research_topic(topic: str) -> str:
    """Search the web and summarize findings for the topic."""

    logger.info(f"Researching topic: {topic}")

    search_result = tavily_client.search(
        query=topic,
        search_depth="advanced",
        num_results=5,
        include_raw_content="markdown",
    )

    response = open_ai_client.chat.completions.create(
        model="qwen/qwen3.5-flash-02-23",
        messages=[
            {
                "role": "system",
                "content": "Summarize these search results into rich research context. Include key facts, stats, dates, and source URLs.",
            },
            {
                "role": "user",
                "content": f"Topic: {topic}\n\nSearch Results:\n{json.dumps(search_result)}",
            },
        ],
    )

    research_context = response.choices[0].message.content

    if not research_context:
        raise ValueError("Invalid response from OpenAI API")

    logger.info(f"Research context for topic '{topic}': {research_context}")

    return research_context


def generate_outline(topic: str, research_context: str):
    """Generate a detailed outline for the topic based on the research context."""

    logger.info(f"Generating outline for topic: {topic}")

    response = open_ai_client.chat.completions.parse(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": OUTLINE_SYSTEM_PROMPT.format(
                    research_context=research_context
                ),
            },
            {
                "role": "user",
                "content": f"Topic: {topic}\n\nResearch Context:\n{research_context}",
            },
        ],
        response_format=ContentOutline,
    )

    outline = response.choices[0].message.parsed

    if not outline:
        raise ValueError("Invalid response from OpenAI API")

    logger.info(f"Generated outline for topic '{topic}': {outline}")

    return outline


def write_draft(outline: ContentOutline) -> str:
    """Write a full blog post draft based on the outline."""

    logger.info("Writing draft based on outline")

    response = open_ai_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": DRAFT_SYSTEM_PROMPT.format(
                    outline=outline.model_dump_json(indent=2)
                ),
            },
            {
                "role": "user",
                "content": f"Write the full blog post for: {outline.title}",
            },
        ],
    )

    draft = response.choices[0].message.content

    if not draft:
        raise ValueError("Invalid response from OpenAI API")

    logger.info("Draft written successfully")

    return draft


def seo_optimize(draft: str) -> SEOData:
    """Optimize the draft for SEO."""

    logger.info("Running SEO optimization...")

    response = open_ai_client.beta.chat.completions.parse(
        model="openai/gpt-4o",
        messages=[
            {
                "role": "system",
                "content": SEO_SYSTEM_PROMPT,
            },
            {"role": "user", "content": f"Optimize this blog post:\n\n{draft}"},
        ],
        response_format=SEOData,
    )

    seo = response.choices[0].message.parsed

    if not seo:
        raise ValueError("Invalid response from OpenAI API")

    logger.info(f"SEO done — keyword: '{seo.primary_keyword}', slug: '{seo.slug}'")
    return seo


def publish_post(seo: SEOData) -> PublishedPost:
    """Format the SEO-optimized post into publish-ready HTML."""

    logger.info("Formatting for publishing...")

    response = open_ai_client.beta.chat.completions.parse(
        model="openai/gpt-4o",
        messages=[
            {
                "role": "system",
                "content": PUBLISH_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    f"Title: {seo.seo_title}\n"
                    f"Slug: {seo.slug}\n"
                    f"Meta: {seo.meta_description}\n"
                    f"Primary Keyword: {seo.primary_keyword}\n"
                    f"Secondary Keywords: {', '.join(seo.secondary_keywords)}\n\n"
                    f"Content:\n{seo.optimized_content}"
                ),
            },
        ],
        response_format=PublishedPost,
    )

    post = response.choices[0].message.parsed

    if not post:
        raise ValueError("Invalid response from OpenAI API")

    logger.info(
        f"Published — {post.word_count} words, ~{post.reading_time_minutes} min read"
    )
    return post
