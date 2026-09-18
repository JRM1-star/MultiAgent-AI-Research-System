# Multi-Agent Research Assistant

[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/built%20with-LangChain-1c3c3c)](https://python.langchain.com/)
[![Groq](https://img.shields.io/badge/inference-Groq-orange)](https://groq.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

An automated research pipeline that searches the web, scrapes the most relevant source, and produces a structured, critiqued report — all driven by cooperating LLM agents built with LangChain and Groq.

## Features

- 🔍 **Automated web search** for recent, reliable sources on any topic
- 📄 **Smart scraping** — pulls full content from the most relevant result
- ✍️ **Structured report generation** (Introduction, Key Findings, Conclusion, Sources)
- 🧠 **Self-critique loop** — a second agent scores and reviews the report before you see it
- ⚡ **Fast inference** via Groq's `openai/gpt-oss-120b`

## How It Works

The pipeline runs four stages in sequence:

```
User Topic
    │
    ▼
┌─────────────────┐
│  Search Agent    │  Tavily web search → list of candidate sources
└────────┬─────────┘
         ▼
┌─────────────────┐
│  Reader Agent    │  Picks best URL, scrapes with BeautifulSoup
└────────┬─────────┘
         ▼
┌─────────────────┐
│  Writer Chain    │  Synthesizes into a structured report
└────────┬─────────┘
         ▼
┌─────────────────┐
│  Critic Chain    │  Scores report, lists strengths/gaps, gives verdict
└────────┬─────────┘
         ▼
   Final Result
```

1. **Search Agent** — Uses Tavily web search to find recent, reliable sources on the given topic.
2. **Reader Agent** — Picks the most relevant URL from the search results and scrapes its full content with BeautifulSoup.
3. **Writer Chain** — Synthesizes the search results and scraped content into a structured report (Introduction, Key Findings, Conclusion, Sources).
4. **Critic Chain** — Reviews the report and returns a score out of 10, strengths, areas to improve, and a one-line verdict.

Each stage's output feeds into the next, and the final state (search results, scraped content, report, and critique) is returned as a dictionary.

## Project Structure

```
.
├── agents.py         # Agent + chain definitions (search, reader, writer, critic)
├── pipeline.py       # Orchestrates the full research pipeline
├── tools.py          # web_search (Tavily) and scrape_url (BeautifulSoup) tools
├── app.py            # Entry point / app interface
├── pyproject.toml    # Project metadata and dependencies (uv)
├── uv.lock           # Locked dependency versions
└── requirements.txt  # Pip-installable dependency list
```

## Tech Stack

- **[LangChain](https://python.langchain.com/)** — agent orchestration and prompt chains
- **[Groq](https://groq.com/)** (`openai/gpt-oss-120b`) — LLM inference
- **[Tavily](https://tavily.com/)** — web search API
- **BeautifulSoup4** — web scraping and text extraction
- **python-dotenv** — environment variable management

## Prerequisites

- Python >= 3.12
- A [Groq API key](https://console.groq.com/)
- A [Tavily API key](https://tavily.com/)

## Setup

### 1. Clone the repository

```bash
it clone https://github.com/JRM1-star/MultiAgent-AI-Research-System.git
cd MultiAgent-AI-Research-System
```

### 2. Install dependencies

Using `uv` (recommended, matches the lockfile):

```bash
uv sync
```

Or using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Usage

Run the pipeline directly:

```bash
python pipeline.py
```

You'll be prompted to enter a research topic, and the pipeline will print progress for each stage (search → scrape → write → critique) followed by the final report and critique.

You can also import and call the pipeline programmatically:

```python
from pipeline import run_research_pipeline

result = run_research_pipeline("The impact of AI on renewable energy")
print(result["report"])
print(result["critic_result"])
```

### Example Output

```
$ python pipeline.py
Enter a research topic: The impact of AI on renewable energy

[1/4] Searching for sources...      ✓ 5 results found
[2/4] Scraping top source...        ✓ 2,847 characters extracted
[3/4] Writing report...             ✓ Report generated
[4/4] Critiquing report...          ✓ Score: 8/10

=== REPORT ===
# The Impact of AI on Renewable Energy
## Introduction
...

=== CRITIQUE ===
Score: 8/10
Strengths: Clear structure, well-sourced claims
Areas to improve: Could include more quantitative data
Verdict: Solid overview report, ready for review
```

## Output

`run_research_pipeline()` returns a dictionary with:

| Key | Description |
|---|---|
| `search_results` | Raw search results from the Search Agent |
| `reader_results` | Scraped content from the Reader Agent |
| `report` | Final structured research report |
| `critic_result` | Score, strengths, areas to improve, and verdict |

## Configuration

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | API key for Groq LLM inference |
| `TAVILY_API_KEY` | Yes | API key for Tavily web search |

## Troubleshooting

| Issue | Likely Cause | Fix |
|---|---|---|
| `AuthenticationError` from Groq | Missing/invalid `GROQ_API_KEY` | Check `.env` is loaded and key is correct |
| Empty or irrelevant search results | Tavily rate limit or vague topic | Narrow the topic string, check Tavily quota |
| Scraped content is empty | Target site blocks scrapers / uses JS rendering | BeautifulSoup can't render JS — try a different source or add a headless-browser fallback |
| Report cuts off mid-sentence | Content truncation at 3,000 characters | Increase the truncation limit in `tools.py` if you need more context |

## Roadmap

- [ ] Support multiple scraped sources instead of just the top result
- [ ] Configurable output formats (Markdown, PDF, JSON)
- [ ] Swap-in support for other LLM providers (OpenAI, Anthropic)
- [ ] Caching layer to avoid re-searching the same topic

## Contributing

Contributions are welcome. Please open an issue to discuss significant changes before submitting a pull request.

## Notes

- Requires Python >= 3.12.
- API keys for Groq and Tavily are required — get them from [console.groq.com](https://console.groq.com/) and [tavily.com](https://tavily.com/).
- The scraper truncates page content to 3,000 characters to keep context manageable.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
