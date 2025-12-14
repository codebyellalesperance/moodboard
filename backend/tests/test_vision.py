import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.vision import clean_json_response, MOOD_EXTRACTION_PROMPT_WITH_IMAGES, MOOD_EXTRACTION_PROMPT_TEXT_ONLY

class TestCleanJsonResponse:

    def test_clean_plain_json(self):
        input_text = '{"name": "Test"}'
        result = clean_json_response(input_text)
        assert result == '{"name": "Test"}'

    def test_clean_json_with_markdown(self):
        input_text = '```json\n{"name": "Test"}\n```'
        result = clean_json_response(input_text)
        assert result == '{"name": "Test"}'

    def test_clean_json_with_plain_markdown(self):
        input_text = '```\n{"name": "Test"}\n```'
        result = clean_json_response(input_text)
        assert result == '{"name": "Test"}'

    def test_clean_json_with_whitespace(self):
        input_text = '  \n{"name": "Test"}\n  '
        result = clean_json_response(input_text)
        assert result == '{"name": "Test"}'


class TestMoodExtractionPrompt:

    def test_prompt_with_images_has_required_fields(self):
        """Verify the image prompt asks for all required fields."""
        required = ['name', 'mood', 'color_palette', 'textures', 'key_pieces', 'avoid', 'search_queries']
        for field in required:
            assert field in MOOD_EXTRACTION_PROMPT_WITH_IMAGES, f"Image prompt missing field: {field}"

    def test_prompt_text_only_has_required_fields(self):
        """Verify the text-only prompt asks for all required fields."""
        required = ['name', 'mood', 'color_palette', 'textures', 'key_pieces', 'avoid', 'search_queries']
        for field in required:
            assert field in MOOD_EXTRACTION_PROMPT_TEXT_ONLY, f"Text-only prompt missing field: {field}"

    def test_prompts_have_user_prompt_placeholder(self):
        """Verify both prompts have a placeholder for user input."""
        assert '{user_prompt}' in MOOD_EXTRACTION_PROMPT_WITH_IMAGES
        assert '{user_prompt}' in MOOD_EXTRACTION_PROMPT_TEXT_ONLY
