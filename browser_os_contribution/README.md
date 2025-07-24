# Local GPT Agent for BrowserOS 🤖

**Privacy-first AI assistant with voice control and LinkedIn automation**

This contribution adds two powerful features to BrowserOS:

1. **🎤 Local GPT Form-Filling Agent** - Voice-controlled, privacy-first form filling using Ollama and RAG pipeline
2. **🔗 LinkedIn Easy Apply Automation** - Intelligent workflow automation for job applications

## ✨ Features

### Local GPT Form-Filling Agent
- **🔒 Privacy-First**: All AI processing happens locally using Ollama (no cloud dependencies)
- **🎙️ Voice Control**: "Fill this form" - agent fills forms intelligently based on your context
- **🧠 RAG Pipeline**: Learns from your previous form submissions for better suggestions
- **👀 DOM Watching**: Automatically detects forms and suggests completions
- **💾 Local Storage**: User context stored locally with ChromaDB vector database

### LinkedIn Easy Apply Automation
- **🚀 Workflow Recording**: Record manual applications once, replay for similar jobs
- **🤖 Screening Questions**: AI-powered responses to common screening questions
- **📊 Application Tracking**: Track applications, success rates, and follow-ups
- **⚡ Smart Matching**: Match jobs to existing workflows based on company/role patterns
- **🛡️ Rate Limiting**: Respectful automation with built-in rate limiting

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        BrowserOS                            │
├─────────────────────────────────────────────────────────────┤
│  Browser Extension (JavaScript)                             │
│  ├─ Content Script (DOM monitoring)                         │
│  ├─ Background Script (message routing)                     │
│  └─ Native Messaging Host (Python bridge)                  │
├─────────────────────────────────────────────────────────────┤
│  Local GPT Agent (Python)                                  │
│  ├─ VoiceProcessor (speech recognition)                     │
│  ├─ RAGPipeline (context + embeddings)                     │
│  ├─ DOMWatcher (form detection)                            │
│  └─ FormFiller (intelligent completion)                    │
├─────────────────────────────────────────────────────────────┤
│  LinkedIn Automation (Python)                              │
│  ├─ LinkedInDetector (job page detection)                  │
│  ├─ WorkflowEngine (record/replay workflows)               │
│  ├─ ScreeningHandler (AI-powered responses)                │
│  └─ ApplicationTracker (status management)                 │
├─────────────────────────────────────────────────────────────┤
│  Local AI Stack                                            │
│  ├─ Ollama (LLM inference)                                 │
│  ├─ ChromaDB (vector storage)                             │
│  └─ SpeechRecognition (voice input)                       │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

