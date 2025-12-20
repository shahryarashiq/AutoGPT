# Smart Discord Assistant Bot - Troubleshooting Guide

This guide helps you diagnose and fix common issues with the Smart Discord Assistant Bot.

## Quick Diagnostic Checklist

Before diving into specific issues, check these basics:

- [ ] Bot token is correct and hasn't been regenerated
- [ ] Bot is invited to your Discord server
- [ ] Bot has proper permissions (Read Messages, Send Messages)
- [ ] Message Content Intent is enabled in Discord Developer Portal
- [ ] AutoGPT Platform agent is running
- [ ] OpenAI API key is configured
- [ ] API key has available credits

## Common Issues and Solutions

### 1. Bot Appears Offline in Discord

**Symptoms:**
- Bot shows as offline (grey dot)
- Bot doesn't respond to any commands
- No activity in Discord

**Possible Causes & Solutions:**

#### A. Agent Not Running
**Check:**
```bash
# In AutoGPT Platform, verify agent status shows "Running"
```

**Solution:**
1. Go to AutoGPT Platform UI
2. Find your bot agent
3. Click "Run" or "Deploy"
4. Wait for status to show "Running"

#### B. Invalid Bot Token
**Check:**
- Bot token in template matches Discord Developer Portal

**Solution:**
1. Go to Discord Developer Portal
2. Navigate to your application → Bot
3. Click "Reset Token" and copy new token
4. Update token in bot template's constant block
5. Save and restart agent

#### C. AutoGPT Platform Not Running
**Check:**
```bash
# Check if platform is accessible
curl http://localhost:8000
```

**Solution:**
```bash
# Start AutoGPT Platform
cd autogpt_platform
docker-compose up -d
```

---

### 2. Bot Online But Doesn't Respond

**Symptoms:**
- Bot shows as online (green dot)
- Commands don't trigger responses
- No errors visible

**Possible Causes & Solutions:**

#### A. Missing Message Content Intent
**Check:**
Discord Developer Portal → Bot → Privileged Gateway Intents

**Solution:**
1. Enable "Message Content Intent"
2. Save changes
3. Restart your bot agent
4. May take a few minutes to propagate

#### B. Missing Channel Permissions
**Check:**
Bot's role permissions in the channel

**Solution:**
1. Right-click channel → Edit Channel
2. Go to Permissions
3. Add bot's role
4. Enable:
   - View Channel
   - Read Message History
   - Send Messages
5. Save

#### C. Pattern Not Matching
**Check:**
Are you using the correct command format?

**Solution:**
Commands must start with `!` and match exactly:
- ✅ `!chat hello` - Correct
- ❌ `!Chat hello` - Wrong (case sensitive)
- ❌ `! chat hello` - Wrong (space after !)
- ❌ `chat hello` - Wrong (missing !)

---

### 3. "Invalid API Key" Errors

**Symptoms:**
- Bot responds but says "Error: Invalid API key"
- Platform logs show authentication errors
- Some commands work, others don't

**Possible Causes & Solutions:**

#### A. OpenAI API Key Not Set
**Check:**
Platform Settings → API Keys

**Solution:**
1. Go to https://platform.openai.com/api-keys
2. Create new key
3. In AutoGPT Platform → Settings → API Keys
4. Add OpenAI key
5. Restart agent

#### B. API Key Has No Credits
**Check:**
https://platform.openai.com/account/billing

**Solution:**
1. Add credits to OpenAI account
2. Check billing settings
3. Verify payment method is active

#### C. Wrong Provider Selected
**Check:**
LLM blocks in template

**Solution:**
1. Open bot template in graph editor
2. Check each LLM block
3. Verify `provider` matches your API key
4. Common providers:
   - `openai`
   - `anthropic`
   - `groq`

---

### 4. YouTube Command Not Working

**Symptoms:**
- `!youtube` command fails
- Error: "Could not fetch transcript"
- Works for some videos but not others

**Possible Causes & Solutions:**

#### A. Video Has No Captions
**Check:**
Does the YouTube video have captions?

**Solution:**
- Only works with videos that have transcripts/captions
- Try videos with auto-generated captions
- Public videos work better than private/unlisted

