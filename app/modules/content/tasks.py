from markdown import markdown
from weasyprint import HTML

from app.celery_app import celery_app
from app.modules.content.method import (
    generate_outline,
    publish_post,
    research_topic,
    seo_optimize,
    write_draft,
)


def create_content(topic: str):
    research_context = research_topic(topic)
    outline = generate_outline(topic, research_context)
    draft = write_draft(outline)
    seo = seo_optimize(draft)
    post = publish_post(seo)

    result = markdown(text=post.markdown_content, output_format="html")
    HTML(string=result).write_pdf(f"{post.slug}.pdf")


@celery_app.task
def create_content_task(topic: str):
    create_content(topic)
