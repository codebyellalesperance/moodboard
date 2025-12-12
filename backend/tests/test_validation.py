import pytest
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validation import validate_moodcheck_request, validate_image, extract_image_data

# A tiny valid PNG image in base64 (1x1 transparent pixel)
VALID_IMAGE = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

class TestValidateMoodcheckRequest:

    def test_valid_request_single_image(self):
        data = {"images": [VALID_IMAGE], "prompt": ""}
        is_valid, errors = validate_moodcheck_request(data)
        assert is_valid is True
        assert errors == []

    def test_valid_request_multiple_images(self):
        data = {"images": [VALID_IMAGE, VALID_IMAGE, VALID_IMAGE], "prompt": "casual summer vibe"}
        is_valid, errors = validate_moodcheck_request(data)
        assert is_valid is True
        assert errors == []

    def test_valid_request_max_images(self):
        data = {"images": [VALID_IMAGE] * 5, "prompt": ""}
        is_valid, errors = validate_moodcheck_request(data)
        assert is_valid is True
        assert errors == []

    def test_missing_images_field(self):
        data = {"prompt": "test"}
        is_valid, errors = validate_moodcheck_request(data)
        assert is_valid is False
        assert "'images' field is required" in errors

    def test_empty_images_array(self):
        data = {"images": []}
        is_valid, errors = validate_moodcheck_request(data)
        assert is_valid is False
        assert "At least one image is required" in errors

    def test_too_many_images(self):
        data = {"images": [VALID_IMAGE] * 6}
        is_valid, errors = validate_moodcheck_request(data)
        assert is_valid is False
        assert "Maximum 5 images allowed" in errors

    def test_prompt_too_long(self):
        data = {"images": [VALID_IMAGE], "prompt": "x" * 201}
        is_valid, errors = validate_moodcheck_request(data)
        assert is_valid is False
        assert "Prompt must be 200 characters or less" in errors

    def test_prompt_at_limit(self):
        data = {"images": [VALID_IMAGE], "prompt": "x" * 200}
        is_valid, errors = validate_moodcheck_request(data)
        assert is_valid is True

    def test_empty_body(self):
        is_valid, errors = validate_moodcheck_request(None)
        assert is_valid is False
        assert "Request body is required" in errors

    def test_images_not_array(self):
        data = {"images": "not an array"}
        is_valid, errors = validate_moodcheck_request(data)
        assert is_valid is False
        assert "'images' must be an array" in errors


class TestValidateImage:

    def test_valid_png(self):
        errors = validate_image(VALID_IMAGE, 1)
        assert errors == []

    def test_valid_jpeg(self):
        jpeg_image = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="
        errors = validate_image(jpeg_image, 1)
        assert errors == []

    def test_invalid_not_string(self):
        errors = validate_image(12345, 1)
        assert "Image 1 must be a string" in errors

    def test_invalid_not_data_uri(self):
        errors = validate_image("not a data uri", 1)
        assert any("must be a valid data URI" in e for e in errors)

    def test_invalid_format(self):
        errors = validate_image("data:image/gif;base64,R0lGODlh", 1)
        assert "Image 1 must be JPEG, PNG, or WEBP format" in errors

    def test_invalid_base64(self):
        errors = validate_image("data:image/png;base64,not-valid-base64!!!", 1)
        assert "Image 1 has invalid base64 encoding" in errors


class TestExtractImageData:

    def test_extract_png(self):
        media_type, data = extract_image_data(VALID_IMAGE)
        assert media_type == "image/png"
        assert data.startswith("iVBORw0KGgo")

    def test_extract_jpeg(self):
        jpeg = "data:image/jpeg;base64,/9j/4AAQ"
        media_type, data = extract_image_data(jpeg)
        assert media_type == "image/jpeg"
        assert data == "/9j/4AAQ"
