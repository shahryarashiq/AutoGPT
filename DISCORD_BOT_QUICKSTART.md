# Quick Start: Smart Discord Assistant Bot

This guide will get your Discord bot running in under 10 minutes!

## What You'll Get

A Discord bot that can:
- 💬 Chat with AI (`!chat`)
- 🔍 Search the web (`!search`)  
- 📹 Summarize YouTube videos (`!youtube`)
- ❓ Show help (`!help`)

## Prerequisites (5 minutes)

### 1. Get a Discord Bot Token

1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Give it a name (e.g., "Smart Assistant")
4. Go to "Bot" tab → Click "Add Bot"
5. Under "Privileged Gateway Intents", enable:
   - ✅ Message Content Intent
6. Click "Reset Token" and copy it (you'll need this!)

### 2. Invite Bot to Your Server

1. Go to "OAuth2" → "URL Generator"
2. Select Scopes: `bot`
3. Select Permissions:
   - Read Messages/View Channels
   - Send Messages
   - Read Message History
4. Copy the generated URL
5. Open it in browser and add bot to your server

### 3. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Copy it (you'll need this!)

## Setup AutoGPT Bot (5 minutes)

### Method 1: Using AutoGPT Platform UI

1. Open AutoGPT Platform at http://localhost:8000 (or your hosted URL)
2. Go to "Templates" or "Library"
3. Find "Smart Discord Assistant Bot"
4. Click "Import Template"
5. In the graph editor, find the "bot-token-constant" block
6. Replace `YOUR_DISCORD_BOT_TOKEN_HERE` with your Discord bot token
7. Go to Settings → Add your OpenAI API key
8. Click "Save" then "Run"

### Method 2: Using JSON Template

1. Copy the template file:
   ```bash
   cp autogpt_platform/graph_templates/Smart\ Discord\ Assistant\ Bot_v1.json /tmp/my-bot.json
   ```

2. Edit the file and replace the bot token:
   ```bash
   # Replace YOUR_DISCORD_BOT_TOKEN_HERE with your actual token
   nano /tmp/my-bot.json
   ```

3. Import in AutoGPT Platform:
   - Open Platform UI
   - Import JSON file
   - Configure API keys
   - Run the agent

## Test Your Bot

In any channel where the bot is present, try:

```
!help
```

You should see the help message!

Try other commands:
```
!chat What is AutoGPT?
!search latest tech news
!youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Troubleshooting

### Bot is offline
- Check bot token is correct
- Verify agent is running in AutoGPT Platform
- Check the platform logs for errors

### Bot doesn't respond
- Make sure "Message Content Intent" is enabled
- Verify bot has permission to read/send messages in channel
- Check bot is online (green dot in Discord)

### Commands don't work
- Make sure you're using the correct prefix: `!`
- Check spelling of commands
- Verify the pattern matcher blocks are configured correctly

### "Invalid API key" error
- Verify OpenAI API key is correctly added in platform settings
- Check API key has available credits
- Ensure key hasn't been revoked

## What's Next?

- **Customize:** Edit the system prompts to change the bot's personality
- **Extend:** Add more commands by duplicating pattern matcher blocks
- **Monitor:** Check the platform logs to see how your bot is performing
- **Share:** Deploy to production and share with your community!

## Full Documentation

For detailed documentation, see: `/docs/content/platform/smart-discord-assistant-bot.md`

## Need Help?

- 📚 Documentation: https://docs.agpt.co
- 💬 Discord: https://discord.gg/autogpt
- 🐛 Issues: https://github.com/Significant-Gravitas/AutoGPT/issues

---

Happy bot building! 🤖✨
