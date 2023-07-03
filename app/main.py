from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .model import langchain_model
from .config import langchain_config
from .generator import langchain_generator

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

langConfig = langchain_config.Loader("app/config.json").load()
generator = langchain_generator.LangChainGenerator(langConfig)

@app.post("/api/build-app")
async def build_app(request: langchain_model.ElementsRequest):
    return {
        'lines': generator.Generate(request.elements)
    }
