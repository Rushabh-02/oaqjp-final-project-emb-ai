
import requests


def emotion_detector(text_to_analyze):
    """Analyze text and return emotion scores and dominant emotion."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )

    headers = {
        "grpc-metadata-mm-model-id":
            "emotion_aggregated-workflow_lang_en_stock"
    }

    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 400:
            return None

        response.raise_for_status()
        result = response.json()

        emotions = result["emotionPredictions"][0]["emotion"]
        dominant_emotion = max(emotions, key=emotions.get)

        emotions["dominant_emotion"] = dominant_emotion
        return emotions

    except requests.RequestException as error:
        print(f"Emotion detection request failed: {error}")
        return None
    except (KeyError, IndexError, TypeError) as error:
        print(f"Unexpected response format: {error}")
        return None
