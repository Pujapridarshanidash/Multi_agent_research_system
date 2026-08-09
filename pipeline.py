
from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain
)


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # ============================================================
    # STEP 1 - SEARCH AGENT
    # ============================================================

    print("\n" + "=" * 50)
    print("Step 1 - Search Agent is working...")
    print("=" * 50)

    search_agent = build_search_agent()

    search_result = search_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    topic
                )
            ]
        }
    )

    # Get final Search Agent response
    research = search_result["messages"][-1].content

    state["topic"] = topic
    state["search_results"] = research

    print("\nSearch Agent completed successfully.\n")


    # ============================================================
    # STEP 2 - READER AGENT
    # ============================================================

    print("\n" + "=" * 50)
    print("Step 2 - Reader Agent is scraping top resources...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"""
Based on the following search results about '{topic}',
pick the most relevant URLs and scrape them for deeper content.

Search Results:
{state["search_results"][:800]}
"""
                )
            ]
        }
    )

    reader_research = reader_result["messages"][-1].content

    state["scraped_content"] = reader_research

    print("\nReader Agent completed successfully.\n")


   ### write report

    print("\n" + "=" * 50)
    print("Step 3 - Writer is drafting the report...")
    print("=" * 50)

    # Combine search results + detailed scraped content
    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n"
        f"{state['scraped_content']}"
    )

    writer_result = writer_chain.invoke(
        {
            "topic": topic,
            "research": research_combined
        }
    )

    state["report"] = writer_result

    print("\nWriter Chain completed successfully.\n")


    # ============================================================
    # critic report
    # ============================================================

    print("\n" + "=" * 50)
    print("Step 4 - Critic is reviewing the report...")
    print("=" * 50)

    critic_result = critic_chain.invoke(
    {
        "topic": state["topic"],
        "research": state["scraped_content"],
        "report": state["report"]
    }
)

    state["critic_report"] = critic_result

    print("\nCritic completed successfully.\n")

    print("=" * 50)
    print("CRITIC REPORT")
    print("=" * 50)

    print(state["critic_report"])
    
    return state
    

    

if __name__ == "__main__":

    topic = input("Enter your research topic: ")

    run_research_pipeline(topic)

    # print("\n" + "=" * 50)
    # print("FINAL RESEARCH REPORT")
    # print("=" * 50)

    # print(result["report"])

    # print("\n" + "=" * 50)
    # print("CRITIC REPORT")
    # print("=" * 50)

    # print(result["critic_report"])
