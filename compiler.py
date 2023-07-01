from scanner import Scanner
from parserr import Parser
from symbol_table import SymbolTable

# initialize a scanner and call get_next_token repeatedly

in_file = open("input.txt", "r")
out_file = open("tokens.txt", "w+")
lex_file = open("lexical_errors.txt", "w+")
sym_file = open("symbol_table.txt", "w+")
parser_errors_file = open("syntax_errors.txt", "w+")
parser_tree_file = open("parse_tree.txt", "w+", encoding='utf-8')

symbol_table = SymbolTable()

scanner = Scanner(
    input_file=in_file,
    output_file=out_file,
    lex_file=lex_file,
    sym_file=sym_file,
    symbol_table=symbol_table
)


parser = Parser(errors_file=parser_errors_file, parse_tree_file=parser_tree_file, scanner=scanner)
parser.run()

in_file.close()
out_file.close()
lex_file.close()
sym_file.close()
parser_errors_file.close()

