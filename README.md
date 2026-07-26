# Gemini History Scraper & Cleaner

If you have a Gemini conversation that's too long to split directly in the UI, here's a lightweight toolkit to scrape, clean, and re-align it. Once processed, you can break the chat into smaller, manageable chunks to recreate new sessions seamlessly.

---

## 🛠️ How-To Guide

1. **Share & Open:** Share your long Gemini conversation, then open the shared link in a standalone tab or window.
2. **Scrape:** Open your browser's DevTools Console (`F12`), paste `console_scraper.js`, and press **Enter**.

   > **Note:** Keep the browser window focused while scraping to prevent execution from pausing. Enable auto-save without confirmation and authorize multi-file downloads if prompted. You can pause and resume using DevTools sources debugging.

    You'll get a list of files in your download directory named gemini_chat_backup_partxxx_(yyyy_items).json. they're incremental and the last one created is going to have all chat content

3. **Clean Scraper Noise:**
    remove chats artifact with:
   ```bash
   python clean_quotes.py <chat_name.json>
   ```
   (tested with python 3.9)
4. **Fix Inverted Flow & Sequence:** some part of conversation may be reversed. use:
   ```bash
   python fix_flexible_flow.py <chat_name_no_quotes.json>
   ```
5. **Split Context:** If everything's ok you'll end up with a: `<chat_name_no_quotes_realigned.json>` (or `.md` ) file you can separate into the parts you need. See below for a possible way of creating a new chat with it.

---

## 💬 Recreating Your Chat in a New Prompt

For every part, create a new chat and paste the following headers before the chat snippet you want to recreate:

### 📄 Header Instruction
> *The JSON/Markdown below is a transcript from a previous conversation. Please read it to establish context, but do not re-answer or summarize anything in the transcript yet. Simply reply with: "Context loaded. Ready for instructions."*

---

### Format Examples

#### Option A: JSON Format

Add your chat parts data: **JSON**

```json
[
  {
    "role": "user",
    "parts": [
      {
        "text": "I have this data structure version"
      }
    ]
  },
  {
    "role": "model",
    "parts": [
      {
        "text": "It looks like you might have forgotten to paste or attach the code! Drop your data structure code right here, and let me know what we're doing with it. Are we optimizing it, debugging a memory leak, converting it to a Python/Go variant, or integrating that password file logic and progress bar we worked on before? Whenever you're ready, paste it in and we'll get to work!"
      }
    ]
  }
]
```

#### Option B: Markdown Format

Add your chat parts data: **MD**

```markdown
I have this data structure version

---

### 🤖 Gemini

It looks like you might have forgotten to paste or attach the code! Drop your data structure code right here, and let me know what we're doing with it. Are we optimizing it, debugging a memory leak, converting it to a Python/Go variant, or integrating that password file logic and progress bar we worked on before? Whenever you're ready, paste it in and we'll get to work!
```

---

## 🔗 Conversation Reference

You can find the conversation used to generate all this at:  
👉 [https://share.gemini.google/TaZSIu4vDuG5](https://share.gemini.google/TaZSIu4vDuG5)
