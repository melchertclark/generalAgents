# Gemini Polling with gemini-cli

UNFINISHED UNFINISHED UNFINISHED

This polling script monitors Limitless AI lifelogs for "Gemini" mentions and uses `gemini-cli` to provide intelligent responses via NTFY notifications.

## Setup Instructions

### 1. Install gemini-cli

Choose one of these installation methods:

**Option A: Global installation (recommended)**
```bash
npm i -g @google/gemini-cli
```

**Option B: One-time run (good for CI/containers)**
```bash
npx https://github.com/google-gemini/gemini-cli
```

### 2. Authenticate gemini-cli

**For interactive use (first time setup):**
```bash
gemini  # Opens browser for OAuth authentication
```

**For headless/unattended scripts:**
```bash
export GEMINI_API_KEY="your_ai_studio_or_vertex_key"
```

The API key approach skips all interactive prompts and works in cron/docker/K8s environments.

### 3. Test the Integration

Run the test script to verify everything is working:

```bash
python test_gemini_cli.py
```

This will:
- Check if gemini-cli is installed and accessible
- Verify your authentication setup
- Test the polling engine integration
- Confirm gemini-cli can respond to queries

### 4. Run the Polling Engine

**Test mode (check current transcript context):**
```bash
python gemini_polling.py test
```

**Normal operation (start polling):**
```bash
python gemini_polling.py
```

## How It Works

1. **Polling**: The script continuously monitors your Limitless AI lifelogs
2. **Trigger Detection**: When "Gemini" is mentioned in any lifelog, it triggers analysis
3. **Context Gathering**: The script collects the day's transcript context (limited to 96,000 chars)
4. **AI Analysis**: gemini-cli analyzes the context and provides a focused response
5. **Notification**: The response is sent via NTFY to your mobile device

## Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Gemini API key for headless operation
- The script uses the same Limitless API key and NTFY configuration as before

### Rate Limits

- **Personal Gmail auth**: 60 requests/min & 1,000/day
- **API key auth**: Follows your AI Studio/Vertex quotas
- The script includes basic retry/backoff logic

## Troubleshooting

### Common Issues

**"gemini-cli not found"**
```bash
npm i -g @google/gemini-cli
```

**Authentication errors**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Timeout errors**
- The script has a 60-second timeout for gemini-cli responses
- Check your internet connection and API key validity

### Debug Mode

Run the test script to diagnose issues:
```bash
python test_gemini_cli.py
```

## Features

- **Smart Context Management**: Limits context to prevent token overflow
- **Duplicate Prevention**: Avoids processing the same Gemini trigger multiple times
- **Error Handling**: Graceful error handling with NTFY notifications
- **Transcript Logging**: Maintains daily transcript files with organized folder structure
- **Mobile-Optimized**: Responses are formatted for mobile notifications

## File Structure

```
liminigent/
├── gemini_polling.py      # Main polling script with gemini-cli integration
├── test_gemini_cli.py     # Test script for verification
├── README_gemini_cli.md   # This file
└── logs/                  # Daily transcript files (auto-generated)
    └── YYYY/MM/DD/
        └── transcript.txt
```

## Migration from Previous Version

If you were using the previous poll agent version:

1. The script automatically detects and uses gemini-cli instead
2. No changes needed to your existing configuration
3. Transcript files and polling logic remain the same
4. Only the AI analysis backend has changed from poll_agent1 to gemini-cli

## Advanced Usage

### Custom gemini-cli Options

You can modify the `run_gemini_cli_query` method in `gemini_polling.py` to add additional gemini-cli flags:

```python
result = subprocess.run([
    "gemini", 
    "--model", "gemini-2.5-pro",  # Specify model (default)
    "--debug",                    # Enable debug mode
    "--sandbox"                   # Run in sandbox mode
], ...)
```

**Note**: The `--no-ansi` and `--stream=false` flags mentioned in the gemini-cli documentation may not be available in all versions. The script uses the basic `gemini` command which automatically detects non-TTY input and runs in headless mode.

### Structured Output

For structured responses, you can modify the prompt to request JSON:

```python
gemini_query = f"""... your prompt ...

Please respond in valid JSON format with keys: analysis, action_items, confidence
"""
```

## Support

For gemini-cli specific issues, check the [official documentation](https://github.com/google-gemini/gemini-cli).

For polling script issues, check the logs in the `logs/` directory for detailed error information. 