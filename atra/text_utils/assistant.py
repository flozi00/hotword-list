from typing import Iterable
from sentence_transformers import util, SentenceTransformer
from huggingface_hub import InferenceClient
import torch
from playwright.sync_api import sync_playwright
import urllib.parse
from enum import Enum

from atra.text_utils.prompts import ASSISTANT_TOKEN, CLASSIFY_SEARCHABLE, END_TOKEN, QUERY_PROMPT, SEARCH_PROMPT, USER_TOKEN

import os
import argilla as rg

try:
    rg.init(
        api_url=os.environ.get("ARGILLA_API_URL"),
        api_key=os.environ.get("ARGILLA_API_KEY"),
        workspace="argilla",
    )
except Exception as e:
    print(e)

class Plugins(Enum):
    LOKAL = "lokal"
    SEARCH = "search"

class Agent:
    def __init__(self, llm: InferenceClient, embedder: SentenceTransformer):
        self.embedder = embedder
        self.llm = llm

    def classify_plugin(self, history: str) -> Plugins:
        """
        Classifies the plugin based on the given history.

        Args:
            history (str): The history to classify the plugin for.

        Returns:
            Plugins: The plugin that matches the searchable answer.
        """
        searchable_answer = self.llm.text_generation(
            prompt=CLASSIFY_SEARCHABLE.replace("<|question|>", history),
            temperature=0.1,
            stop_sequences=["\n", END_TOKEN],
            max_new_tokens=3,
        )

        for plugin in Plugins:
            if plugin.value.lower() in searchable_answer.lower():
                search_query_record = rg.Text2TextRecord(text=history, prediction=[searchable_answer],)
                rg.log(search_query_record, "plugin_record")
                return plugin
            
    def generate_search_query(self, history: str) -> str:
        """
        Generates a search query based on the given history using the LLM.

        Args:
            history (str): The history to use as context for generating the search query.

        Returns:
            str: The generated search query.
        """
        search_query = self.llm.text_generation(
            prompt=QUERY_PROMPT.replace("<|question|>", history),
            stop_sequences=["\n", END_TOKEN],
        ).strip()
        search_query_record = rg.Text2TextRecord(text=history, prediction=[search_query],)
        rg.log(search_query_record, "search_query_record")
        return search_query
    
    def generate_search_question(self, history: str) -> str:
        """
        Generates a search question based on the given history using the LLM.
        
        Args:
            history (str): The history to use as context for generating the search question.
            
        Returns:
            str: The generated search question.
        """
        search_question = self.llm.text_generation(
            prompt=SEARCH_PROMPT.replace("<|question|>", history),
            stop_sequences=["\n", END_TOKEN],
        ).strip()
        search_question_record = rg.Text2TextRecord(text=history, prediction=[search_question],)
        rg.log(search_question_record, "search_question_record")
        return search_question
    
    def do_qa(self, question: str, context: str) -> Iterable[str]:
        """
        Generates an answer to a question based on the given context using the LLM.
        
        Args:
            question (str): The question to be answered.
            context (str): The context to use for answering the question.
            
        Returns:
            str: The generated answer.
        """
        text = ""
        QA_Prompt = USER_TOKEN + context + "\nQuestion: " + "\n\n" + question + "\n\nAnswer in german plain text:" + END_TOKEN + ASSISTANT_TOKEN
        answer = self.llm.text_generation(
            prompt=QA_Prompt,
            max_new_tokens=512,
            temperature=0.1,
            stop_sequences=["<|", END_TOKEN],
            stream=True,
        )

        for token in answer:
            text += token
            yield text
        
        record = rg.Text2TextRecord(
            text=QA_Prompt,
            prediction=[text],
        )
        rg.log(record, "qa_record")

        return text

    def re_ranking(self, query: str, options: list) -> str:
        """
        Re-ranks a list of options based on their similarity to a given query.

        Args:
            query (str): The query to compare the options against.
            options (list): A list of strings representing the options to be ranked.

        Returns:
            str: A string containing the top-ranked options that have a cosine similarity score greater than 0.7.
        """
        corpus = ["passage: " + o for o in options]
        query = "query: " + query

        filtered_corpus = []

        corpus_embeddings = self.embedder.encode(corpus, convert_to_tensor=True)
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)

        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=20 if len(corpus) > 20 else len(corpus))

        for score, idx in zip(top_results[0], top_results[1]):
            if score > 0.7:
                filtered_corpus.append(corpus[idx])

        return "\n".join(filtered_corpus)
    
    def get_webpage_content_playwright(self, query: str) -> str:
        """
        Uses Playwright to launch a Chromium browser and navigate to a search engine URL with the given query.
        Returns the filtered and re-ranked text content of the webpage.

        Args:
        - query (str): The search query to be used in the URL.

        Returns:
        - filtered (str): The filtered and re-ranked text content of the webpage.
        """
        url = (
            "https://searx.be/search?categories=general&language=de&q="
            + urllib.parse.quote(query)
        )
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            content = page.locator("body").inner_text()
            browser.close()

        content = content.split("\n")
        filtered = ""
        for co in content:
            if len(co.split(" ")) > 5:
                filtered += co + "\n"

        filtered = self.re_ranking(query, filtered.split("\n"))

        return filtered
    
    def custom_generation(self, query) -> Iterable[str]:
        text = ""
        result = self.llm.text_generation(
            prompt=query,
            max_new_tokens=512,
            temperature=0.6,
            stop_sequences=["<|", END_TOKEN],
            stream=True,
        )
        for token in result:
            text += token

            yield text

        record = rg.Text2TextRecord(
            text=query,
            prediction=[text],
        )
        rg.log(record, "chat_record")

        yield text