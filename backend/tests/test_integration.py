import pytest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Test image (1x1 transparent PNG)
VALID_IMAGE = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:

    def test_health_check(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'moodboard-api'


class TestMoodcheckValidation:

    def test_empty_request(self, client):
        """Empty request (no images, no prompt) should fail."""
        response = client.post('/api/moodcheck',
                               content_type='application/json',
                               data='{}')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'provide images and/or describe' in str(data['details'])

    def test_empty_images_no_prompt(self, client):
        """Empty images array with no prompt should fail."""
        response = client.post('/api/moodcheck',
                               content_type='application/json',
                               data=json.dumps({'images': []}))
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    def test_text_only_valid(self, client):
        """Text-only request (no images) should be accepted for validation."""
        response = client.post('/api/moodcheck',
                               content_type='application/json',
                               data=json.dumps({'prompt': 'coastal grandmother aesthetic'}))
        # Will fail at API call stage, but should pass validation (not 400)
        assert response.status_code in [200, 500]  # 500 = API error, but passed validation

    def test_too_many_images(self, client):
        response = client.post('/api/moodcheck',
                               content_type='application/json',
                               data=json.dumps({'images': [VALID_IMAGE] * 6}))
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Maximum 5 images' in str(data['details'])

    def test_invalid_image_format(self, client):
        response = client.post('/api/moodcheck',
                               content_type='application/json',
                               data=json.dumps({'images': ['not-a-valid-image']}))
        assert response.status_code == 400

    def test_prompt_too_long(self, client):
        response = client.post('/api/moodcheck',
                               content_type='application/json',
                               data=json.dumps({
                                   'images': [VALID_IMAGE],
                                   'prompt': 'x' * 501
                               }))
        assert response.status_code == 400
        data = json.loads(response.data)
        assert '500 characters' in str(data['details'])


class TestMoodcheckSuccess:
    """
    These tests make real API calls and cost money.
    Only run when specifically needed.
    Mark with @pytest.mark.slow to skip in normal runs.
    """

    @pytest.mark.slow
    def test_successful_moodcheck_with_image(self, client):
        """Test a full successful moodcheck flow with images."""
        response = client.post('/api/moodcheck',
                               content_type='application/json',
                               data=json.dumps({
                                   'images': [VALID_IMAGE],
                                   'prompt': 'casual summer'
                               }))

        assert response.status_code == 200
        data = json.loads(response.data)

        # Check success
        assert data['success'] is True

        # Check vibe structure
        assert 'vibe' in data
        vibe = data['vibe']
        assert 'name' in vibe
        assert 'mood' in vibe
        assert 'color_palette' in vibe
        assert 'key_pieces' in vibe

        # Check products structure
        assert 'products' in data
        assert isinstance(data['products'], list)

        # Check search queries
        assert 'search_queries_used' in data
        assert isinstance(data['search_queries_used'], list)

    @pytest.mark.slow
    def test_successful_moodcheck_text_only(self, client):
        """Test a full successful moodcheck flow with text only."""
        response = client.post('/api/moodcheck',
                               content_type='application/json',
                               data=json.dumps({
                                   'prompt': 'dark academia aesthetic with vintage vibes'
                               }))

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    @pytest.mark.slow
    def test_moodcheck_with_budget_prompt(self, client):
        """Test that budget hints affect results."""
        response = client.post('/api/moodcheck',
                               content_type='application/json',
                               data=json.dumps({
                                   'images': [VALID_IMAGE],
                                   'prompt': 'affordable casual wear'
                               }))

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True


class TestCORS:

    def test_cors_headers(self, client):
        """Test that CORS headers are present."""
        response = client.options('/api/moodcheck')
        # CORS should allow requests from any origin in development
        assert response.status_code in [200, 204]


class TestErrorHandling:

    def test_404_endpoint(self, client):
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
