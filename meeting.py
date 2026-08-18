
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
print("\n" + "="*60)
print("📋 MEETING MINUTES ASSISTANT (Powered by DeepSeek)")
print("="*60)

print("\n📝 Paste your meeting minutes below (press Ctrl+D or Ctrl+Z when done):")
print("   (Or paste everything at once and press Enter twice)\n")

# Collect multi-line input
lines = []
while True:
    try:
        line = input()
        if line.strip() == "":
            # If user presses Enter twice, we'll continue collecting
            # But we'll break if they press Enter on an empty line after content
            if len(lines) > 0 and lines[-1] == "":
                break
            lines.append("")
        else:
            lines.append(line)
    except EOFError:
        break

meeting_notes = "\n".join(lines).strip()

if not meeting_notes:
    print("❌ No meeting notes entered. Please try again.")
    exit()

# ==================================================
# 3. CALL THE DEEPSEEK API
# ==================================================
print("\n🤖 Analyzing meeting minutes and extracting action points...\n")

try:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": """You are a professional meeting assistant.
Given the meeting minutes, do the following in a clear, structured format:

1. **Summary**: Write a 2-3 sentence summary of the meeting
2. **Key Decisions**: List the key decisions made (bullet points)
3. **Action Points**: List all action items with:
   - What needs to be done
   - Who is responsible (if mentioned)
   - Deadline (if mentioned)
4. **My Tasks**: Identify ALL tasks that are specifically for "me" or "I" or the person who wrote the notes. 
   Highlight these with ✅.
5. **Process/Next Steps**: Describe the process or next steps that need to follow.

If names are mentioned, use them. If something is unclear, state "Uncertain" instead of inventing."""},
            {"role": "user", "content": meeting_notes}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    ai_output = response.choices[0].message.content
    
    # ==================================================
    # 4. SAVE TO A FILE
    # ==================================================
    filename = f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, "w") as file:
        file.write("="*60 + "\n")
        file.write("MEETING MINUTES ANALYSIS\n")
        file.write("="*60 + "\n")
        file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        file.write("="*60 + "\n")
        file.write("ORIGINAL MINUTES\n")
        file.write("="*60 + "\n\n")
        file.write(meeting_notes)
        file.write("\n\n")
        file.write("="*60 + "\n")
        file.write("AI-GENERATED EXTRACT\n")
        file.write("="*60 + "\n\n")
        file.write(ai_output)
        file.write("\n\n")
        file.write("="*60 + "\n")
        file.write("✅ AI-NOTE: Always verify AI-generated facts against trusted sources!\n")
        file.write("="*60 + "\n")
    
    # ==================================================
    # 5. SHOW THE OUTPUT
    # ==================================================
    print("="*60)
    print("✅ MEETING ANALYSIS COMPLETE!")
    print("="*60)
    print(f"\n📁 Saved to: {filename}\n")
    print(ai_output)
    print("\n" + "="*60)
    print("✅ File saved successfully!")

except Exception as e:
    print(f"❌ An error occurred: {e}")
    print("\n💡 Troubleshooting tips:")
    print("  1. Check your DeepSeek API key is correct")
    print("  2. Make sure you have internet")
    print("  3. Make sure you have credits in your DeepSeek account")
    print("  4. Try using 'deepseek-v4-flash' as the model if 'deepseek-chat' doesn't work")