#### B. Video Is Restricted
**Check:**
- Age-restricted videos
- Private videos
- Region-locked content

**Solution:**
- Use public, unrestricted videos
- Ensure video is accessible without login
- Try a different video to test

#### C. URL Format Wrong
**Check:**
URL format in command

**Solution:**
Accepted formats:
- ✅ `https://www.youtube.com/watch?v=VIDEO_ID`
- ✅ `https://youtu.be/VIDEO_ID`
- ❌ `youtube.com/watch?v=VIDEO_ID` (missing https)
- ❌ `VIDEO_ID` (just the ID)

---

### 5. Search Command Returns No Results

**Symptoms:**
- `!search` command doesn't work
- No search results returned
- Generic error message

**Possible Causes & Solutions:**

#### A. Web Search Block Not Configured
**Check:**
Web search block settings

**Solution:**
1. Verify web search block (ID: 87840993-2053-44b7-8da4-187ad4ee518c)
2. Check if search API credentials are needed
3. Configure search provider in platform settings

#### B. Rate Limited
**Check:**
Platform logs for rate limit messages

**Solution:**
- Wait a few minutes
- Implement rate limiting in bot
- Reduce search frequency

#### C. No Internet Connection
**Check:**
```bash
# Test internet connectivity
curl https://www.google.com
```

**Solution:**
- Verify AutoGPT Platform has internet access
- Check firewall settings
- Verify proxy configuration if applicable

---

### 6. Bot Responds Slowly

**Symptoms:**
- Responses take >30 seconds
- Occasional timeouts
- Inconsistent response times

**Possible Causes & Solutions:**

#### A. Using Large AI Model
**Check:**
LLM block model selection

**Solution:**
Switch to faster models:
```json
{
  "model": "gpt-4o-mini"  // Faster and cheaper
}
```

Instead of:
```json
{
  "model": "gpt-4o"  // Slower but more capable
}
```

#### B. Large YouTube Videos
**Check:**
Video length

**Solution:**
- Long videos = long transcripts = slower processing
- Consider adding max length check
- Truncate very long transcripts

#### C. Platform Resource Constraints
**Check:**
```bash
# Check Docker resources
docker stats
```

**Solution:**
```bash
# Increase Docker resources
# Edit docker-compose.yml
resources:
  limits:
    cpus: '2'
    memory: 4G
```

---

### 7. Bot Sends Multiple Responses

**Symptoms:**
- Single command triggers multiple responses
- Duplicate messages
- Bot seems to "loop"

**Possible Causes & Solutions:**

#### A. Multiple Pattern Matches
**Check:**
Pattern matcher configurations

**Solution:**
Ensure patterns are mutually exclusive:
- `^!chat\\s+(.+)` - Matches only !chat
- `^!search\\s+(.+)` - Matches only !search
- No overlapping patterns

#### B. Multiple Bot Instances
**Check:**
How many times is the agent running?

**Solution:**
1. Go to AutoGPT Platform
2. Check for duplicate agents
3. Stop all instances
4. Start only one instance

---

### 8. Help Command Not Working

**Symptoms:**
- `!help` shows nothing or error
- Help text is blank

**Possible Causes & Solutions:**

#### A. Constant Block Empty
**Check:**
Help text constant block value

**Solution:**
1. Open template in editor
2. Find help-text-block
3. Verify `data` field has help text
4. Re-save if needed

#### B. Pattern Mismatch
**Check:**
Help pattern matcher

**Solution:**
Pattern should be: `^!help`
- Matches: `!help`, `!help `, `!help anything`
- Simple pattern for easy access

---

## Platform-Specific Issues

### Docker Issues

**Container Won't Start:**
```bash
# Check logs
docker-compose logs -f

# Restart services
docker-compose down
docker-compose up -d
```

**Port Already in Use:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process or change port in docker-compose.yml
```

**Database Issues:**
```bash
# Reset database
docker-compose down -v
docker-compose up -d
```

### Permission Issues

**Bot Can't Read Messages:**
1. Server Settings → Roles
2. Find bot's role
3. Enable "Read Messages"
4. Check channel-specific permissions override

**Bot Can't Send Messages:**
1. Server Settings → Roles
2. Enable "Send Messages"
3. Check channel overwrites
4. Ensure not muted/restricted

---

## Debugging Tools

### Enable Debug Logging

In AutoGPT Platform:
```json
{
  "log_level": "DEBUG"
}
```

### Check Platform Logs

```bash
# Docker deployment
docker-compose logs -f backend

