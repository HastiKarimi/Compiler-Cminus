from scanner import Scanner
from parserr import Parser
from symbol_table import SymbolTable
from heap_manager import HeapManager
from code_generator import CodeGenerator

# initialize a scanner and call get_next_token repeatedly

in_file = open("input.txt", "r")
out_file = open("tokens.txt", "w+")
lex_file = open("lexical_errors.txt", "w+")
sym_file = open("symbol_table.txt", "w+")
parser_errors_file = open("syntax_errors.txt", "w+")
parser_tree_file = open("parse_tree.txt", "w+", encoding='utf-8')

heap = HeapManager()
symbol_table = SymbolTable(heap)

scanner = Scanner(
    input_file=in_file,
    output_file=out_file,
    lex_file=lex_file,
    sym_file=sym_file,
    symbol_table=symbol_table
)


code_generator = CodeGenerator(symbol_table=symbol_table, heap=heap)


parser = Parser(errors_file=parser_errors_file, parse_tree_file=parser_tree_file,
                scanner=scanner, code_gen=code_generator)
parser.run()


in_file.close()
out_file.close()
lex_file.close()
sym_file.close()
parser_errors_file.close()

for row in symbol_table.table:
    print(row)

code_generator.print_pb()

