from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import router


app = FastAPI(
    title="ComicCraft",
    description="AI Comic Story Creator using Gemini",
    version="1.0.0"
)


templates = Jinja2Templates(directory="templates")


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.include_router(router)
app.state.templates=templates


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )