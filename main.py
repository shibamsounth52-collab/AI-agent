
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

@tool
def calculator(a: float, b: float, ) -> str:
    """useful for performing basic arithmetic calculations with number"""
    print("tool has been called.")
    return f"the sum of {a} and {b} is {a+b}"
@tool
def say_hello(name:str)->str:
    """useful for greeting a user"""
    print("tool has been called.")
    return f"hello {name},i hope you are well today"


def main():
    model=ChatOpenAI(temperature=0)
    tools=[calculator,say_hello]
    agent_executer=create_react_agent(model,tools)
    print("hi this my agent ask anything in text. to exit type 'exit' or 'quit'")
    print("you can ask me to perform calculations or greet you by name.")
    
    while True:
        user_input=input("\nYOu:" ).strip()
        
        if user_input.lower() in ['exit','quit']:
            print("good bye!")
            break

        print("\nAssistant: ",end="")

        for chunk in agent_executer.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent"in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
            
                        
        print()  # print a newline after the response is complete



if __name__ == "__main__":
    main()