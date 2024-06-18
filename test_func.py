from helpers import (
    query_you_com,
    query_tavily,
    query_perplexity,
)  # , brave_search_summarization,


def test_queries():
    test_query = "How is the weather in Palo Alto, CA?"

    print("Testing You.com API:")
    # you_com_result = query_you_com(test_query)
    you_com_result = query_you_com(test_query)
    print(you_com_result["answer"])

    print("\nTesting Tavily.com API:")
    tavily_result = query_tavily(test_query)
    print(tavily_result["answer"])

    print("\nTesting Perplexity.ai API:")
    perplexity_result = query_perplexity(test_query)
    print(perplexity_result)

    # print("\nTesting Brave.com API:")
    # brave_result = brave_search_summarization(test_query)
    # print(brave_result)
    
def test_brave_ai_wrapper():
    # Initialize the BraveAIWrapper with your API key
    api_key = "your_api_key_here"
    brave_ai = BraveAIWrapper(api_key=api_key)

    # Define the test query
    query = "What is some of the best mountain biking near Crested Butte, CO?"

    # Test get_brave_results
    print("Testing get_brave_results...")
    results = brave_ai.get_brave_results(query)
    if results:
        print("get_brave_results output:", json.dumps(results, indent=2))
    else:
        print("get_brave_results failed.")

    # Test get_and_summarize
    print("\nTesting get_and_summarize...")
    summary = brave_ai.get_and_summarize(query)
    if summary:
        print("get_and_summarize output:", summary)
    else:
        print("get_and_summarize failed.")

    # Test download_documents
    print("\nTesting download_documents...")
    documents = brave_ai.download_documents(query)
    if documents:
        for doc in documents:
            print("Document metadata:", doc.metadata)
            print("Document content:", doc.page_content[:200])  # Print first 200 characters
            print("-" * 40)
    else:
        print("download_documents failed.")


if __name__ == "__main__":
    test_queries()
    test_brave_ai_wrapper()
