import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.vision import clean_json_response, MOOD_EXTRACTION_PROMPT

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

    def test_prompt_has_required_fields(self):
        """Verify the prompt asks for all required fields."""
        required = ['name', 'mood', 'color_palette', 'textures', 'key_pieces', 'avoid', 'search_queries']
        for field in required:
            assert field in MOOD_EXTRACTION_PROMPT, f"Prompt missing field: {field}"

    def test_prompt_has_user_prompt_placeholder(self):
        """Verify the prompt has a placeholder for user input."""
        assert '{user_prompt}' in MOOD_EXTRACTION_PROMPT
