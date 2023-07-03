import argparse
import uvicorn
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

generator = langchain_generator.LangChainGenerator({})


@app.post("/api/build-app")
async def build_app(request: langchain_model.ElementsRequest):
    return {
        'lines': generator.Generate(request.elements)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LangChain applications API')
    parser.add_argument('--config', '-c', type=str,
                        default='./langchain-config.json')
    parser.add_argument('--http_host', default='0.0.0.0')
    parser.add_argument('--http_port', type=int, default=8888)
    args = parser.parse_args()

    langConfig = langchain_config.Loader(args.config).load()
    generator = langchain_generator.LangChainGenerator(langConfig)

    config = uvicorn.Config(app, host=args.http_host, port=args.http_port)
    server = uvicorn.Server(config=config)
    server.run()
