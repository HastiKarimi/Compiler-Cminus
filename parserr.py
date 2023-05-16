import json

data = {}
with open("data.json", "r") as f:
    data = json.load(f)


production_rules_file = open("rules.txt", "r")
production_rule_lines = production_rules_file.readlines()

non_terminals = {}
rule_index = 0
rules = []

for production_rule in production_rule_lines:
    nt, right_side = production_rule.split("->")
    nt = nt.strip()
    right_side = right_side.strip().split("|")
    nt_rule_list = []
    for rule in right_side:
        the_rule = Rule(rule_index, rule.strip().split(" "))
        rules.append(the_rule)
        nt_rule_list.append(rule_index)
        rule_index += 1

    non_terminals[nt] = Nonterminal(nt, nt_rule_list)
    
    




# non_terminal = {"Define": NoneTerminal()}

# class NoneTerminal:
#     def __init__(self, name, rules):
#         self.name = name
#         rules = [1, 5, 8] 
#         first
#         follow
    

# nt -> a1a2a3 | b1b2b3 | ...
# a1 -> asdf | 



# def find_first:



# class Rule:
#     nt_or_terminals = ['a1', 'a2', 'a3']
#     first = []
#     use():
#         a1()
#         a2()
#         a3()
    



# 1. initialize 
# 2. get first non_terminal
# 3. get a token
# 4. for current non terminal, choose which rule to use based on the token
# 5. apply the rule (and update current non_terminal)
# 6. in cases of error, panic mode




class Rule:
    def __init__(self, rule_id: int, actions: list[str]):
        self.actions = actions
        self.id = rule_id
        self.firsts = find_rule_firsts(rule_id)

    def apply(self):
        for action in self.actions:
            if is_terminal(action):
                match_token(action)
        

class Nonterminal:
    def __init__(self, name: str, rule_ids: list[int]):
        self.name = name
        self.rule_ids = rule_ids
        self.firsts = find_nt_firsts(name)
        self.follows = find_nt_follows(name)

    def predict_rule(self) -> int:
        # predicts the id of the rule to apply based on the current token
        pass
    
    def proceed_transition(self):
        applying_rule_id = self.predict_rule()
        rule = rules[applying_rule_id]
        rule.apply()
        # todo error recovery process


def find_nt_firsts(nt_name:str) -> list[str]:
    pass # todo implement

def find_nt_follows(nt_name: str) -> list[str]:
    pass # todo implement

def find_rule_firsts(rule_id: int) -> list[str]:
    pass # todo implement

def is_terminal(name: str) -> bool:
    pass # todo implement

def match_token(terminal: str):
    pass # todo implement