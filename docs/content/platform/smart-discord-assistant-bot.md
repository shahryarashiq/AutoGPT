# Smart Discord Assistant Bot Tutorial

## Overview

This tutorial demonstrates how to create a multi-functional Discord bot using AutoGPT that can:
- Chat intelligently using AI
- Search the web and summarize results
- Transcribe and summarize YouTube videos
- Provide help information

This bot showcases the power of the AutoGPT platform by combining multiple blocks into a single intelligent assistant.

## Features

### 1. AI Chat (!chat)
Engage in natural conversations with an AI assistant powered by GPT-4.

**Usage:** `!chat <your message>`

**Example:**
```
!chat What is machine learning?
!chat Tell me a joke
!chat Explain quantum physics simply
```

### 2. Web Search (!search)
Search the web and get AI-summarized results.

**Usage:** `!search <your query>`

**Example:**
```
!search latest AI developments 2024
!search best programming languages for beginners
!search climate change statistics
```

### 3. YouTube Video Summarization (!youtube)
Get a concise summary of any YouTube video.

**Usage:** `!youtube <youtube_url>`

**Example:**
```
!youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ
!youtube https://youtu.be/example
```

### 4. Help Command (!help)
Display available commands and usage examples.

**Usage:** `!help`

## Setup Instructions

### Prerequisites

1. **Discord Bot Token**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Navigate to the "Bot" section
   - Click "Add Bot"
   - Copy the bot token
   - Enable "Message Content Intent" under Privileged Gateway Intents

2. **AutoGPT Platform Access**
   - AutoGPT Platform installed and running
   - OpenAI API key configured (for AI responses)

3. **Bot Permissions**
   - Read Messages
   - Send Messages
   - Read Message History

### Installation Steps

#### Step 1: Import the Bot Template

1. Open the AutoGPT Platform interface
2. Navigate to the "Library" or "Templates" section
3. Look for "Smart Discord Assistant Bot" template
4. Click "Import" or "Use Template"

#### Step 2: Configure the Bot Token

1. In the graph editor, find the "bot-token-constant" node
2. Click on it to edit
3. Replace `YOUR_DISCORD_BOT_TOKEN_HERE` with your actual Discord bot token
4. Save the changes

#### Step 3: Configure API Keys (if needed)

1. Ensure your OpenAI API key is configured in the platform settings
2. The LLM blocks will automatically use your configured credentials

#### Step 4: Save and Deploy

1. Click the "Save" button to save your agent
2. Give it a meaningful name (e.g., "My Discord Assistant")
3. Click "Run" or "Deploy" to start the bot

### Inviting the Bot to Your Server

1. Go back to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application
3. Navigate to "OAuth2" > "URL Generator"
4. Select scopes:
   - `bot`
   - `applications.commands` (optional, for slash commands)
5. Select bot permissions:
   - Read Messages/View Channels
   - Send Messages
   - Read Message History
6. Copy the generated URL and open it in your browser
7. Select the server you want to add the bot to
8. Authorize the bot

## How It Works

### Architecture

The bot uses a pattern-matching approach to route different commands to appropriate handlers:

```
Discord Message Input
        ↓
   Pattern Matchers (4 routes)
        ↓
    ┌───┴───┬───────┬────────┐
    ↓       ↓       ↓        ↓
 !chat  !search !youtube  !help
    ↓       ↓       ↓        ↓
  LLM    Search   YouTube  Const
    ↓       ↓       ↓        ↓
    └───┬───┴───┬───┴────────┘
        ↓       ↓
   LLM Summary (for search/youtube)
        ↓
 Discord Message Output
```

### Block Breakdown

1. **Read Discord Messages Block**
   - Listens for messages in Discord channels
   - Outputs message content, channel info, and user info

2. **Pattern Matcher Blocks (4)**
   - Match messages against regex patterns
   - Route to positive output if pattern matches
   - Route to negative output if no match

3. **LLM Blocks (3)**
   - `chat-llm`: Handles general conversation
   - `search-llm-summary`: Summarizes web search results
   - `youtube-llm-summary`: Summarizes video transcripts

4. **Web Search Block**
   - Performs web searches
   - Returns relevant search results

5. **YouTube Transcribe Block**
   - Extracts video ID from URL
   - Fetches video transcript
   - Outputs full transcript text

6. **Send Discord Message Block**
   - Sends responses back to Discord
   - Uses the same channel as the input message

7. **Constant Block**
   - Stores the Discord bot token
   - Provides help text

## Customization Options

### Modify AI Personality

Edit the `sys_prompt` in the `chat-llm` block:

```json
{
  "sys_prompt": "You are a helpful and friendly AI assistant in a Discord server. Keep your responses concise and engaging. Use Discord markdown when appropriate."
}
```

### Change AI Model

