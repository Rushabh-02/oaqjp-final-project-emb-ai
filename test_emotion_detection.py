import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Unit tests for the emotion detector."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_dominant_anger(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "emotionPredictions": [
                {
                    "emotion": {
                        "anger": 0.8,
                        "disgust": 0.1,
                        "fear": 0.05,
                        "joy": 0.02,
                        "sadness": 0.03,
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        result = emotion_detector("I am very angry")

        self.assertEqual(result["dominant_emotion"], "anger")
        self.assertEqual(result["anger"], 0.8)
        self.assertEqual(result["disgust"], 0.1)
        self.assertEqual(result["fear"], 0.05)
        self.assertEqual(result["joy"], 0.02)
        self.assertEqual(result["sadness"], 0.03)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_bad_request_returns_none(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        result = emotion_detector("")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()