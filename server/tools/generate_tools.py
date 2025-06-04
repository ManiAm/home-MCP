
import sys
import re
import inspect
import logging
from typing import Any, Optional
from pydantic import BaseModel, create_model
from langchain.tools import StructuredTool

log = logging.getLogger(__name__)


class EmptyInput(BaseModel):
    """Used for methods with no parameters"""
    pass


def normalize_tool_name(name: str) -> str:
    """Convert method name to OpenAI-compatible function name."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)


def make_wrapper_noarg(method, name: str):

    def wrapper(_: Any = None):

        log.info("[TOOL CALL] %s()", name)

        try:

            status, output = method()
            if not status:
                log.error("[TOOL ERROR] %s: %s", name, output)
                return f"Tool {name} failed: {str(output)}"

            log.debug("[TOOL RESULT] %s", output)
            return str(output)

        except Exception as e:

            log.error(f"[TOOL ERROR] {name}: {str(e)}")
            return f"Tool {name} failed: {str(e)}"

    return wrapper


def make_wrapper(method, name: str):

    def wrapper(**kwargs):

        log.info("[TOOL CALL] %s(%s)", name, kwargs)

        try:

            status, output = method(**kwargs)
            if not status:
                log.error("[TOOL ERROR] %s: %s", name, output)
                return f"Tool {name} failed: {str(output)}"

            log.debug("[TOOL RESULT] %s", output)
            return str(output)

        except Exception as e:

            log.error("[TOOL ERROR] %s: %s", name, str(e))
            return f"Tool {name} failed: {str(e)}"

    return wrapper


def generate_tools_from_client(client_instance):

    if not isinstance(client_instance, list):
        log.error("client_instance is not of type list")
        sys.exit(1)

    members_all = []
    for instance in client_instance:
        members = inspect.getmembers(instance, predicate=inspect.ismethod)
        members_all.extend(members)

    tools = []

    for name, method in members_all:

        if name.startswith("_") or not getattr(method, "_include_as_tool", False):
            continue

        sig = inspect.signature(method)
        params = sig.parameters
        description = inspect.getdoc(method) or "No description provided."

        if len(params) == 0:
            args_schema = EmptyInput
            func_wrapper = make_wrapper_noarg(method, name)
        else:
            fields = {}
            for param in params.values():
                annotation = param.annotation if param.annotation != inspect._empty else str
                default = param.default if param.default != inspect._empty else ...

                # Force all non-required params to Optional
                if default is None:
                    annotation = Optional[annotation]

                fields[param.name] = (annotation, default)

            args_schema = create_model(f"{name.title()}Input", **fields)
            func_wrapper = make_wrapper(method, name)

        tool = StructuredTool.from_function(
            name=normalize_tool_name(name),
            description=description,
            func=func_wrapper,
            args_schema=args_schema
        )

        tools.append(tool)

    return tools
