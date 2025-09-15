import importlib
from pathlib import Path
import sys
from typing import TYPE_CHECKING
from fastapi.routing import APIRouter
import os

if TYPE_CHECKING:  # pragma: no cover
    from fastapi import FastAPI

__all__ = ["load_fs_router"]


def _change_seg(seg: str):
    res = f"{{{seg[1:-1]}}}" if seg.startswith("[") and seg.endswith("]") else seg
    return res if res.startswith("{") and res.endswith("}") else res.replace("_", "-")


def _get_api_prefix(route_dir: Path, prefix: str, f: Path):
    result_prefix = prefix
    prefix_by_path = f.relative_to(route_dir).as_posix()
    if prefix_by_path.startswith("."):
        prefix_by_path = prefix_by_path[1:]
    if result_prefix:
        if result_prefix.endswith("/"):
            result_prefix = result_prefix[:-1]
        result_prefix = (
            f"{result_prefix}/{prefix_by_path}" if prefix_by_path else result_prefix
        )
    elif prefix_by_path:
        result_prefix = (
            prefix_by_path if prefix_by_path.startswith("/") else f"/{prefix_by_path}"
        )

    if result_prefix:
        result_prefix = "/".join([
            _change_seg(p)
            for p in result_prefix.split("/")
            if not p.startswith("(") and not p.endswith(")")
        ])
        if not result_prefix.startswith("/"):
            result_prefix = f"/{result_prefix}"

    return result_prefix


def load_fs_router(
    app: "FastAPI", route_dir: Path | str = "routers", *, prefix: str = ""
):
    route_dir = Path(route_dir)
    if not route_dir.exists():
        return
    collected_apis = []
    python_root = Path(sys.path[0]).resolve()
    cwd = Path(os.getcwd())

    normalized_dir = (cwd / route_dir).relative_to(python_root)
    for root, _, files in os.walk(route_dir):
        root = cwd / root
        for f in files:
            if not f.endswith(".py"):
                continue
            f = f[: -len("__init__.py" if f.endswith("__init__.py") else ".py")]
            module_path = (root / f).relative_to(python_root)
            api_prefix = _get_api_prefix(normalized_dir, prefix, module_path)
            module = importlib.import_module(module_path.as_posix().replace("/", "."))

            for attr in dir(module):
                if attr.startswith("__"):
                    continue
                router = getattr(module, attr)
                if not isinstance(router, APIRouter) or router in collected_apis:
                    continue
                collected_apis.append(router)
                app.include_router(router, prefix=api_prefix)
