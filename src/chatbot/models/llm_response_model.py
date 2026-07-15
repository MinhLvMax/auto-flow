from typing import get_args, get_origin
from pydantic import BaseModel
import json


class LLMResponseModel(BaseModel):

    @classmethod
    def llm_schema(cls):
        template, rules = cls._build_schema(cls)

        return f"""
Output format:

{json.dumps(template, indent=2, ensure_ascii=False)}

Field rules:
{chr(10).join(rules)}
"""

    @classmethod
    def _build_schema(cls, model: type[BaseModel], prefix=""):
        template = {}
        rules = []

        for name, field in model.model_fields.items():
            path = f"{prefix}{name}"
            field_type = field.annotation
            origin = get_origin(field_type)

            # list[T]
            if origin is list:
                item_type = get_args(field_type)[0]

                if (
                        isinstance(item_type, type)
                        and issubclass(item_type, BaseModel)
                ):
                    child_template, child_rules = cls._build_schema(
                        item_type,
                        prefix=f"{path}[]."
                    )

                    template[name] = [child_template]
                    rules.extend(child_rules)

                else:
                    template[name] = ["string"]

                    if field.description:
                        rules.append(
                            f"- {path}: {field.description}"
                        )

            # nested object
            elif (
                    isinstance(field_type, type)
                    and issubclass(field_type, BaseModel)
            ):
                child_template, child_rules = cls._build_schema(
                    field_type,
                    prefix=f"{path}."
                )

                template[name] = child_template
                rules.extend(child_rules)

            # primitive
            else:
                template[name] = "string"

                if field.description:
                    rules.append(
                        f"- {path}: {field.description}"
                    )

        return template, rules
