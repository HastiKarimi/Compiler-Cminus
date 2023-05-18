# Hasti Karimi 99105656
# Negar Babashah 99109325

# 1. initialize
# 2. get first non_terminal
# 3. get a token
# 4. for current non-terminal, choose which rule to use based on the token
# 5. apply the rule (and update current non_terminal)
# 6. in cases of error, panic mode


import json


def remove_duplicates(my_list):
    return list(dict.fromkeys(my_list))


def is_terminal(name: str) -> bool:
    return name in non_terminals


class Parser:
    def __init__(self, non_terminals_dict, rules_list, errors_file) -> None:
        self.non_terminals = non_teminals_dict
        self.rules = rules_list
        self.errors_file = errors_file
        self.initialize()
        self.current_token = None
        self.current_line = None
        self.scanner = None  # todo
        self.current_nt = self.non_terminals["Program"]
        self.parse_tree = []

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
        nt_list = []
        self.parse_tree.append((self.current_nt.name, nt_list))
        self.call_nt(self.current_nt.name, nt_list)

    def call_nt(self, nt_name: str, nt_list: list):
        my_list = nt_list
        self.current_nt = non_terminals[nt_name]
        rule = self.current_nt.predict_rule(self.current_token)
        if rule is None:
            if self.current_token in self.current_nt.follows:
                self.report_missing_token(self.current_token.name, self.current_line)
                return  # assume that the current nt is found and we should continue
            else:
                self.report_illegal_token(self.current_token, self.current_line)
                self.update_token()  # assume there was an illegal input and ignore it
                self.call_nt(nt_name, nt_list)
                return

        my_list.extend(rule.get_actions())
        for i in range(len(my_list)):
            action = my_list[i]
            if is_terminal(action):
                self.match_action(action)
            else:
                child_nt_list = []
                my_list[i] = (action, child_nt_list)
                self.call_nt(action, child_nt_list)

    def match_action(self, terminal_action: str):
        # TODO what happens if current token is $?
        if self.current_token is not terminal_action:
            self.report_missing_token(self.current_token, self.current_line)
        self.update_token()

    def update_token(self):
        self.current_token, self.current_line = self.scanner.get_next_token()

    def report_missing_token(self, missing_token_name: str, line_number: int):
        error_message = "#" + str(line_number) + " : syntax error, missing " + str(missing_token_name)
        self.errors_file.write(error_message)

    def report_illegal_token(self, illegal_token: str, line_number: int):
        error_message = "#" + str(line_number) + " : syntax error, illegal " + str(missing_token_name)
        self.errors_file.write(error_message)


class Rule:
    def __init__(self, rule_id: int, actions: list[str]):
        self.actions = actions
        self.id = rule_id
        self.firsts = []

    def get_actions(self):
        return self.actions

    def set_first(self, list_firsts: list[str]):
        self.firsts = list_firsts


class Nonterminal:
    def __init__(self, name: str, rule_ids: list[int]):
        self.name = name
        self.rule_ids = rule_ids
        self.firsts = data[first_keyword][self.name]
        self.follows = data[follow_keyword][self.name]
        self.epsilon_rule = None
        for i in rule_ids:
            rule_firsts = self.find_rule_firsts(i)
            if not self.has_epsilon_rule and epsilon_keyword in rule_firsts:
                self.epsilon_rule = i
            rules[i].set_first(rule_firsts)

    def find_rule_firsts(self, rule_id: int) -> list[str]:
        rule = rules[rule_id]

        if rule.get_actions()[0] == epsilon_keyword:  # the rule itself is epsilon
            return rule.get_actions

        rule_first = []
        actions = rule.get_actions()
        for index in range(len(actions)):
            action = actions[index]
            if is_terminal(action):
                rule_first.append(action)
                return remove_duplicates(rule_first)
            else:
                # then action is a non-terminal
                action_first = data[first_keyword][action]
                if epsilon_keyword in action_first:
                    if index is not len(action) - 1:
                        rule_first += action_first.remove(epsilon_keyword)
                    else:
                        # If we're here, all the actions were terminals that contained epsilon in their firsts.
                        # So epsilon must be included in rule_first
                        rule_first += action_first
                else:
                    rule_first = action_first + rule_first
                    remove_duplicates(rule_first)

        return remove_duplicates(rule_first + data[follow_keyword][self.name])

    def predict_rule(self, current_token: str) -> int:
        # predicts the id of the rule to apply based on the current token. If no rule was found, return None
        for rule_id in self.rule_ids:
            rule = rules[rule_id]
            if current_token in rule.firsts:
                return rule_id
        return self.epsilon_rule
        # it's either None or one of the rules that has epsilon in its first set


rules = []
non_terminals = {}
data = {}
epsilon_keyword = 'EPSILON'
first_keyword = 'first'
follow_keyword = 'follow'
errors_file = open("syntax_errors.txt", "w+")
parser = Parser(non_terminals, rules, errors_file)
