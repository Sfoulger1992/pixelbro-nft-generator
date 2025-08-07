
import openai

class PixelBroGPT:
    def __init__(self):
        openai.api_key = "YOUR_OPENAI_API_KEY"

        self.system_prompt = (
            "You are PixelBro, a chill, creative assistant who helps users make generative NFT art projects. "
            "You speak in a laid-back, friendly tone and guide them step-by-step through creating pixel-art traits, "
            "generating NFTs, metadata, and smart contracts. Be helpful, throw in fun comments, and never get too formal."
        )

    def chat(self, user_input):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=300
        )
        return response['choices'][0]['message']['content'].strip()
