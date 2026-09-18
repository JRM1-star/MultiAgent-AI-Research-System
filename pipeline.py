from agents import build_reader_agent,build_search_agent,writer_chain,critic_chain

def run_research_pipeline(topic:str)->dict:
    state={}

    #step 1-creating search agent 
    print("\n"+"="*50)
    print("step 1 - search agent is working")
    print("="*50)

    search_agent=build_search_agent()

    search_result=search_agent.invoke({
        "messages":[("user",f"find recent,reliable and detailed information about:{topic}")]
    })

    state['search_results']=search_result['messages'][-1].content

    print("\n search result",state["search_results"])

    #step 2-creating reader agent
    print("\n"+"="*50)
    print("step 2 - Reader agent is scrapping the website")
    print("="*50)
    
    reader_agent=build_reader_agent()

    reader_result=reader_agent.invoke({
        "messages":[("user",
                    f"Based on the following search results about{topic},"
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state["search_results"][:800]}"
                    )]
    })

    state["reader_results"]=reader_result["messages"][-1].content
    
    print("\n scraped content \n",state["reader_results"])
    
    #STEP3-WRITER CHAIN
    print("\n"+"="*50)
    print("step 3 - Writer is drafting the report.....")
    print("="*50)
    
    research_combined=(
        f"SEARCH RESULTS:\n {state['search_results']} \n\n"
        f"DETAILED SCRAPPED CONTENT:\n {state['reader_results']}" 
    )
    
    state["report"]=writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })
    
    print("\n Final Report \n",state["report"])
    
    #critic report
    print("\n"+"="*50)
    print("step 4 - Critic is critizing the report.....")
    print("="*50)
    
    state["critic_result"]=critic_chain.invoke({"report":state["report"]})
    print("\n Critic Report \n",state["critic_result"])
    
    return state
    
if __name__=="__main__":
    topic=input("Enter a research topic:")
    run_research_pipeline(topic)