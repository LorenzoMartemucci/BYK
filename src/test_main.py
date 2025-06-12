from src.logics.tutorial_logic import TutorialLogic
import json


robby = TutorialLogic()
print(robby.start_game())
while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Uscita dal programma.")
        break
   
    response = robby.process_input(user_input)
    print(f"Robby: {response}")
    if robby.is_tutorial_completed():
        print("- Prompt recap: ",robby.prompt_recap())
        rewritten_prompt = robby.rewrite_prompt()
        print(f"Robby: {rewritten_prompt}")
        print("Robby: Esegui il prompt seguente:")
        response = robby.exec_prompt(rewritten_prompt)
        print(f"Robby: {response}")
        break

