#!/usr/bin/env python
# coding: utf-8

# In[3]:


from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Set your libretranslate url here.
LIBRETRANSLATE_URL = "https://libretranslate.de/translate"  # Public instance


@app.route("/translate", methods=["POST"])
def translate_text():
    try:
        data = request.get_json()
        text_to_translate = data.get("text")

        if not text_to_translate:
            return jsonify({"error": "Missing 'text' parameter"}), 400

        payload = {
            "q": text_to_translate,
            "source": "en",
            "target": "es"
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(LIBRETRANSLATE_URL, headers=headers,
                                 data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for non-200 status codes.

        translation_data = response.json()

        translated_text = translation_data["translatedText"]

        return jsonify({"translated_text": translated_text})

    except requests.exceptions.RequestException as e:
        print(f"Error during request to LibreTranslate: {e}")
        return jsonify({"error": "Translation request failed"}), 500
    except Exception as e:
        print(f"Error during translation: {e}")
        return jsonify({"error": "Translation failed"}), 500

# No changes in this part, Gunicorn will handle the app execution.


# In[ ]:




