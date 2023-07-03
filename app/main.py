from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import List, Optional, Union
from dataclasses import dataclass
from pydantic import BaseModel

from pathlib import Path
import json

# config related classes

@dataclass
class Arg:
    name: str
    type: str
    value: str


@dataclass
class Template:
    name: str
    installs: str
    imports: str
    template: str


@dataclass
class Option:
    name: str
    args: List[Arg]
    templates: List[Template]


@dataclass
class Section:
    name: str
    tag: str
    path: str
    options: List[Option]


@dataclass
class LangChainConfig:
    sections: List[Section]


class Loader:
    json_path: str

    def __init__(self, path: Union[str, Path]) -> None:
        self.json_path = path

    def load(self):
        with open(self.json_path, 'r') as f:
            data = json.load(f)
            config = LangChainConfig(**data)

            config.sections = [
                Section(
                    d['name'],
                    d['tag'],
                    d['path'],
                    [
                        Option(
                            o['name'],
                            [
                                Arg(**a) for a in o['args']
                            ] if 'args' in o.keys() else None,
                            [
                                Template(**t) for t in o['templates']
                            ] if 'templates' in o.keys() else None
                        ) for o in d['options']
                    ]
                ) for d in data['sections']
            ]

            return config

# element related classes

@dataclass
class Argument:
    name: str
    value: str


@dataclass
class Element:
    type: str
    name: str
    arguments: Optional[list[Argument]]
    index: int


class ElementsRequest(BaseModel):
    elements: list[Element]


# generator related classes

class LangChainGenerator:
    config: LangChainConfig

    def __init__(self, config: LangChainConfig) -> None:
        self.config = config

    def Generate(self, elements: list[Element]) -> list[str]:
        installs = []
        imports = []
        items = []
        for element in elements:
            section = next(
                (section for section in self.config.sections if section.tag == element.type), None)
            if section != None:
                option = next(
                    (option for option in section.options if option.name == element.name), None)
                if option != None and len(option.templates) > 0:
                    install_list = [template.installs for template in option.templates if template.name == 'default' and len(
                        template.installs) > 0]
                    if len(install_list) > 0:
                        installs.append('#' + install_list[0])

                    import_list = [template.imports for template in option.templates if template.name == 'default' and len(
                        template.imports) > 0]
                    if len(import_list) > 0:
                        imports.append(import_list[0])

                    template_list = [template.template for template in option.templates if template.name == 'default' and len(
                        template.template) > 0]
                    if len(template_list) > 0:
                        for template_line in template_list[0].split('\n'):
                            if len(template_line.strip(' ')) > 0:
                                items.append(template_line)

        for element in elements:
            items = [item.replace(
                f'{{{element.type.lower()}}}', element.name) for item in items]

            for argument in element.arguments:
                items = [item.replace(
                    f'{{{argument.name.lower()}}}', argument.value) for item in items]

        return installs + [''] + imports + [''] + items


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
