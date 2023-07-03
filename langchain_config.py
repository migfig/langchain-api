from typing import List, Union
from dataclasses import dataclass
from pathlib import Path
import json


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
        pass

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
