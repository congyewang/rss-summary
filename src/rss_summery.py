import feedparser
from openai import OpenAI
from html import unescape
import tomllib
from typing import Dict


class RSSSummarizer:
    def __init__(self) -> None:
        self.config = self.read_config()
        self.client = self.make_client()
        self.feed = self.make_feed()

    def read_config(
        self, config_path: str = "config.toml"
    ) -> Dict[str, str | int | float]:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)

        type_checks = {
            "rss_url": str,
            "model": str,
            "api_key": str,
            "base_url": str,
            "prompt": str,
            "temperature": float,
            "max_tokens": int,
            "timeout": int,
        }

        for field, expected_type in type_checks.items():
            if not isinstance(config[field], expected_type):
                raise ValueError(
                    f"The {field} field must be a {expected_type.__name__}"
                )

        return config

    def clean_html(self, text: str) -> str:
        """
        Simple HTML tag cleanup function to remove tags and entities from text content and convert line breaks and paragraphs to newlines for better readability.

        Args:
            text (str): The text to clean up with HTML tags and entities

        Returns:
            str: The cleaned text with line breaks  and paragraphs converted to newlines
        """
        return unescape(text).replace("<br>", "\n").replace("</p>", "\n\n")

    def summarize_with_llm(self, content: str, client: OpenAI) -> str:
        """
        Summarization using OpenAI-compatible APIs.

        Args:
            content (str): The content to summarize
            client (OpenAI): The OpenAI client instance

        Returns:
            str: The summarized content
        """
        response = client.chat.completions.create(
            model=self.config["model"],
            messages=[
                {
                    "role": "system",
                    "content": self.config["prompt"],
                },
                {"role": "user", "content": content},
            ],
            temperature=self.config["temperature"],
            max_tokens=self.config["max_tokens"],
            timeout=self.config["timeout"],
        )

        return response.choices[0].message.content

    def make_client(self) -> OpenAI:
        """
        Create an OpenAI client instance.

        Returns:
            OpenAI: The OpenAI client instance
        """
        client = OpenAI(
            base_url=self.config["base_url"],
            api_key=self.config["api_key"],
        )

        return client

    def make_feed(self) -> feedparser.FeedParserDict:
        """
        Parse the RSS feed.

        Returns:
            feedparser.FeedParserDict: The parsed RSS feed
        """
        feed = feedparser.parse(self.config["rss_url"])

        return feed

    def run(self) -> None:
        """
        Run the summarization process.
        """
        for i, entry in enumerate(self.feed.entries[:5]):  # 限制前5篇防止过量
            try:
                content = f"{entry.title}\n\n{self.clean_html(entry.description)}"

                summary = self.summarize_with_llm(content[:3000], self.client)

                print(f"📰 第 {i+1} 篇总结：")
                print(summary)
                print("\n" + "-" * 50 + "\n")

            except Exception as e:
                print(f"处理第 {i+1} 篇时出错：{str(e)}")