# Local development
tail -f logs/autogpt_platform.log
```

### Test Individual Blocks

1. Open graph editor
2. Click on individual block
3. Use "Test" button
4. Check inputs/outputs
5. Verify behavior

### Monitor API Usage

**OpenAI:**
https://platform.openai.com/usage

**Track Costs:**
- Check daily usage
- Set spending limits
- Monitor token consumption

---

## Error Messages Reference

### "Connection timed out"
**Meaning:** Bot can't reach Discord or API  
**Fix:** Check internet, firewall, credentials

### "Rate limit exceeded"
**Meaning:** Too many requests to API  
**Fix:** Wait, implement rate limiting

### "Missing required parameter"
**Meaning:** Block missing input  
**Fix:** Check connections between blocks

### "Invalid format"
**Meaning:** Data format doesn't match expected  
**Fix:** Verify input data types

### "Permission denied"
**Meaning:** Bot lacks necessary permissions  
**Fix:** Check Discord role permissions

---

## Performance Optimization

### Reduce Response Time

1. **Use Smaller Models:**
   - gpt-4o-mini instead of gpt-4o
   - Faster, cheaper, still capable

2. **Shorter System Prompts:**
   - Keep prompts under 100 words
   - Be specific and concise

3. **Limit Token Output:**
   ```json
   {
     "max_tokens": 500
   }
   ```

4. **Cache Common Responses:**
   - Implement caching for FAQs
   - Store previous search results

### Reduce Costs

1. **Token Limits:**
   - Set max input tokens: 1000
   - Set max output tokens: 500

2. **Command Filtering:**
   - Ignore bot messages
   - Skip empty messages
   - Implement cooldowns

3. **Model Selection:**
   - Use gpt-4o-mini for most tasks
   - Reserve gpt-4o for complex queries

---

## Getting More Help

### Platform Issues
- **Docs:** https://docs.agpt.co
- **GitHub Issues:** https://github.com/Significant-Gravitas/AutoGPT/issues

### Discord Bot Issues
- **Discord.py Docs:** https://discordpy.readthedocs.io
- **Discord Developer:** https://discord.com/developers/docs

### API Issues
- **OpenAI Support:** https://help.openai.com
- **OpenAI Status:** https://status.openai.com

### Community Support
- **AutoGPT Discord:** https://discord.gg/autogpt
- **Ask in #support channel**
- **Share logs for faster help**

---

## Still Having Issues?

If you've tried everything and still can't get the bot working:

1. **Gather Information:**
   - Platform logs
   - Error messages
   - Steps to reproduce
   - Template configuration

2. **Check Similar Issues:**
   - Search GitHub issues
   - Check Discord support channel
   - Look for similar problems

3. **Ask for Help:**
   - Post in Discord #support
   - Create GitHub issue
   - Include all relevant details
   - Be specific about what you've tried

4. **Provide Context:**
   ```
   - Bot template version: v1
   - Platform version: X.X.X
   - Error message: "..."
   - Steps taken: 1. 2. 3.
   - Expected behavior: ...
   - Actual behavior: ...
   ```

---

## Prevention Tips

### Before Deploying

- [ ] Test all commands locally
- [ ] Verify API keys are valid
- [ ] Check bot permissions
- [ ] Enable debug logging
- [ ] Set up monitoring
- [ ] Document configuration
- [ ] Test error scenarios

### Regular Maintenance

- [ ] Check API usage weekly
- [ ] Review logs for errors
- [ ] Update API keys before expiry
- [ ] Monitor bot performance
- [ ] Update AutoGPT platform
- [ ] Back up configuration
- [ ] Test after updates

### Best Practices

- Use environment variables for secrets
- Implement rate limiting
- Add error handling
- Log important events
- Monitor costs
- Keep documentation updated
- Test before deploying changes

---

**Last Updated:** December 2024

Need more help? Join the [AutoGPT Discord](https://discord.gg/autogpt)!
