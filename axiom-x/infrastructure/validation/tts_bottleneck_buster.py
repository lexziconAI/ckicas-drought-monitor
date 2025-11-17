import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_google_tts_diagnostic():
    """Comprehensive Google TTS diagnostic"""
    print("🔍 GOOGLE TTS BOTTLENECK OPTIMIZATION BUSTER")
    print("=" * 60)

    # Check available keys
    gemini_key = os.getenv('GOOGLE_API_KEY')
    tts_key = os.getenv('GOOGLE_TTS_API_KEY')

    print(f"Gemini API Key: {'✅ Found' if gemini_key else '❌ Missing'}")
    print(f"TTS API Key: {'✅ Found' if tts_key else '❌ Missing'}")

    # Test 1: Current failing method
    print("\n🧪 TEST 1: Current method (API Key auth)")
    try:
        url = "https://texttospeech.googleapis.com/v1/text:synthesize"
        headers = {"X-Goog-Api-Key": gemini_key or tts_key, "Content-Type": "application/json"}
        payload = {
            "input": {"text": "test"},
            "voice": {"languageCode": "en-US", "name": "en-US-Neural2-A"},
            "audioConfig": {"audioEncoding": "MP3"}
        }

        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")

    # Test 2: Check if TTS API is enabled for the project
    print("\n🧪 TEST 2: Check API availability")
    try:
        # Try to list voices (this should work if API is enabled)
        url = "https://texttospeech.googleapis.com/v1/voices"
        headers = {"X-Goog-Api-Key": gemini_key or tts_key}
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Voices endpoint: {response.status_code}")
        if response.status_code == 200:
            voices = response.json()
            print(f"Available voices: {len(voices.get('voices', []))}")
        else:
            print(f"Error: {response.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")

    # Test 3: Alternative TTS services
    print("\n🧪 TEST 3: Alternative TTS services")

    # Test OpenAI TTS (if available)
    print("  - OpenAI TTS:")
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input="Hello world"
            )
            print("    ✅ OpenAI TTS working")
        except Exception as e:
            print(f"    ❌ OpenAI TTS failed: {str(e)[:100]}")
    else:
        print("    ⚠️  No OpenAI key")

    # Test ElevenLabs
    print("  - ElevenLabs:")
    eleven_key = os.getenv('ELEVENLABS_API_KEY')
    if eleven_key:
        try:
            url = "https://api.elevenlabs.io/v1/user"
            headers = {"xi-api-key": eleven_key}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print("    ✅ ElevenLabs working")
            else:
                print(f"    ❌ ElevenLabs error: {response.status_code}")
        except Exception as e:
            print(f"    ❌ ElevenLabs failed: {str(e)[:100]}")
    else:
        print("    ⚠️  No ElevenLabs key")

    # Test Azure TTS (if available)
    print("  - Azure TTS:")
    azure_key = os.getenv('AZURE_TTS_KEY') or os.getenv('AZURE_SPEECH_KEY')
    azure_region = os.getenv('AZURE_TTS_REGION') or os.getenv('AZURE_SPEECH_REGION')
    if azure_key and azure_region:
        try:
            url = f"https://{azure_region}.tts.speech.microsoft.com/cognitiveservices/v1"
            headers = {
                "Ocp-Apim-Subscription-Key": azure_key,
                "Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3"
            }
            data = f"""<speak version='1.0' xml:lang='en-US'>
                <voice xml:lang='en-US' xml:gender='Female' name='en-US-AriaNeural'>
                    Test speech synthesis.
                </voice>
            </speak>"""

            response = requests.post(url, headers=headers, data=data, timeout=10)
            if response.status_code == 200:
                print("    ✅ Azure TTS working")
            else:
                print(f"    ❌ Azure TTS error: {response.status_code}")
        except Exception as e:
            print(f"    ❌ Azure TTS failed: {str(e)[:100]}")
    else:
        print("    ⚠️  No Azure TTS keys")

    # Recommendations
    print("\n💡 BOTTLENECK OPTIMIZATION RECOMMENDATIONS:")
    print("=" * 60)

    if gemini_key and tts_key:
        print("1. ✅ You have both Gemini and TTS API keys")
        print("2. 🔧 Enable Text-to-Speech API in Google Cloud Console")
        print("3. 🔧 Verify TTS API key has correct permissions")
    elif gemini_key:
        print("1. ⚠️  Using Gemini API key for TTS (wrong key type)")
        print("2. 🔧 Get dedicated Google Cloud TTS API key")
        print("3. 🔧 Enable Text-to-Speech API in Google Cloud Console")
    else:
        print("1. ❌ No Google API keys found")
        print("2. ✅ OpenAI TTS is available as fallback")
        print("3. 💡 Consider Azure TTS or ElevenLabs for production")

    print("\n🎯 IMMEDIATE FIX OPTIONS:")
    print("A) Get Google Cloud TTS API key + enable API")
    print("B) Use OpenAI TTS (already working)")
    print("C) Add Azure TTS credentials")
    print("D) Skip TTS (not critical for Phase 1)")

if __name__ == "__main__":
    test_google_tts_diagnostic()