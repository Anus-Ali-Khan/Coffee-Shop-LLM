from agents import GuardAgent,ClassificationAgent,DetailsAgent,AgentProtocol,RecommendationAgent,OrderTakingAgent
import os
import pathlib
folder_path = pathlib.Path(__file__).parent.resolve()





def main():
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()

    agent_dict : dict[str,AgentProtocol] = {
        "details_agent" : DetailsAgent(),
        "recommendation_agent" :  RecommendationAgent(
        os.path.join(folder_path, 'recommendation_objects/apriori_recommendations.json'),
        os.path.join(folder_path, 'recommendation_objects/popularity_recommendation.csv')
    ),
        "order_taking_agent" : OrderTakingAgent() 
    }

    messages = []
    while True:
        # Flush output
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n\n Print Messages ........")
        for message in messages:
            print(f"{message['role']}: {message['content']}")

        # Get user input
        prompt = input("User: ")
        messages.append({"role":"user","content":prompt})

        # Get Guard Agent's response
        guard_agent_response = guard_agent.get_response(messages)
        
        if guard_agent_response["memory"]["guard_decision"] == "not allowed":
            messages.append(guard_agent_response)[0]
            continue

        # Get Classification Agent's Response
        classification_agent_response = classification_agent.get_response(messages)
        chosen_agent = classification_agent_response["memory"]["classification_decision"]
        # print("Chosen Agent: ", chosen_agent)


        # Get the chosen agents's reponse
        agent = agent_dict[chosen_agent]
        response = agent.get_response(messages)
        k

        messages.append(response)

if __name__ == "__main__":
    main()

   
    
   
         

