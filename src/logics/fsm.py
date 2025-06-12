import json
import os

class FSM:

    def __init__(self, path = "rsc/fsm_def.json"):
        self.path = path
        self.__init_fsm(self.__load_json_file())

    def __load_json_file(self) -> dict:
        assert self.path.endswith(".json"), "'path' must be a JSON file path!"
        assert os.path.exists(self.path), "File not found! 'path' must be a valid file path!"
        with open(self.path, encoding="utf-8") as f:
            try:
                fsm_json = json.load(f)
            except:
                raise ValueError("'path' is not a valid JSON file!")
        return fsm_json

    def __init_fsm(self, data: dict) -> tuple:
        required_keys = ["states", "alphabet", "initialState", "acceptStates", "transitions","state_questions"]
        for key in required_keys:
            assert key in data, "Missing '" + key + "' key in the JSON file!"

        #initializa FSM attributes
        self.states = data["states"]
        self.alphabet = data["alphabet"]
        self.initial_state = data["initialState"]
        self.accept_states = data["acceptStates"]
        self.state_questions = data["state_questions"]
        #create transition matrix
        self.transitions = {}
        for transition in data["transitions"]:
            from_state = transition["from"]
            input_symbol = transition["input"]
            to_state = transition["to"]
            self.transitions[(from_state, input_symbol)] = to_state

        #set current state to initial state
        self.current_state = self.initial_state

    def next_step(self, label: str) -> bool:
        current_state = self.current_state
        try:
            self.current_state = self.transitions[(current_state, label)]
        except:
            # undefined transition or symbol not in the alphabet
            raise ValueError(f"Undefined transition from state '{self.current_state}' with input '{label}'!")
        return self.current_state in self.accept_states

    def get_current_state(self) -> str:
        return self.current_state

    def is_in_accepting_state(self):
        return self.current_state in self.accept_states



if __name__ == "__main__":
 
    fsm = FSM("rsc/fsm_def.json")
    print(fsm.get_current_state())

    print(fsm.next_step("valid_name"))
    print(fsm.get_current_state())
    print(fsm.is_in_accepting_state())