1. **BrowserOS** - Build and install BrowserOS following [BUILD.md](https://github.com/browseros-ai/BrowserOS/blob/main/docs/BUILD.md)
2. **Ollama** - Install and run locally:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3.2
   ```
3. **Python 3.11+** with pip

### Installation

1. **Clone this contribution**:
   ```bash
   git clone <your-fork-url>
   cd browser-os-local-gpt-agent
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup native messaging host**:
   ```bash
   python browser_os_integration.py --setup-native-host
   ```

4. **Install browser extension in BrowserOS**:
   - Open BrowserOS
   - Navigate to `browser://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `browser_extension` folder

### Configuration

1. **Initialize user context**:
   ```bash
   python setup_user_context.py
   ```
   This will prompt you to enter your personal information for form filling.

2. **Test the installation**:
   ```bash
   python test_integration.py
   ```

## 📖 Usage

### Voice Commands

Once activated, use these voice commands:

- **"Fill this form"** - Auto-fill the current form with your context
- **"Save this workflow"** - Save current form interaction as reusable workflow  
- **"Start applying"** - Begin LinkedIn Easy Apply automation
- **"Stop watching"** - Deactivate DOM monitoring
- **"Application summary"** - Get summary of recent applications

### Manual Activation

- **Keyboard shortcut**: `Ctrl+Shift+G` to toggle agent
- **Extension popup**: Click the extension icon in BrowserOS toolbar
- **Context menu**: Right-click on forms for AI suggestions

### LinkedIn Automation

1. Navigate to LinkedIn job search results
2. Say "Start applying" or click the extension popup
3. The agent will:
   - Detect Easy Apply opportunities
   - Check if you've already applied
   - Use existing workflows or record new ones
   - Handle screening questions intelligently
   - Track application status

## 🔧 Configuration Options

Edit `config.json` to customize behavior:

```json
{
  "privacy_mode": true,
  "voice_activation": true,
  "auto_suggest": true,
  "linkedin_automation": {
    "enabled": true,
    "max_applications_per_day": 25,
    "min_delay_between_applications": 30,
    "respect_rate_limits": true
  },
  "ollama": {
    "model": "llama3.2",
    "host": "localhost:11434"
  },
  "voice": {
    "language": "en-US",
    "continuous_listening": true
  }
}
```

## 🛡️ Privacy & Security

- **100% Local Processing**: No data sent to external servers
- **Encrypted Storage**: User context encrypted at rest
- **Minimal Permissions**: Extension requests only necessary permissions
- **Rate Limiting**: Respectful automation to avoid being blocked
- **Audit Logs**: All actions logged locally for transparency

## 🚀 Development

### Project Structure

```
browser-os-local-gpt-agent/
├── local_gpt_agent.py          # Core AI agent
├── linkedin_workflow_automation.py  # LinkedIn automation
├── browser_os_integration.py   # BrowserOS integration layer
├── browser_extension/          # Browser extension files
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   └── popup.html
├── native_host/               # Native messaging host
├── requirements.txt
├── config.json
└── tests/
```

### Running Tests

```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests (requires BrowserOS)
python -m pytest tests/integration/

# End-to-end tests
python -m pytest tests/e2e/
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes following the code style
4. Add tests for new functionality
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 🔍 How It Works

### Form Detection & Filling

1. **DOM Monitoring**: Content script continuously monitors for form elements
2. **Field Classification**: AI classifies fields (name, email, address, etc.)
3. **Context Retrieval**: RAG pipeline retrieves relevant user context
4. **Smart Completion**: Ollama generates appropriate field values
5. **Confidence Scoring**: Only high-confidence suggestions are applied

### LinkedIn Automation

1. **Page Detection**: Identifies LinkedIn job pages and Easy Apply buttons
2. **Workflow Matching**: Finds existing workflows for similar roles/companies
3. **Dynamic Execution**: Handles varying form structures and screening questions
4. **Learning Loop**: Records successful patterns for future use
5. **Compliance**: Respects rate limits and terms of service

### Voice Processing Pipeline

1. **Speech Recognition**: Converts voice to text using SpeechRecognition
2. **Intent Classification**: Ollama classifies user intent from command
3. **Action Routing**: Routes to appropriate handler (form fill, automation, etc.)
4. **Feedback Loop**: Provides audio/visual confirmation of actions

## 🐛 Troubleshooting

### Common Issues

**"Native host not found"**
```bash
# Reinstall native messaging host
python browser_os_integration.py --setup-native-host --force
```

**"Ollama not responding"**
```bash
# Check Ollama status
ollama list
ollama serve

# Test model
ollama run llama3.2 "Hello"
```

**"Voice recognition not working"**
```bash
# Check microphone permissions
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"

# Test speech recognition
python test_voice.py
```

**"Extension not loading"**
- Ensure BrowserOS is in developer mode
- Check extension developer console for errors
- Verify manifest.json syntax

### Debug Mode

Enable debug logging:
```bash
export LOCAL_GPT_DEBUG=1
python browser_os_integration.py
```

### Performance Optimization

For better performance:
- Use smaller Ollama models like `llama3.2:1b` for faster inference
- Increase `context_cache_size` in config for better RAG performance
- Disable continuous listening if not needed

## 📊 Metrics & Analytics

The agent tracks (locally):
- Forms filled successfully
- Voice commands processed
- LinkedIn applications submitted
- Workflow success rates
- Response time metrics

View analytics:
```bash
python analytics.py --report
```

## 🤝 Acknowledgments

- [BrowserOS](https://github.com/browseros-ai/BrowserOS) - Privacy-first browser platform
- [Ollama](https://ollama.com/) - Local LLM inference
- [ChromaDB](https://www.trychroma.com/) - Vector database for RAG
- [Stagehand.dev](https://stagehand.dev/) - Inspiration for browser automation patterns

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚧 Roadmap

- [ ] **Multi-language Support** - Voice commands in multiple languages
- [ ] **Advanced Workflows** - Complex multi-step automation patterns  
- [ ] **Mobile Integration** - Extend to mobile BrowserOS
- [ ] **Plugin Ecosystem** - Allow third-party form handlers
- [ ] **Advanced Analytics** - ML-powered success predictions
- [ ] **Collaborative Learning** - Anonymous pattern sharing (opt-in)

---

**Built with ❤️ for the BrowserOS community**

*Making browser automation intelligent, private, and accessible through voice.*