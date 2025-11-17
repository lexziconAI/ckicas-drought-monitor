import os
import cohere
from dotenv import load_dotenv

load_dotenv()

def test_cohere_key():
    """Test Cohere API key validity"""
    api_key = os.getenv('COHERE_API_KEY')

    if not api_key:
        print("❌ No COHERE_API_KEY found in .env")
        return False

    print(f"🔑 Testing Cohere API key: {api_key[:10]}...")

    try:
        # Initialize client
        co = cohere.Client(api_key=api_key)

        # Try a simple request
        response = co.chat(
            model="command-r-08-2024",  # Use current live model
            message="Hello, just testing API connectivity. Reply with: COHERE_TEST_OK"
        )

        print(f"✅ Cohere API working! Response: {response.text.strip()}")
        return True

    except Exception as e:
        print(f"❌ Cohere API error: {str(e)}")

        # Common error analysis
        error_str = str(e).lower()

        if "invalid api key" in error_str or "unauthorized" in error_str:
            print("\n🔧 POSSIBLE FIXES:")
            print("1. Check if API key is expired - get new one from https://dashboard.cohere.com/api-keys")
            print("2. Verify key format - should start with no prefix, just the key")
            print("3. Check account has credits/billing set up")
            print("4. Try regenerating the API key in Cohere dashboard")

        elif "rate limit" in error_str:
            print("\n🔧 POSSIBLE FIXES:")
            print("1. Wait a few minutes before retrying")
            print("2. Check your rate limits in Cohere dashboard")
            print("3. Upgrade your plan if needed")

        elif "model" in error_str:
            print("\n🔧 POSSIBLE FIXES:")
            print("1. Use 'command-r-plus' instead of newer models")
            print("2. Check available models at https://docs.cohere.com/docs/models")

        else:
            print("\n🔧 GENERAL FIXES:")
            print("1. Verify internet connection")
            print("2. Check Cohere service status")
            print("3. Try a different Cohere model")
            print("4. Contact Cohere support if issue persists")

        return False

if __name__ == "__main__":
    test_cohere_key()