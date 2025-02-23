# RSS Summary

A Python-based tool that summarizes RSS feeds content automatically.

## Description

RSS Summary is a tool designed to process and summarize content from RSS feeds, making it easier to digest large amounts of information from multiple sources.

## Installation

1. Clone the repository
2. Create a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Unix/macOS
    ```
3. Install dependencies

## Configuration

Create a `config.toml` file in the root directory with your RSS feed settings (see example-config.toml for reference).

## Usage

Run the tool using:
```bash
python main.py
```

## Project Structure

```
rss_summary/
├── src/
│   └── rss_summary.py
├── .gitignore
├── main.py
└── README.md
```