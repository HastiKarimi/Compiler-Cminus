# Hasti Karimi 99105656
# Negar Babashah 99109325

# 1. initialize
# 2. get first non_terminal
# 3. get a token
# 4. for current non-terminal, choose which rule to use based on the token
# 5. apply the rule (and update current non_terminal)
# 6. in cases of error, panic mode


import json

rules = []
non_terminals = {}
data = {}

starting_nt = 'Program'
epsilon_keyword = 'EPSILON'
first_keyword = 'first'
follow_keyword = 'follow'
eof_keyword = '$'

illegal_error_keyword = "illegal"
missing_error_keyword = "missing"
unexpected_error_keyword = "unexpected"

parse_tree_vertical = '│'
parse_tree_horizontal = '──'
parse_tree_corner = '└'
parse_tree_middle = '├'


def remove_duplicates(my_list):
    return list(dict.fromkeys(my_list))


def is_terminal(name: str) -> bool:
    return name not in non_terminals


class Parser:
    def __init__(self, errors_file, scanner) -> None:
        self.non_terminals = non_terminals
        self.rules = rules
        self.errors_file = errors_file
        self.initialize()
        self.current_token = None  # (type, lexeme)
        self.current_line = None
        self.scanner = scanner
        self.current_nt = self.non_terminals[starting_nt]
        self.parse_tree = []
        self.syntax_error_output = ""

    def initialize(self):
        global data
        with open("data.json", "r") as f:
            data = json.load(f)
        # TODO : in data, $ is the follow of program. But in syntax trees of test cases, it is not like that.

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
        self.update_token()
        self.call_nt(self.current_nt.name, nt_list)
        # after everything is finished, and we have probably faced $,
        # we should write syntax errors and parse tree in file
        self.write_syntax_errors()
        self.write_parse_tree()

    def call_nt(self, nt_name: str, nt_list: list):
        my_list = nt_list
        self.current_nt = non_terminals[nt_name]
        rule = self.current_nt.predict_rule(self.current_token)
        if rule is None:
            if self.current_token[0] in self.current_nt.follows:
                self.report_syntax_error(missing_error_keyword, self.current_nt.name, self.current_line)
                return  # assume that the current nt is found and we should continue
            else:
                self.report_syntax_error(illegal_error_keyword, self.current_token, self.current_line)
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
        if self.current_token[1] is eof_keyword:
            self.report_syntax_error(unexpected_error_keyword, 'EOF', self.current_line)
        elif self.current_token[0] is not terminal_action:
            self.report_syntax_error(terminal_action, self.current_token[0], self.current_line)
        self.update_token()

    def update_token(self):
        self.current_token, self.current_line = self.scanner.get_next_token(write_to_file=False)

    def report_syntax_error(self, error_type, token_name, line_number):
        error_message = "#" + str(line_number) + " : syntax error, " + str(error_type) + " " \
                        + str(token_name) + "\n"
        self.syntax_error_output += error_message

    def write_syntax_errors(self):
        if self.syntax_error_output == '':
            self.syntax_error_output = "There is no syntax error."
        self.errors_file.wirte(self.syntax_error_output)
        self.errors_file.close()  # TODO who is responsible for closing this file? Parser or compiler?

    def write_parse_tree(self):
        pass

    @staticmethod
    def draw_subtree(node, children, ancestors_open, last_child):
        # children is a list of tuples. if the child is a terminal, the tuple is (token type, lexeme)
        # if the child is a non-terminal, the tuple is (node name, [its children])
        Parser.print_node_line(ancestors_open, last_child, node)

        ancestors_open.append(last_child)
        for index in range(len(children)):
            child = children[index]
            if type(child[1]) == list:
                # means the child was a non-terminal
                next_node = child[0]
                next_children = child[1]
                next_last_child = (index == len(children) - 1)
                Parser.draw_subtree(node=next_node, children=next_children, ancestors_open=ancestors_open,
                                    last_child=next_last_child)
            else:
                # the child is a terminal
                next_node = child
                next_children = []
                next_last_child = (index == len(children) - 1)
                Parser.draw_subtree(node=next_node, children=next_children, ancestors_open=ancestors_open,
                                    last_child=next_last_child)

    @staticmethod
    def print_node_line(ancestors_open, last_child, node):
        line = ''
        for ancestor_index in range(len(ancestors_open) - 1):
            is_open = ancestors_open[ancestor_index]
            if is_open:
                line += parse_tree_vertical
            else:
                line += ' '
            line += '   '
        if last_child:
            line += parse_tree_corner
        else:
            line += parse_tree_middle
        line += parse_tree_horizontal
        if is_terminal(node):
            line += ' (' + str(node[0]) + ', ' + str(node[1]) + ')'
        else:
            line += str(node)
        print(line)


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
            if (self.epsilon_rule is None) and (epsilon_keyword in rule_firsts):
                self.epsilon_rule = i
            rules[i].set_first(rule_firsts)

    def find_rule_firsts(self, rule_id: int) -> list[str]:
        rule = rules[rule_id]

        if rule.get_actions()[0] == epsilon_keyword:  # the rule itself is epsilon
            return rule.get_actions()

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
                        rule_first += [val for val in action_first if val != epsilon_keyword]
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
            if current_token[0] in rule.firsts:
                return rule_id
        return self.epsilon_rule
        # it's either None or one of the rules that has epsilon in its first set


