import langchain_config
import langchain_model


class LangChainGenerator:
    config: langchain_config.LangChainConfig

    def __init__(self, config: langchain_config.LangChainConfig) -> None:
        self.config = config

    def Generate(self, elements: list[langchain_model.Element]) -> list[str]:
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
