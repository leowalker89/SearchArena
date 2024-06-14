from helpers import query_you_com, query_tavily, query_perplexity #, brave_search_summarization,

def test_queries():
    test_query = "How is the weather in Palo Alto, CA?"

    print("Testing You.com API:")
    # you_com_result = query_you_com(test_query)
    you_com_result = query_you_com(test_query)
    print(you_com_result['answer'])

    print("\nTesting Tavily.com API:")
    tavily_result = query_tavily(test_query)
    print(tavily_result['answer'])

    print("\nTesting Perplexity.ai API:")
    perplexity_result = query_perplexity(test_query)
    print(perplexity_result)

    # print("\nTesting Brave.com API:")
    # brave_result = brave_search_summarization(test_query)
    # print(brave_result)

if __name__ == "__main__":
    test_queries()
