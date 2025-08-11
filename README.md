# A2A CR Box - Enterprise Content Discovery Agent

A professional enterprise content discovery assistant powered by Gemini, specializing in Box content search and enterprise document management.

## 🚀 Features

### Core Capabilities
- **Box Content Search**: Find files, documents, and folders in Box
- **Box AI Ask**: Ask intelligent questions about specific file content
- **Box Hub Ask**: Automatically discover and use the most relevant Box Hub
- **Enterprise Content Discovery**: Locate specific documents, regulatory files, reports, and business content
- **Professional Communication**: Business-appropriate responses with enterprise focus

### Tools Available
1. **Box Search** - Find documents and files across your Box enterprise
2. **Box AI Ask** - Ask questions about specific file content using Box AI
3. **Box Hub Ask** - Automatically discover and use the most relevant knowledge hub
4. **Weather** - Location-based weather queries

## 🏗️ Architecture

- **Google ADK (Agent Development Kit)**: Powers the GeminiAgent
- **Box Python SDK**: Handles Box API authentication and operations
- **JWT Authentication**: Secure server-to-server authentication with Box
- **Cloud Run**: Deployed as a scalable containerized service
- **AgentSpace Integration**: Ready for Discovery Engine registration

## 🔧 Setup

### Prerequisites
- Python 3.9+
- Google Cloud Platform account
- Box Developer account with JWT app credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd A2A_CR_Box
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Box JWT Authentication**
   - Copy `box_jwt_config.example.json` to `box_jwt_config.json`
   - Fill in your Box JWT app credentials:
     - `clientID`
     - `clientSecret`
     - `enterpriseID`
     - `publicKeyID`
     - `privateKey`
     - `passphrase`

4. **Set environment variables**
   ```bash
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   export GOOGLE_CLOUD_LOCATION="us-central1"
   export GOOGLE_GENAI_USE_VERTEXAI="TRUE"
   export MODEL="gemini-2.5-flash"
   ```

## 🚀 Deployment

### Local Development
```bash
python -m uvicorn agent_executor:app --reload
```

### Cloud Run Deployment
```bash
./deploy.sh <project-id> <service-name>
```

### AgentSpace Registration
After deployment, register your agent in Google Cloud Discovery Engine:
```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://discoveryengine.googleapis.com/v1alpha/projects/<PROJECT_ID>/locations/global/collections/default_collection/engines/<ENGINE_ID>/assistants/default_assistant/agents" \
  -d '{
    "name": "Box_Search_Agent",
    "displayName": "Box Search Agent",
    "description": "Enterprise content discovery agent for Box",
    "a2aAgentDefinition": {
      "jsonAgentCard": "{\"provider\": {\"url\": \"<YOUR_CLOUD_RUN_URL>\"},\"name\": \"box_search_agent\",\"description\": \"A Box search assistant that helps you find content in your Box enterprise\"}"
    }
  }'
```

## 📖 Usage Examples

### Box Content Search
```
User: "Find regulatory documents"
Agent: [Searches Box and returns organized results with file counts and details]
```

### Box AI Ask
```
User: "What are the key points in Capital Call Notice.pdf?"
Agent: [Uses Box AI to analyze the specific file and provide insights]
```

### Box Hub Ask
```
User: "What are our company policies?"
Agent: [Automatically discovers relevant hubs and provides answers from the best knowledge base]
```

## 🔒 Security

- **JWT Authentication**: Secure server-to-server authentication
- **Environment Variables**: Sensitive configuration stored securely
- **Box API Permissions**: Minimal required permissions for enterprise access
- **Cloud Run Security**: No unauthenticated access, secure by default

## 🛠️ Development

### Project Structure
```
A2A_CR_Box/
├── agent_executor.py      # Main A2A executor
├── gemini_agent.py        # Gemini agent with tools
├── box_auth.py           # Box JWT authentication
├── box_search.py         # Box content search
├── box_ai_ask.py         # Box AI file analysis
├── box_hub_ask.py        # Box Hub discovery and querying
├── requirements.txt      # Python dependencies
├── deploy.sh            # Cloud Run deployment script
└── README.md            # This file
```

### Adding New Tools
1. Create your tool function in a new Python file
2. Import it in `gemini_agent.py`
3. Add it to the `tools` list
4. Update the agent instructions
5. Add corresponding skills

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the logs in Google Cloud Console
- Review Box API documentation
- Check Google ADK documentation

## 🔄 Version History

- **v1.0.0**: Initial release with Box search and AI capabilities
- **v1.1.0**: Added Box Hub Ask functionality
- **v1.2.0**: Enhanced enterprise focus and professional communication
