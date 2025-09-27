# Bonus Examples

This folder contains additional examples showcasing advanced Agno capabilities.

## YouTube Agent (`youtube_agent.py`)

An AI assistant that extracts knowledge from YouTube videos and can answer questions about the video content.

### Features:
- **Video Transcript Processing**: Downloads and processes YouTube video transcripts
- **Searchable Video Knowledge**: Creates embeddings from video content using HuggingFace
- **Persistent Storage**: Stores video knowledge in PostgreSQL with pgvector
- **Question Answering**: Answer questions about specific video content
- **Web Search Fallback**: Can search the web for information not in the video

### Video Source:
- **Title**: "Building AI Agents with Python"
- **Author**: Arjan Codes
- **URL**: https://www.youtube.com/watch?v=D7_ipDqhtwk
- **Content**: Tutorial about building AI agents with Python, design patterns, and best practices

### Usage:
```bash
cd bonus
python youtube_agent.py
```

### Example Questions:
- "What is the main topic of the video?"
- "What Python libraries does Arjan recommend for AI agents?"
- "What are the key components of an AI agent?"
- "Can you summarize the main takeaways from the video?"

### Technical Requirements:
- PostgreSQL with pgvector extension
- HuggingFace API key (`HUGGINGFACE_API_KEY`)
- Groq API key (`GROQ_API_KEY`)
- Internet connection for video transcript download

### How It Works:
1. **Video Processing**: Uses `YouTubeReader` to download and extract transcript
2. **Embedding Creation**: Processes transcript chunks with HuggingFace embedder
3. **Vector Storage**: Stores embeddings in PostgreSQL with pgvector
4. **Knowledge Search**: Agent automatically searches video knowledge for relevant content
5. **Intelligent Responses**: Combines video knowledge with LLM reasoning

### Benefits:
- Learn from video content without watching
- Quick access to specific information from long videos
- Persistent knowledge base for future queries
- Scalable to multiple videos and sources

This example demonstrates how to build AI assistants that can extract and utilize knowledge from multimedia content, opening up possibilities for educational tools, content analysis, and knowledge management systems.