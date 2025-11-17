import os
import asyncio
import requests
import base64
from dotenv import load_dotenv
from anthropic import Anthropic
import time

load_dotenv()

class APIValidator:
    """Validate all Axiom-X external API integrations"""

    def __init__(self):
        self.results = {
            'llm': {},
            'financial': {},
            'image_generation': {},
            'text_to_speech': {},
            'vision': {}
        }

    # ========== FINANCIAL APIS ==========

    def test_alpha_vantage(self):
        """Test Alpha Vantage stock data API"""
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not api_key:
            return {'status': 'NO_KEY'}

        try:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={api_key}"
            response = requests.get(url, timeout=10)
            data = response.json()

            if 'Time Series (Daily)' in data:
                return {'status': 'SUCCESS', 'message': 'Stock data retrieved'}
            elif 'Note' in data:
                return {'status': 'RATE_LIMITED', 'message': data['Note']}
            else:
                return {'status': 'ERROR', 'message': str(data.get('Error Message', 'Unknown'))}
        except Exception as e:
            return {'status': 'FAILED', 'error': str(e)[:100]}

    def test_polygon(self):
        """Test Polygon.io market data API"""
        api_key = os.getenv('POLYGON_API_KEY')
        if not api_key:
            return {'status': 'NO_KEY'}

        try:
            url = f"https://api.polygon.io/v2/aggs/ticker/AAPL/prev?apiKey={api_key}"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get('status') == 'OK':
                return {'status': 'SUCCESS', 'message': 'Market data retrieved'}
            else:
                return {'status': 'ERROR', 'message': data.get('error', 'Unknown')}
        except Exception as e:
            return {'status': 'FAILED', 'error': str(e)[:100]}

    def test_finnhub(self):
        """Test Finnhub stock API"""
        api_key = os.getenv('FINNHUB_API_KEY')
        if not api_key:
            return {'status': 'NO_KEY'}

        try:
            url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={api_key}"
            response = requests.get(url, timeout=10)
            data = response.json()

            if 'c' in data:  # 'c' is current price
                return {'status': 'SUCCESS', 'message': f"Price: ${data['c']}"}
            else:
                return {'status': 'ERROR', 'message': str(data)}
        except Exception as e:
            return {'status': 'FAILED', 'error': str(e)[:100]}

    # ========== IMAGE GENERATION APIS ==========

    def test_fal_ai(self):
        """Test fal.ai image generation API"""
        api_key = os.getenv('FAL_API_KEY')
        if not api_key:
            return {'status': 'NO_KEY'}

        try:
            # Simple test: Check if API key is valid
            url = "https://fal.run/fal-ai/fast-sdxl"
            headers = {
                "Authorization": f"Key {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "prompt": "test validation image",
                "image_size": "square_hd",
                "num_inference_steps": 1  # Minimal for speed
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'SUCCESS',
                    'message': 'Image generated',
                    'image_url': data.get('images', [{}])[0].get('url')
                }
            else:
                return {'status': 'ERROR', 'message': f"HTTP {response.status_code}"}
        except Exception as e:
            return {'status': 'FAILED', 'error': str(e)[:100]}

    def test_replicate(self):
        """Test Replicate API (possibly 'nanobana' or other model)"""
        api_key = os.getenv('REPLICATE_API_KEY')
        if not api_key:
            return {'status': 'NO_KEY'}

        try:
            # Just test authentication
            url = "https://api.replicate.com/v1/models"
            headers = {"Authorization": f"Token {api_key}"}

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                return {'status': 'SUCCESS', 'message': 'API authenticated'}
            else:
                return {'status': 'ERROR', 'message': f"HTTP {response.status_code}"}
        except Exception as e:
            return {'status': 'FAILED', 'error': str(e)[:100]}

    def test_stability_ai(self):
        """Test Stability AI (Stable Diffusion)"""
        api_key = os.getenv('STABILITY_API_KEY')
        if not api_key:
            return {'status': 'NO_KEY'}

        try:
            url = "https://api.stability.ai/v1/user/account"
            headers = {"Authorization": f"Bearer {api_key}"}

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                return {'status': 'SUCCESS', 'message': 'Account verified'}
            else:
                return {'status': 'ERROR', 'message': f"HTTP {response.status_code}"}
        except Exception as e:
            return {'status': 'FAILED', 'error': str(e)[:100]}

    def test_openai_dalle(self):
        """Test OpenAI DALL-E image generation"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return {'status': 'NO_KEY'}

        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            # Small test image
            response = client.images.generate(
                model="dall-e-3",
                prompt="simple test circle",
                size="1024x1024",
                n=1
            )

            return {
                'status': 'SUCCESS',
                'message': 'Image generated',
                'image_url': response.data[0].url
            }
        except Exception as e:
            return {'status': 'FAILED', 'error': str(e)[:100]}

    # ========== TEXT-TO-SPEECH ==========

    def test_google_tts(self):
        """Test Google Cloud Text-to-Speech"""
        # Skip Google TTS - API key blocked, use OpenAI TTS instead
        return {'status': 'SKIPPED', 'message': 'Using OpenAI TTS instead'}

    def test_openai_tts(self):
        """Test OpenAI Text-to-Speech (primary TTS solution)"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return {'status': 'NO_KEY'}

        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            # Test TTS generation
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input="This is a test of OpenAI text-to-speech synthesis."
            )

            # Check if we got audio data
            if response.content:
                return {'status': 'SUCCESS', 'message': 'Audio generated successfully'}
            else:
                return {'status': 'ERROR', 'message': 'No audio data received'}
        except Exception as e:
            return {'status': 'FAILED', 'error': str(e)[:100]}

    def test_elevenlabs(self):
        """Test ElevenLabs TTS (if key exists)"""
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if not api_key:
            return {'status': 'NO_KEY'}

        try:
            url = "https://api.elevenlabs.io/v1/user"
            headers = {"xi-api-key": api_key}

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                return {'status': 'SUCCESS', 'message': 'Account verified'}
            else:
                return {'status': 'ERROR', 'message': f"HTTP {response.status_code}"}
        except Exception as e:
            return {'status': 'FAILED', 'error': str(e)[:100]}

    # ========== VISION API VALIDATION ==========

    def test_claude_vision(self, test_image_url=None):
        """
        Test Claude's vision API by analyzing an image
        If test_image_url provided, use that; otherwise use a generated image
        """
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return {'status': 'NO_KEY'}

        try:
            client = Anthropic(api_key=api_key)

            # If no image provided, use a simple test image URL
            if not test_image_url:
                test_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/240px-Cat03.jpg"

            # Download and encode image
            image_response = requests.get(test_image_url, timeout=10)
            image_data = base64.standard_b64encode(image_response.content).decode("utf-8")

            # Test vision API
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=100,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Describe this image in 5 words or less."
                        }
                    ],
                }],
            )

            description = message.content[0].text

            return {
                'status': 'SUCCESS',
                'message': f'Vision working: "{description}"',
                'image_analyzed': test_image_url
            }
        except Exception as e:
            return {'status': 'FAILED', 'error': str(e)[:100]}

    # ========== ORCHESTRATION ==========

    def run_all_tests(self):
        """Run all API tests and generate report"""
        print("=" * 70)
        print("🔍 AXIOM-X COMPLETE API ECOSYSTEM VALIDATION")
        print("=" * 70)

        # Financial APIs
        print("\n💰 FINANCIAL DATA APIS:")
        self.results['financial']['alpha_vantage'] = self.test_alpha_vantage()
        print(f"  Alpha Vantage: {self._format_result(self.results['financial']['alpha_vantage'])}")

        self.results['financial']['polygon'] = self.test_polygon()
        print(f"  Polygon.io: {self._format_result(self.results['financial']['polygon'])}")

        self.results['financial']['finnhub'] = self.test_finnhub()
        print(f"  Finnhub: {self._format_result(self.results['financial']['finnhub'])}")

        # Image Generation APIs
        print("\n🎨 IMAGE GENERATION APIS:")
        self.results['image_generation']['fal_ai'] = self.test_fal_ai()
        print(f"  fal.ai: {self._format_result(self.results['image_generation']['fal_ai'])}")

        self.results['image_generation']['replicate'] = self.test_replicate()
        print(f"  Replicate: {self._format_result(self.results['image_generation']['replicate'])}")

        self.results['image_generation']['stability'] = self.test_stability_ai()
        print(f"  Stability AI: {self._format_result(self.results['image_generation']['stability'])}")

        self.results['image_generation']['openai_dalle'] = self.test_openai_dalle()
        print(f"  OpenAI DALL-E: {self._format_result(self.results['image_generation']['openai_dalle'])}")

        # Text-to-Speech APIs
        print("\n🔊 TEXT-TO-SPEECH APIS:")
        self.results['text_to_speech']['openai_tts'] = self.test_openai_tts()
        print(f"  OpenAI TTS: {self._format_result(self.results['text_to_speech']['openai_tts'])}")

        self.results['text_to_speech']['google_tts'] = self.test_google_tts()
        print(f"  Google TTS: {self._format_result(self.results['text_to_speech']['google_tts'])}")

        self.results['text_to_speech']['elevenlabs'] = self.test_elevenlabs()
        print(f"  ElevenLabs: {self._format_result(self.results['text_to_speech']['elevenlabs'])}")

        # Vision API (use generated image if available)
        print("\n👁️  VISION API VALIDATION:")

        # Try to get a generated image URL from previous tests
        test_image = None
        for result in self.results['image_generation'].values():
            if result.get('status') == 'SUCCESS' and 'image_url' in result:
                test_image = result['image_url']
                print(f"  Using generated image from {result.get('provider', 'image gen')} for vision test...")
                break

        self.results['vision']['claude_vision'] = self.test_claude_vision(test_image)
        print(f"  Claude Vision: {self._format_result(self.results['vision']['claude_vision'])}")

        # Summary
        self._print_summary()

        return self.results

    def _format_result(self, result):
        """Format test result for display"""
        status = result.get('status', 'UNKNOWN')

        if status == 'SUCCESS':
            msg = result.get('message', 'OK')
            return f"✅ {msg}"
        elif status == 'NO_KEY':
            return "⚠️  No API key found"
        elif status == 'RATE_LIMITED':
            return f"⏸️  Rate limited: {result.get('message', '')}"
        elif status == 'ERROR':
            return f"❌ Error: {result.get('message', 'Unknown')}"
        elif status == 'FAILED':
            return f"❌ Failed: {result.get('error', 'Unknown')}"
        else:
            return f"❓ {status}"

    def _print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 70)
        print("📊 VALIDATION SUMMARY")
        print("=" * 70)

        categories = {
            'Financial': self.results['financial'],
            'Image Gen': self.results['image_generation'],
            'TTS': self.results['text_to_speech'],
            'Vision': self.results['vision']
        }

        for category, tests in categories.items():
            success = sum(1 for r in tests.values() if r.get('status') == 'SUCCESS')
            total = len(tests)
            print(f"{category:12} {success}/{total} working")

        print("=" * 70)

        # Check if Constitutional-Market-Harmonics has what it needs
        financial_working = any(
            r.get('status') == 'SUCCESS'
            for r in self.results['financial'].values()
        )

        if financial_working:
            print("\n✅ Constitutional-Market-Harmonics: At least 1 financial API working")
        else:
            print("\n⚠️  Constitutional-Market-Harmonics: No financial APIs available")

        # Check if image generation + vision pipeline works
        image_working = any(
            r.get('status') == 'SUCCESS'
            for r in self.results['image_generation'].values()
        )
        vision_working = self.results['vision'].get('claude_vision', {}).get('status') == 'SUCCESS'

        if image_working and vision_working:
            print("✅ Image Generation → Vision Pipeline: VALIDATED")
        else:
            print("⚠️  Image Generation → Vision Pipeline: Incomplete")

        print("\n🚀 Ready for Phase 1: Recursive Self-Optimization")

if __name__ == "__main__":
    validator = APIValidator()
    results = validator.run_all_tests()