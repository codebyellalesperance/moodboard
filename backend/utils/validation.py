"""Request validation utilities."""

import base64
import re
from config import Config

# Supported image MIME types
SUPPORTED_TYPES = {'image/jpeg', 'image/png', 'image/webp'}

# Data URI regex pattern
DATA_URI_PATTERN = re.compile(r'^data:([^;]+);base64,(.+)$')


def validate_moodcheck_request(data: dict) -> list[str] | None:
    """
    Validate the moodcheck request body.

    Args:
        data: Request JSON body

    Returns:
        List of error messages, or None if valid
    """
    errors = []

    if not data:
        return ['Request body is required']

    # Validate images
    images = data.get('images')

    if not images:
        errors.append('At least one image is required')
    elif not isinstance(images, list):
        errors.append('Images must be an array')
    elif len(images) > Config.MAX_IMAGES:
        errors.append(f'Maximum {Config.MAX_IMAGES} images allowed')
    else:
        for i, image in enumerate(images):
            image_errors = validate_image(image, i)
            errors.extend(image_errors)

    # Validate prompt
    prompt = data.get('prompt')
    if prompt is not None:
        if not isinstance(prompt, str):
            errors.append('Prompt must be a string')
        elif len(prompt) > Config.MAX_PROMPT_LENGTH:
            errors.append(f'Prompt must be {Config.MAX_PROMPT_LENGTH} characters or less')

    return errors if errors else None


def validate_image(image: str, index: int) -> list[str]:
    """Validate a single image data URI."""
    errors = []
    prefix = f'Image {index + 1}'

    if not isinstance(image, str):
        errors.append(f'{prefix}: must be a string')
        return errors

    # Parse data URI
    match = DATA_URI_PATTERN.match(image)
    if not match:
        errors.append(f'{prefix}: must be a valid base64 data URI')
        return errors

    mime_type, base64_data = match.groups()

    # Check MIME type
    if mime_type not in SUPPORTED_TYPES:
        errors.append(f'{prefix}: unsupported type {mime_type}. Use JPEG, PNG, or WEBP')

    # Check size
    try:
        decoded = base64.b64decode(base64_data)
        size_mb = len(decoded) / (1024 * 1024)
        if size_mb > Config.MAX_IMAGE_SIZE_MB:
            errors.append(f'{prefix}: exceeds {Config.MAX_IMAGE_SIZE_MB}MB limit')
    except Exception:
        errors.append(f'{prefix}: invalid base64 encoding')

    return errors
