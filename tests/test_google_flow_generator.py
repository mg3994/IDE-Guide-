import pytest
from src.ide_guide.catalog import DEFAULT_IDE_CATALOG
from src.ide_guide.google_flow_generator import generate_google_flow_video_spec, DISCLAIMER_TEXT

def test_google_flow_generator_shorts():
    sample_ide = DEFAULT_IDE_CATALOG[0]
    spec = generate_google_flow_video_spec(sample_ide, format_type="shorts")

    assert f"# Google Flow Video Specification: {sample_ide['name']}" in spec
    assert "9:16" in spec
    assert "YouTube ([@IDEguide]" in spec
    assert "Google Flow Visual Prompt" in spec
    assert "Camera Movement" in spec
    assert "Voiceover Script" in spec
    assert DISCLAIMER_TEXT in spec

def test_google_flow_generator_longform():
    sample_ide = DEFAULT_IDE_CATALOG[1]
    spec = generate_google_flow_video_spec(sample_ide, format_type="longform")

    assert "16:9" in spec
    assert DISCLAIMER_TEXT in spec
