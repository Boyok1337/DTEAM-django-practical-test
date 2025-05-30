import requests
from django.conf import settings
from core.constants import DEEPL_FREE_API_URL, DEEPL_PRO_API_URL


def translate_text(text: str, target_lang_code: str) -> dict:
    api_key = getattr(settings, 'DEEPL_API_KEY', None)
    if not api_key:
        return {"error": "DeepL API key not configured"}, 500

    api_key = api_key.strip()
    api_url = DEEPL_FREE_API_URL if api_key.endswith(':fx') else DEEPL_PRO_API_URL

    try:
        response = requests.post(
            api_url,
            data={
                "auth_key": api_key,
                "text": text,
                "target_lang": target_lang_code
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code == 403:
            return {
                "error": "DeepL API authentication failed. Check your API key and endpoint.",
                "details": response.text
            }, 403

        if response.status_code == 456:
            return {"error": "DeepL API quota exceeded"}, 429

        response.raise_for_status()
        result = response.json()

        if "translations" in result and result["translations"]:
            return {"translated_text": result["translations"][0]["text"]}, 200
        else:
            return {"error": "No translation returned"}, 500

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}, 500
