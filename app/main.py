from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import langchain_model
import langchain_config
import langchain_generator


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

langConfig = langchain_config.Loader("langchain-config.json").load()
generator = langchain_generator.LangChainGenerator(langConfig)

@app.post("/api/build-app")
async def build_app(request: langchain_model.ElementsRequest):
    return {
        'lines': generator.Generate(request.elements)
    }
