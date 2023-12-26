# agent.py
import sys
import requests
import autogen
import os

def initiate_chat(message):
    os.environ["OPENAI_API_KEY"] = "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"

    # only configured for chat gpt-3.5-turbo-1106
    config_list_gpt4 = autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={
            "model": ["gpt-3.5-turbo"],
        },
    )

    gpt4_config = {
        "seed": 42,  # change the seed for different trials
        "temperature": 0.5,
        "config_list": config_list_gpt4,
        "timeout": 120,
        "max_tokens": 200,
    }
    user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False,
    )
    cto = autogen.AssistantAgent(
        name="CTO",
        system_message="CTO. State your name first. Check the plan and provide feedback from a technical persepctive. Suggest how to build the solution. CTO needs to approve the plan.",
        llm_config=gpt4_config
    )


    cfo = autogen.AssistantAgent(
        name="CFO",
        system_message="CFO. State your name first. Check the plan and provide feedback from a financial persepctive. Suggest how to build the business case. CFO needs to approve the plan.",
        llm_config=gpt4_config,
    )

    cpo = autogen.AssistantAgent(
        name="CPO",
        system_message="CPO. State your name first. Check the plan and provide feedback from a people persepctive. Suggest what capabilities are required to deliver the plan.",
        llm_config=gpt4_config,

    )
    ceo = autogen.AssistantAgent(
        name="CEO",
        system_message='''Planner. Suggest a plan. Be Creative within reason.
        Revise the plan based on feedback from admin, CFO, CPO and critic, until admin approval.
        Explain the plan first. be clear about the problem, solution, and how to measure success.
    ''',
        llm_config=gpt4_config,
    )

    critic = autogen.AssistantAgent(
        name="Critic",
        system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
        llm_config=gpt4_config,
    )
    groupchat = autogen.GroupChat(
        agents=[user_proxy, cfo, ceo ],
            messages=[],
            max_round=3)
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

    conversation = {}

    autogen.ChatCompletion.start_logging(history_dict=conversation)

    response = user_proxy.initiate_chat(
        manager,
        message=message,
        silent=True
    )

    autogen.ChatCompletion.stop_logging()    

    return conversation

def respond(message):
    # This is where you would implement your agent's response logic
    response = initiate_chat(message)

    return response

if __name__ == "__main__":
    message = sys.argv[1]
    response = respond(message)
