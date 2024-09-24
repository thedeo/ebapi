import unittest
from pydantic import ValidationError
from app.db.models.response import DynamicResponse  # Adjust the import based on your project structure


class TestDynamicResponse(unittest.TestCase):

    def test_valid_dynamic_response(self):
        # Create a valid DynamicResponse object with required fields
        response = DynamicResponse(id='123', name='Test Item', extra_field='extra_value')

        # Assertions for required fields
        self.assertEqual(response.id, '123')
        self.assertEqual(response.name, 'Test Item')

        # Assertions for extra fields
        self.assertEqual(response.extra_field, 'extra_value')

    def test_missing_required_fields(self):
        # Test missing required fields (should raise ValidationError)
        with self.assertRaises(ValidationError) as context:
            DynamicResponse(id='123')  # Missing 'name'
        
        self.assertIn('field required', str(context.exception))

    def test_missing_field(self):
        # Test missing required field (should raise ValidationError)
        with self.assertRaises(ValidationError) as context:
            DynamicResponse(id=None, name='Test Item')  # This should raise an error

        self.assertIn('none is not an allowed value', str(context.exception))

    def test_extra_fields(self):
        # Create a DynamicResponse object with extra fields only
        response = DynamicResponse(id='456', name='Another Item', additional_info='some info', tags=['tag1', 'tag2'])

        # Assertions for required fields
        self.assertEqual(response.id, '456')
        self.assertEqual(response.name, 'Another Item')

        # Assertions for extra fields
        self.assertEqual(response.additional_info, 'some info')
        self.assertEqual(response.tags, ['tag1', 'tag2'])


if __name__ == '__main__':
    unittest.main()
