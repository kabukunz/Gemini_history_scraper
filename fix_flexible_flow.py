import sys
import os
import json

def fix_flexible_flow():
    if len(sys.argv) < 2:
        print("❌ Error: Missing input JSON file.")
        print("👉 Usage: python fix_flexible_pairs.py <path_to_your_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found.")
        sys.exit(1)

    print(f"📖 Reading JSON file: {input_file}")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Step 1: Group contiguous turns by role into blocks
    blocks = []
    current_block = []
    current_role = None

    for turn in data:
        role = turn.get("role")
        if role != current_role:
            if current_block:
                blocks.append((current_role, current_block))
            current_block = [turn]
            current_role = role
        else:
            current_block.append(turn)

    if current_block:
        blocks.append((current_role, current_block))

    print(f"📦 Grouped {len(data)} turns into {len(blocks)} continuous role blocks.")

    # Step 2: Swap adjacent Model -> User block sequences so User comes first
    fixed_blocks = []
    i = 0
    total_blocks = len(blocks)

    while i < total_blocks:
        role, turns = blocks[i]
        next_role, next_turns = blocks[i+1] if i + 1 < total_blocks else (None, None)

        # If we see a Model block followed by a User block, swap their order
        if role == "model" and next_role == "user":
            fixed_blocks.append(next_turns)  # User block first
            fixed_blocks.append(turns)       # Model block second
            i += 2
        else:
            fixed_blocks.append(turns)
            i += 1

    # Flatten back into a single list of turns
    final_turns = [turn for block in fixed_blocks for turn in block]

    # Output file paths
    base_name, _ = os.path.splitext(input_file)
    output_json = f"{base_name}_flexible_fixed.json"
    output_md = f"{base_name}_flexible_fixed.md"

    # Save fixed JSON
    with open(output_json, "w", encoding="utf-8") as out_j:
        json.dump(final_turns, out_j, indent=2, ensure_ascii=False)

    # Save fixed Markdown
    with open(output_md, "w", encoding="utf-8") as out_m:
        for turn in final_turns:
            role = turn.get("role", "unknown").capitalize()
            text = turn["parts"][0]["text"] if turn.get("parts") else ""
            if not text:
                continue
            header = "### 👤 User\n\n" if role == "User" else "### 🤖 Gemini\n\n"
            out_m.write(f"{header}{text}\n\n---\n\n")

    print(f"✅ Successfully re-aligned flow!")
    print(f"📄 Saved JSON: {output_json}")
    print(f"📝 Saved Markdown: {output_md}")

if __name__ == "__main__":
    fix_flexible_flow()