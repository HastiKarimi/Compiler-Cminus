# 1. initialize 
# 2. get first non_terminal
# 3. get a token
# 4. for current non terminal, choose which rule to use based on the token
# 5. apply the rule (and update current non_terminal)
# 6. in cases of error, panic mode


import json


rules = []
non_terminals = {}
data = {}
parser = Parser(non_terminals, rules)


class Parser:
    def __init__(self, non_teminals_dict, rules_list) -> None:
        self.non_terminals = non_teminals_dict
        self.rules = rules_list
        self.initialize()
        self.current_token = None
        self.current_nt = self.non_terminals["Program"]


    def initialize(self):
        global data
        with open("data.json", "r") as f:
            data = json.load(f)


        production_rules_file = open("rules.txt", "r")
        production_rule_lines = production_rules_file.readlines()

        
        rule_index = 0

        for production_rule in production_rule_lines:
            nt, right_side = production_rule.split("->")
            nt = nt.strip()
            right_side = right_side.strip().split("|")
            nt_rule_list = []
            for rule in right_side:
                the_rule = Rule(rule_index, rule.strip().split(" "))
                self.rules.append(the_rule)
                nt_rule_list.append(rule_index)
                rule_index += 1

            self.non_terminals[nt] = Nonterminal(nt, nt_rule_list)

    def run(self):
        pass

    def call_nt(self, nt_name: str):
        self.current_nt = non_terminals[nt_name]
        rule = self.current_nt.predict_rule(self.current_token)
        # todo in parse tree, set the actions of rule as the children of current_nt



    def find_nt_firsts(self, nt_name:str) -> list[str]:
        pass # todo implement

    def find_nt_follows(self, nt_name: str) -> list[str]:
        pass # todo implement


    def is_terminal(self, name: str) -> bool:
        pass # todo implement

    def match_token(sefl, terminal: str):
        pass # todo implement
        
    

class Rule:
    def __init__(self, rule_id: int, actions: list[str]):
        self.actions = actions
        self.id = rule_id
        self.firsts = []
        # self.firsts = parser.find_rule_firsts(rule_id)

    def get_actions(self):
        return self.actions

    def set_first(self, list_firsts: list[str]):
        self.firsts = list_firsts

    def apply(self):
        for action in self.actions:
            if parser.is_terminal(action):
                parser.match_token(action)
            else:
                parser.call_nt(action)
                
        

class Nonterminal:
    def __init__(self, name: str, rule_ids: list[int]):
        self.name = name
        self.rule_ids = rule_ids
        self.firsts = data['first'][self.name]
        self.follows = data['follow'][self.name]
        for i in rule_ids:
            rules[i].set_first(self.find_rule_firsts(i))

    def find_rule_firsts(self, rule_id: int) -> list[str]:
        rule = rules[rule_id]
        if rule.get_actions()[0] == 'EPSILON':
            return data['follow'][self.name]

        # TODO handle if every action has epsilon
        first_rule = []
        for action in rule.get_actions():
            if action not in non_terminals:
                first_rule.append(action)
                return first_rule
            else:
                # then action is a non-terminal
                first_action = data['first'][action]
                if 'EPSILON' in first_action:
                    first_rule = first_action.remove('EPSILON') + first_rule
                else:
                    first_rule = first_action + first_rule
                    return first_rule

        return first_rule


    def predict_rule(self, current_token: str) -> int:
        # predicts the id of the rule to apply based on the current token
        pass
    
    def proceed_transition(self):
        applying_rule_id = self.predict_rule()
        rule = rules[applying_rule_id]
        rule.apply()
        # todo error recovery process


