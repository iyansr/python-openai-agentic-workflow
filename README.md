# Agentic Workflow

An AI-powered content generation system that automates research, writing, and publishing workflows using FastAPI and Celery.

## Overview

This project implements an agentic workflow for creating SEO-optimized blog posts. It leverages multiple AI models and web search to:

1. **Research** topics using Tavily search API
2. **Generate** detailed content outlines
3. **Write** full draft articles
4. **Optimize** content for SEO
5. **Publish** as formatted PDF documents

## Architecture

The system follows a modular, asynchronous architecture:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│   FastAPI   │────▶│    Celery   │────▶│  Content Task   │
│   (HTTP)    │     │   (Queue)   │     │   (Async)       │
└─────────────┘     └─────────────┘     └─────────────────┘
                                                │
                    ┌─────────────┬─────────────┼─────────────┐
                    ▼             ▼             ▼             ▼
              ┌─────────┐   ┌──────────┐  ┌──────────┐  ┌──────────┐
              │ Tavily  │   │  OpenAI  │  │  OpenAI  │  │  PDF     │
              │ Search  │   │ Research │  │  Writer  │  │ Export   │
              └─────────┘   └──────────┘  └──────────┘  └──────────┘
```

## Features

- **Automated Research**: Web search with AI-powered summarization
- **Structured Outlines**: AI-generated content outlines with sections and key points
- **Draft Writing**: Full blog post generation based on outlines
- **SEO Optimization**: Automatic keyword research and content optimization
- **PDF Publishing**: Convert final content to PDF format
- **Async Processing**: Background task execution via Celery
- **API Documentation**: Interactive API docs via Scalar

## Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **Celery**: Distributed task queue for async processing
- **Redis**: Message broker and result backend
- **OpenAI API**: LLM for content generation (via OpenRouter)
- **Tavily**: Web search API for research
- **WeasyPrint**: HTML to PDF conversion
- **Pydantic**: Data validation and serialization
- **UV**: Fast Python package manager

## Prerequisites

- Python >= 3.14.2
- Redis server running locally or accessible
- API keys for OpenRouter and Tavily

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd agentic-workflow
```

2. Install dependencies using UV:
```bash
uv sync
```

3. Create a `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
```

4. Ensure Redis is running:
```bash
redis-server
```

## Usage

### Start the Development Server

```bash
make dev
```

This starts the FastAPI server with auto-reload on `http://localhost:8000`.

### Start the Celery Worker

In a separate terminal:

```bash
make celery
```

### Generate Content

Send a POST request to create content:

```bash
curl -X POST http://localhost:8000/content \
  -H "Content-Type: application/json" \
  -d '{"topic": "The Future of AI Agents"}'
```

The task will be processed asynchronously, and a PDF will be generated in the project root.

### API Documentation

Visit `http://localhost:8000/scalar` for interactive API documentation.

## Project Structure

```
agentic-workflow/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── celery_app.py        # Celery configuration
│   ├── modules/
│   │   └── content/
│   │       ├── __init__.py
│   │       ├── schema.py    # Pydantic models
│   │       ├── tasks.py     # Celery tasks
│   │       ├── method.py    # Content generation logic
│   │       └── prompt.py    # System prompts for AI
│   └── utils/
│       ├── __init__.py
│       ├── openai.py        # OpenAI client configuration
│       └── tavily.py        # Tavily client configuration
├── pyproject.toml           # Project dependencies
├── Makefile                 # Development commands
└── README.md
```

## Workflow Pipeline

1. **Research Phase** (`research_topic`)
   - Search web using Tavily API
   - Summarize findings with AI

2. **Outline Phase** (`generate_outline`)
   - Generate structured outline
   - Include meta description and sections

3. **Draft Phase** (`write_draft`)
   - Write full blog post based on outline
   - Maintain professional tone and structure

4. **SEO Phase** (`seo_optimize`)
   - Identify primary and secondary keywords
   - Optimize title, meta, and content
   - Generate URL slug

5. **Publish Phase** (`publish_post`)
   - Format for final publication
   - Convert to PDF using WeasyPrint

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenRouter API key | Yes |
| `TAVILY_API_KEY` | Tavily search API key | Yes |
| `REDIS_URL` | Redis connection URL | No (defaults to localhost) |

## Models Used

- **Research**: `qwen/qwen3.5-flash-02-23` - Fast summarization
- **Outline/Draft**: `openai/gpt-oss-120b` - Long-form content generation
- **SEO/Publish**: `openai/gpt-4o` - High-quality optimization
