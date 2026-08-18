import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

# ==================================================
# 1. CONFIGURE DEEPSEEK CLIENT
# ==================================================
# Read API key from environment variable (NOT hardcoded!)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    print("❌ ERROR: DEEPSEEK_API_KEY not found in .env file")
    print("Create a .env file with: DEEPSEEK_API_KEY=your_key_here")
    exit()

# Create the client pointing to DeepSeek's API
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)


# ==================================================
# 2. GET USER INPUT
# ==================================================
print("\n" + "="*50)
print("📚 PERSONAL STUDY ASSISTANT (Powered by DeepSeek)")
print("="*50)

topic = input("\nEnter your topic or paste your notes: ")

if not topic.strip():
    print("❌ You didn't enter anything. Please try again.")
    exit()

# ==================================================
# 3. CALL THE DEEPSEEK API
# ==================================================
print("\n🤖 Generating summary and practice questions...\n")

try:
    response = client.chat.completions.create(
        model="deepseek-chat",  # DeepSeek's main chat model [citation:10]
        messages=[
            {"role": "system", "content": """You are a helpful study assistant.
Given the topic or notes, do the following:
1. Write a 1-paragraph summary
2. Generate 5 practice questions with answers
3. Format your response clearly with labels: "Summary:", "Question 1:", etc.
If you are unsure about a fact, say 'Uncertain' instead of inventing."""},
            {"role": "user", "content": topic}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    ai_output = response.choices[0].message.content
    
    # ==================================================
    # 4. SAVE TO A FILE
    # ==================================================
    filename = f"study_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, "w") as file:
        file.write(f"TOPIC/NOTES: {topic}\n\n")
        file.write("="*50 + "\n")
        file.write("AI-GENERATED STUDY MATERIAL (via DeepSeek)\n")
        file.write("="*50 + "\n\n")
        file.write(ai_output)
    
    # ==================================================
    # 5. SHOW THE OUTPUT
    # ==================================================
    print("="*50)
    print("✅ STUDY MATERIAL GENERATED!")
    print("="*50)
    print(f"\n📁 Saved to: {filename}\n")
    print(ai_output)
    print("\n" + "="*50)
    print("✅ File saved successfully!")
    print("\n💡 Remember: Always verify AI-generated facts against trusted sources!")

except Exception as e:
    print(f"❌ An error occurred: {e}")
    print("\n💡 Troubleshooting tips:")
    print("  1. Check your DeepSeek API key is correct")
    print("  2. Make sure you have internet")
    print("  3. Make sure you have credits in your DeepSeek account")
    print("  4. Try using 'deepseek-v4-flash' as the model if 'deepseek-chat' doesn't work")