Update the `model` field in LLM blocks:
- `gpt-4o-mini` - Fast and cost-effective (default)
- `gpt-4o` - More capable
- `gpt-4-turbo` - Advanced reasoning
- `claude-3-5-sonnet-20241022` - Alternative AI provider

### Add New Commands

1. Add a new Pattern Matcher block
2. Define the regex pattern for your command
3. Connect to appropriate processing blocks
4. Link output to the Discord sender

### Adjust Response Length

Modify the LLM system prompts to control response length:
- "Keep responses under 100 words"
- "Provide detailed explanations"
- "Use bullet points for clarity"

## Testing

### Test Commands

1. **Test Chat:**
   ```
   !chat Hello, how are you?
   ```
   Expected: Friendly AI response

2. **Test Search:**
   ```
   !search What is AutoGPT?
   ```
   Expected: Summary of web search results about AutoGPT

3. **Test YouTube:**
   ```
   !youtube https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```
   Expected: Summary of the video content

4. **Test Help:**
   ```
   !help
   ```
   Expected: Help message with command list

## Troubleshooting

### Bot doesn't respond

**Check:**
- Bot is online in Discord (green indicator)
- Bot has proper permissions in the channel
- Message Content Intent is enabled
- Bot token is correct
- Agent is running in AutoGPT platform

### "Invalid token" error

**Solution:**
- Verify bot token is correct
- Regenerate token in Discord Developer Portal if needed
- Update token in the constant block

### YouTube command fails

**Common issues:**
- Video has no captions/transcript
- Video is private or age-restricted
- URL format is incorrect

**Solution:**
- Ensure video has English captions
- Try a different public video
- Check URL format matches pattern

### Search command returns no results

**Check:**
- Internet connectivity
- Search API credentials configured
- Query is not empty

## Advanced Usage

### Adding Message History

To make the chat more contextual, you can add a memory/history block:

1. Add a "List History" block
2. Connect it between the Pattern Matcher and LLM
3. Configure to store last N messages
4. Include history in the LLM prompt

### Rate Limiting

To prevent abuse:

1. Add a counter block per user
2. Implement cooldown periods
3. Set maximum requests per minute

### Multi-language Support

1. Add language detection block
2. Route to appropriate LLM with language-specific prompts
3. Configure translation blocks if needed

## Security Considerations

### Best Practices

1. **Never expose your bot token**
   - Store tokens securely
   - Use environment variables
   - Don't commit tokens to version control

2. **Implement permission checks**
   - Restrict commands to specific roles
   - Add admin-only commands

3. **Monitor usage**
   - Track API costs
   - Set spending limits
   - Log command usage

4. **Sanitize inputs**
   - Validate URLs before processing
   - Prevent injection attacks
   - Limit response lengths

## Cost Optimization

### Tips to Reduce Costs

1. **Use cheaper models for simple tasks**
   - `gpt-4o-mini` for basic chat
   - `gpt-4o` only when needed

2. **Implement caching**
   - Cache web search results
   - Cache YouTube transcripts
   - Set expiration times

3. **Set token limits**
   - Limit input token count
   - Limit output token count
   - Truncate long transcripts

4. **Filter irrelevant messages**
   - Only process messages with bot mention
   - Ignore messages from bots
   - Skip empty messages

## Example Use Cases

### 1. Study Group Assistant
Students can ask questions, search for resources, and get video summaries for learning materials.

### 2. Server Moderator Helper
Help users by answering common questions, searching documentation, and explaining video content.

### 3. Content Creator Tool
Quickly research topics, summarize reference videos, and brainstorm ideas with AI.

### 4. Technical Support Bot
Search for solutions, explain technical concepts, and provide relevant video tutorials.

## Next Steps

### Enhancements to Consider

1. **Add image generation**
   - Integrate with DALL-E or Stable Diffusion
   - Generate images from text descriptions

2. **Add voice support**
   - Transcribe voice messages
   - Generate voice responses

3. **Database integration**
   - Store user preferences
   - Track conversation history
   - Implement user statistics

4. **Webhook integration**
   - Connect to other services
   - Trigger external workflows
   - Send notifications

5. **Analytics dashboard**
   - Track command usage
   - Monitor response times
   - Analyze user engagement

## Community and Support

- **Documentation:** [docs.agpt.co](https://docs.agpt.co)
- **Discord:** [discord.gg/autogpt](https://discord.gg/autogpt)
- **GitHub:** [github.com/Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)

## License

This bot template is part of the AutoGPT Platform and is subject to the Polyform Shield License.

## Credits

Created as an example bot template demonstrating AutoGPT Platform capabilities. Combines multiple blocks to create a practical Discord assistant.

---

**Need help?** Join the AutoGPT Discord community or check the documentation for more tutorials and examples.
