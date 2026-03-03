from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.modules.content.schema import ContentInput
from app.modules.content.tasks import create_content_task

app = FastAPI()


@app.post("/content")
def do_research(body: ContentInput):
    create_content_task.delay(body.topic)

    return {"message": "Processing!"}


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
