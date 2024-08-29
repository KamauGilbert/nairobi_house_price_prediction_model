## 🤖 Chatbot Subfolder

This subfolder contains two important files:

1. **`chatgpt.py`** - 📝 A Python script that powers the RAG chatbot. You can chat with the bot directly in the terminal! Before running the script, make sure to install the required libraries using `pip install -r requirements.txt`. Remember to input your `OPENAI_API_KEY` (🔑) from [OpenAI's API Keys](https://platform.openai.com/api-keys). You'll need to create an account and generate the key there. Please note that these keys are billable, so check your usage limits here: [OpenAI Billing](https://platform.openai.com/settings/organization/limits). If you encounter the `insufficient_quota` error, ensure you've topped up your account to continue using the API.

2. **`data.txt`** - 📄 This file contains content from the article [Homeowners Seek Affordable Units as Housing Prices Sustain Unsteady Decline](https://www.kba.co.ke/homeowners-seek-affordable-units-as-housing-prices-sustain-unsteady-decline/) sourced online, detailing the state of housing in Kenya. Ensure both `data.txt` and `chatgpt.py` are in the same directory to run the script without issues.

✨ **Pro Tip:** RAG chatbots are fascinating! Feel free to edit the `data.txt` file with any other information you'd like, and then run `chatgpt.py` to see how the AI interacts with you based on the new content.

For more on RAG applications, check out the [LangChain AI Repository](https://github.com/langchain-ai/langchain?tab=readme-ov-file) or watch [this insightful video](https://youtu.be/CK0ExcCWDP4?si=WRQtxTIzCHBlPGrh) by Krish Naik. 🎥
