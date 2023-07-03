from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .langchain_model import ElementsRequest
from .langchain_config import Loader
from .langchain_generator import LangChainGenerator

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

langConfig = Loader("app/config.json").load()
generator = LangChainGenerator(langConfig)

@app.post("/api/build-app")
async def build_app(request: ElementsRequest):
    return {
        'lines': generator.Generate(request.elements)
    }
