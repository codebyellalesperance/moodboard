import base64
import re

def validate_moodcheck_request(data):
    """
    Validate the moodcheck request data.

    Args:
        data: Request JSON data

    Returns:
        tuple: (is_valid: bool, errors: list)
    """
    errors = []

    # Check data exists
    if data is None:
        return False, ["Request body is required"]

    # Check images exist
    if 'images' not in data:
        errors.append("'images' field is required")
        return False, errors

    images = data.get('images', [])

    # Check images is a list
    if not isinstance(images, list):
        errors.append("'images' must be an array")
        return False, errors

    # Check image count
    if len(images) == 0:
        errors.append("At least one image is required")

    if len(images) > 5:
        errors.append("Maximum 5 images allowed")

    # Validate each image
    for i, img in enumerate(images):
        img_errors = validate_image(img, i + 1)
        errors.extend(img_errors)

    # Validate prompt if provided
    prompt = data.get('prompt', '')
    if prompt and len(prompt) > 200:
        errors.append("Prompt must be 200 characters or less")

    return len(errors) == 0, errors


def validate_image(image_data, index):
    """
    Validate a single base64 image.

    Args:
        image_data: Base64 encoded image string
        index: Image number (for error messages)

    Returns:
        list: List of error messages (empty if valid)
    """
    errors = []

    # Check it's a string
    if not isinstance(image_data, str):
        errors.append(f"Image {index} must be a string")
        return errors

    # Check data URI format
    if not image_data.startswith('data:image/'):
        errors.append(f"Image {index} must be a valid data URI (data:image/...)")
        return errors

    # Check supported formats
    valid_formats = ['data:image/jpeg', 'data:image/png', 'data:image/webp', 'data:image/jpg']
    if not any(image_data.startswith(fmt) for fmt in valid_formats):
        errors.append(f"Image {index} must be JPEG, PNG, or WEBP format")
        return errors

    # Extract base64 data
    try:
        # Format is: data:image/jpeg;base64,/9j/4AAQ...
        if ';base64,' not in image_data:
            errors.append(f"Image {index} must be base64 encoded")
            return errors

        base64_data = image_data.split(';base64,')[1]

        # Check size (base64 is ~33% larger than binary)
        estimated_size = len(base64_data) * 0.75
        max_size = 5 * 1024 * 1024  # 5MB

        if estimated_size > max_size:
            errors.append(f"Image {index} exceeds 5MB limit")

        # Verify it's valid base64
        base64.b64decode(base64_data)

    except Exception as e:
        errors.append(f"Image {index} has invalid base64 encoding")

    return errors


def extract_image_data(image_uri):
    """
    Extract media type and base64 data from a data URI.

    Args:
        image_uri: Full data URI string

    Returns:
        tuple: (media_type, base64_data)
    """
    # data:image/jpeg;base64,/9j/4AAQ...
    header, base64_data = image_uri.split(';base64,')
    media_type = header.replace('data:', '')
    return media_type, base64_data
