from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3")

choice_template = """
Answer the question below.
Here is the conversation history: {context}
Question: {question}
Choices: {choices}
Answer: (provide multiple answers if applicable, separated by commas,  and give reasons for each answer and print text from context which affected your result): 
"""
choice_prompt = ChatPromptTemplate.from_template(choice_template)
choice_chain = choice_prompt | model

quest_template = """
Answer the question below.
Here is the conversation history: {context}
Question: {question}
Answer: 
"""   
quest_prompt = ChatPromptTemplate.from_template(quest_template)
quest_chain = quest_prompt | model

def read_context_from_file(file_path):
    with open(file_path, 'r') as file:
        context = file.read()
    return context

def add_to_context(result):
    add = input("Do you want to add result to context? (yes/no) ")
    if add.lower() == "yes":
        context = context + result

def get_choices():
    choices = []
    print("Please provide the choices for the prompt. Type 'done' when finished.")
    while True:
        choice = input("Enter a choice: ")
        if choice.lower() == "done":
            break
        choices.append(choice)
    return choices

def get_question():
    question = input("Please enter your question: ")
    return question

def multiple_choice_flow():
     while True:
        question = get_question()
        choices = get_choices()
        print("Getting answers from the model...")
        result = choice_chain.invoke({"context": context, "question": question, "choices": "\n".join(choices)})
        print(f"Debug: Model result: {result}")
        add_to_context(result)
        continue_input = input("Do you want to continue? (yes/no): ")
        if continue_input.lower() == "yes":
            continue
        else:
            break
 
def question_ans_flow():
     while True:
        question = get_question()
        print("Getting answers from the model...")
        result = quest_chain.invoke({"context": context, "question": question})
        print(f"Debug: Model result: {result}")
        add_to_context(result)
        continue_input = input("Do you want to continue? (yes/no): ")
        if continue_input.lower() == "yes":
            continue
        else:
            break

def handle_conversation():
    context = read_context_from_file('context.txt')
    print("Welcome to Mobot! Type 'exit' to quit")
    while True:
        opt = input("Do you want to QnA or Multiple choice QnA (choice/quest) or exit to quit: ")
        if opt.lower() == "choice":
            multiple_choice_flow()
        elif opt.lower() == "quest":
            question_ans_flow()
        elif opt.lower() == "exit":
            break
        else:
            print("Invalid choice. Please try again.")
            continue
   

if __name__ == "__main__":
    handle_conversation()