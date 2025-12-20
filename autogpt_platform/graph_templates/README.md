# AutoGPT Agent Templates

This directory contains ready-to-use agent templates that you can import into the AutoGPT Platform.

## Available Templates

### 1. Smart Discord Assistant Bot (NEW!)
**File:** `Smart Discord Assistant Bot_v1.json`  
**Version:** 1

A comprehensive Discord bot with multiple capabilities:
- 💬 AI Chat - Natural conversations powered by GPT-4
- 🔍 Web Search - Search and get AI-summarized results  
- 📹 YouTube Summarization - Transcribe and summarize videos
- ❓ Help Command - Built-in command documentation

**Commands:**
- `!chat <message>` - Chat with AI
- `!search <query>` - Search the web
- `!youtube <url>` - Get video summary
- `!help` - Show available commands

**Use Cases:** 
- Study group assistant
- Server moderator helper
- Content creator tool
- Technical support bot

**Documentation:** See `/docs/content/platform/smart-discord-assistant-bot.md` for full setup guide

**Quick Start:** See `/DISCORD_BOT_QUICKSTART.md` for 10-minute setup

---

### 2. Discord Bot Chat To LLM
**File:** `Discord Bot Chat To LLM_v5.json`  
**Version:** 5

A simple Discord chatbot that responds to messages with AI.

**Command:** `!chat <message>`

**Description:** The bot listens for messages starting with `!chat` and responds using an LLM (Large Language Model). Great for basic AI conversations in Discord.

**Use Cases:**
- Simple Q&A bot
- Conversational assistant
- Learning how to integrate Discord with LLM

---

### 3. Discord Chatbot with History
**File:** `Discord Chatbot with History_v145.json`  
**Version:** 145

An advanced Discord chatbot that maintains conversation history for context-aware responses.

**Features:**
- Remembers previous messages
- Context-aware responses
- More natural conversations

**Use Cases:**
- Long-form conversations
- Customer support
- Interactive storytelling

---

### 4. Discord Search Bot
**File:** `Discord Search Bot_v17.json`  
**Version:** 17

A Discord bot that performs web searches and provides AI-summarized results.

**Command:** `!search <query>`

**Description:** The bot searches the web for information and uses AI to summarize the results into a concise, readable format.

**Use Cases:**
- Quick fact-checking
- Research assistant
- Information lookup

---

### 5. Medium Blogger
**File:** `Medium Blogger_v28.json`  
**Version:** 28

An automated content creation agent for Medium.

**Features:**
- Generates blog post content
- Formats for Medium platform
- Automated publishing workflow

**Use Cases:**
- Content automation
- Blog post generation
- Medium publishing workflow

---

## How to Use Templates

### Method 1: Import via UI

1. Open AutoGPT Platform interface
2. Navigate to "Library" or "Templates"
3. Click "Import Template"
4. Select the desired JSON file
5. Configure any required settings (API keys, tokens, etc.)
6. Save and run

### Method 2: Manual Import

1. Copy the template JSON file
2. Open AutoGPT Platform
3. Create a new agent
4. Open the graph editor
5. Import the JSON through the import function
6. Configure settings
7. Save and deploy

## Configuration Requirements

Most templates require:

- **Discord Bot Token** (for Discord bots)
  - Get from: https://discord.com/developers/applications
  - Enable "Message Content Intent"
  
- **OpenAI API Key** (for LLM features)
  - Get from: https://platform.openai.com/api-keys
  - Configure in platform settings

- **Other API Keys** (template-specific)
  - Check template documentation for requirements

## Customization

All templates can be customized:

1. **Change AI Model:**
   - Edit LLM blocks
   - Select different model (gpt-4o, claude-3, etc.)

2. **Modify Prompts:**
   - Edit system prompts in LLM blocks
   - Change personality and behavior

3. **Add/Remove Features:**
   - Add new blocks
   - Create new connections
   - Modify patterns and logic

4. **Adjust Settings:**
   - Change trigger patterns
   - Modify output formats
   - Update token limits

## Creating Your Own Templates

To create a new template:

1. Build your agent in the platform
2. Test thoroughly
3. Export as JSON
4. Set `"is_template": true` in the JSON
5. Add descriptive name and description
6. Document usage and requirements
7. Submit PR to add to this directory

### Template JSON Structure

```json
{
  "id": "unique-id",
  "version": 1,
  "is_active": false,
  "is_template": true,
  "name": "Template Name",
  "description": "What the template does",
  "nodes": [...],
  "links": [...]
}
```

## Versioning

Templates use semantic versioning:
- Filename format: `Template Name_vX.json`
- Higher version = newer/improved
- Breaking changes = new major version
- Keep old versions for compatibility

## Contributing

Want to contribute a template?

1. Create and test your agent
2. Export as JSON template
3. Add documentation
4. Submit PR with:
   - Template JSON file
   - Documentation (if complex)
   - Example usage
   - Screenshots (if applicable)

## Support

- **Documentation:** https://docs.agpt.co
- **Discord Community:** https://discord.gg/autogpt
- **GitHub Issues:** https://github.com/Significant-Gravitas/AutoGPT/issues

## License

Templates in this directory are part of the AutoGPT Platform and subject to the Polyform Shield License.

---

**Last Updated:** December 2024  
**Total Templates:** 5
