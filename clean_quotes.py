import sys
import os
import json
import re

def clean_text(text):
    """Strips Gemini's UI quote prefixes while preserving your actual reply."""
    if not text:
        return ""
    
    # Matches "You said" followed by quoted text (e.g., 'You said  "..."' or 'You said  “...”')
    cleaned = re.sub(r'^You said\s+["“].*?["”]\s*', '', text, flags=re.DOTALL)
    
    # Catch unquoted 'You said <text>' patterns up to double newlines or end of quote block
    cleaned = re.sub(r'^You said\s+.*?\n\n', '', cleaned, flags=re.DOTALL)
    
    # Catch edge case where "You said " is just prepended to the user prompt
    if cleaned.startswith("You said "):
        cleaned = re.sub(r'^You said\s+', '', cleaned)

    return cleaned.strip()

def clean_quotes_only():
    if len(sys.argv) < 2:
        print("❌ Error: Missing input JSON file.")
        print("👉 Usage: python clean_quotes.py <path_to_your_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found.")
        sys.exit(1)

    print(f"📖 Reading JSON file: {input_file}")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Process each turn without altering array order
    cleaned_count = 0
    for turn in data:
        if turn.get("parts") and len(turn["parts"]) > 0:
            original_text = turn["parts"][0]["text"]
            cleaned_result = clean_text(original_text)
            
            if original_text != cleaned_result:
                cleaned_count += 1
                turn["parts"][0]["text"] = cleaned_result

    # Generate output names based on input file
    base_name, _ = os.path.splitext(input_file)
    output_json = f"{base_name}_no_quotes.json"
    output_md = f"{base_name}_no_quotes.md"

    # Save cleaned JSON
    with open(output_json, "w", encoding="utf-8") as out_json:
        json.dump(data, out_json, indent=2, ensure_ascii=False)

    # Save cleaned Markdown
    with open(output_md, "w", encoding="utf-8") as out_md:
        for turn in data:
            role = turn.get("role", "unknown").capitalize()
            text = turn["parts"][0]["text"] if turn.get("parts") else ""
            if not text:
                continue
            header = "### 👤 User\n\n" if role == "User" else "### 🤖 Gemini\n\n"
            out_md.write(f"{header}{text}\n\n---\n\n")

    print(f"✅ Finished! Cleaned 'You said' prefixes from {cleaned_count} turns.")
    print("Created output files:")
    print(f" 📄 {output_json}")
    print(f" 📝 {output_md}")

if __name__ == "__main__":
    clean_quotes_only()