"""Tests for request validation."""

import pytest
from utils.validation import validate_moodcheck_request, validate_image

# Small valid base64 PNG (1x1 transparent pixel)
VALID_PNG = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='


class TestValidateMoodcheckRequest:
    """Tests for validate_moodcheck_request function."""

    def test_valid_request(self):
        """Valid request should return None."""
        data = {'images': [VALID_PNG], 'prompt': 'casual summer'}
        assert validate_moodcheck_request(data) is None

    def test_valid_request_no_prompt(self):
        """Request without prompt should be valid."""
        data = {'images': [VALID_PNG]}
        assert validate_moodcheck_request(data) is None

    def test_empty_body(self):
        """Empty body should return error."""
        errors = validate_moodcheck_request({})
        assert errors is not None
        assert any('image' in e.lower() for e in errors)

    def test_no_images(self):
        """Missing images should return error."""
        errors = validate_moodcheck_request({'prompt': 'test'})
        assert errors is not None
        assert any('image' in e.lower() for e in errors)

    def test_too_many_images(self):
        """More than 5 images should return error."""
        data = {'images': [VALID_PNG] * 6}
        errors = validate_moodcheck_request(data)
        assert errors is not None
        assert any('5' in e for e in errors)

    def test_prompt_too_long(self):
        """Prompt over 200 chars should return error."""
        data = {'images': [VALID_PNG], 'prompt': 'x' * 201}
        errors = validate_moodcheck_request(data)
        assert errors is not None
        assert any('200' in e for e in errors)


class TestValidateImage:
    """Tests for validate_image function."""

    def test_valid_png(self):
        """Valid PNG should return no errors."""
        errors = validate_image(VALID_PNG, 0)
        assert errors == []

    def test_invalid_format(self):
        """Non-data-URI should return error."""
        errors = validate_image('not a data uri', 0)
        assert len(errors) > 0

    def test_unsupported_type(self):
        """Unsupported MIME type should return error."""
        gif = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
        errors = validate_image(gif, 0)
        assert any('unsupported' in e.lower() for e in errors)
