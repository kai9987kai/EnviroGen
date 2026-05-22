from __future__ import annotations

from pathlib import Path

import pytest

from envirogen import EnviroGenApp, Environment
from envirogen.resources import RESOURCE_CATALOG, resources_by_category


def test_resource_catalog_is_large_and_categorized() -> None:
    categories = resources_by_category()

    assert len(RESOURCE_CATALOG) >= 35
    assert {
        "ABM fundamentals",
        "Mesa",
        "NetLogo",
        "Artificial life",
        "Ecology simulation",
        "Experiments and optimization",
        "Visualization",
    } <= set(categories)


def test_resource_docs_include_all_in_app_urls() -> None:
    docs = Path("docs/resources.md").read_text(encoding="utf-8")

    for resource in RESOURCE_CATALOG:
        assert resource.url in docs


def test_tkinter_app_can_create_and_destroy_window_when_display_exists() -> None:
    app = EnviroGenApp(Environment(width=100, height=80, seed=5))
    try:
        app._ensure_ui()
    except Exception as exc:
        if exc.__class__.__name__ == "TclError":
            pytest.skip("Tkinter display is not available")
        raise

    assert app.canvas is not None
    app.env.add_bot(x=20, y=20)
    app.env.add_plant(x=30, y=30)
    app.env.add_obstacle(x=40, y=40, width=10, height=10)
    app.step_once()
    app.root.destroy()

