
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv
import streamlit as st

# ============================================================
# LOAD API KEY - Works on both LOCAL and STREAMLIT CLOUD
# ============================================================

# Try to load from Streamlit Secrets first (for cloud)
# Fall back to .env file (for local development)
try:
    mistral_api_key = st.secrets["MISTRAL_API_KEY"]
except:
    # Fall back to .env file for local development
    load_dotenv()
    mistral_api_key = os.getenv("MISTRAL_API_KEY")

# Verify API key is set
if not mistral_api_key:
    raise ValueError(
        "MISTRAL_API_KEY not found! "
        "Please set it in Streamlit Secrets (cloud) or .env file (local)"
    )

# ============================================================
# INITIALIZE LLM WITH API KEY
# ============================================================

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    api_key=mistral_api_key  # ← Explicitly pass the API key
)

# ============================================================
# SEARCH AGENT
# ============================================================

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )


# ============================================================
# READER AGENT
# ============================================================

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


# ============================================================
# WRITER CHAIN
# ============================================================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert research writer. Write clear, structured, and insightful reports.
Your task is to write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual, and professional."""
    ),
    ("human", "Write the research report.")
])

writer_chain = writer_prompt | llm | StrOutputParser()

# ============================================================
# CRITIC CHAIN
# ============================================================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert research critic and fact-checker.

Your task is to critically review the research report given below.
Identify factual problems, missing information, unsupported claims,
poor reasoning, and areas that need improvement.

Topic:
{topic}

Research Gathered:
{research}

Research Report:
{report}

Evaluate the report based on:

- Factual accuracy
- Relevance to the topic
- Completeness
- Quality of reasoning
- Clarity and structure
- Unsupported or hallucinated claims
- Proper use of research sources
- Whether the important findings are properly explained

Provide your review in the following structure:

1. Overall Assessment
2. Strengths
3. Issues and Errors
4. Missing Information
5. Unsupported Claims
6. Suggested Improvements
7. Final Verdict

Be critical, factual, and specific.
Do not rewrite the entire report.
Only provide constructive feedback for improving the report."""
    ),
    (
        "human",
        "Critically review the research report."
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()