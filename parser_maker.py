import csv 
import pandas 
import re
import numpy as np
from string import Template
from pprint import pprint
def remove_brackets(value):
    if len(value) > 0 and '{' == value[0] and '}' == value[-1] :
        value = value[1:-1]
    return value

def remove_tt(value):
    if '::=' in value :
        return value.split('::=')[1]
    else :
        return value
    
def change_commas(value):
    secondary = value.replace(","," ")
    if ', ,' in value :
        secondary += " ,"
    return secondary

def change_epsilon(value):
    if "''" in value :
        value = value.replace("''","EPSILON")
    return value

def tokenize(input_string, tokens):
    pprint(tokens)
    input_string = input_string.strip()
    print(input_string)
    result = []
    for token in tokens:
        if input_string.startswith(token):
            result.append(token)
            input_string = input_string[len(token):]
    return result

ffff = open('table_text.txt','w+')
df = pandas.read_csv('parse_table.csv') 

df.fillna("", inplace=True)
# df = df.map(remove_brackets)
df = df.map(remove_tt)
df = df.map(change_commas)
df = df.map(change_epsilon)

terminals = [
]
non_terminals = [
]

for index, row in df.iterrows():
    follow_symbols = []
    non_terminals.append(row['Nonterminal'])
    for column in df.columns:
        if column == 'Follow' :
           follow_symbols = row[column].split()
        elif column not in ["First","Nonterminal"] :
            if column not in terminals :
                terminals.append(column)
            if row[column] == "" and column in follow_symbols:
                # print(row["Nonterminal"], column)
                row[column] = "Synch"

# pprint(non_terminals)
# pprint(terminals)

ffff.write(df.to_string())


func_template = """
def {func}() :
    {func_body}
    
"""
func_bode_template = """
\tif lookahead in {terminal_list} :
{do_sth}
"""
all_code = ""
match_function = """
def Match(expected_token : str) :
    if lookahead == expected_token :
        lookahead = get_next_token()
    else :
        print("Missing input ...")
"""
all_code += match_function

for index, row in df.iterrows():
    classification = {}
    # print(row["Nonterminal"], "---->")
    for col in df.columns:
        if col not in ["First","Nonterminal","Follow"] :
            value = df.loc[index, col]
            # Check if the value exists in the DataFrame
            if value in df.values:
                # If the value exists, add it to the classification
                if value not in classification:
                    classification[value] = [col]
                else:
                    classification[value].append(col)
    
    func_body = ""

    for key in classification.keys() :
        tt = func_bode_template
        temporal_body = ""
        if key.strip() == '' :
            temporal_body = f"""
\t\tprint('Invalid character at ...')
\t\tlookahead = get_next_token()
\t\t{row["Nonterminal"]}()
"""
        elif key.strip() == 'Synch' :
            temporal_body = f"""
\t\tprint('Missing character at ...')
\t\treturn
"""           
        elif key.strip() == 'EPSILON' :
            temporal_body = f"""
\t\treturn
"""
        else :
            tokens = key.split()
            for token in tokens :
                if token in terminals :
                    temporal_body += f"\t\tMatch('{token}')\n"
                elif token in non_terminals :
                    temporal_body += f"\t\t{token}()\n"
        func_body += tt.format(terminal_list=classification[key], do_sth=temporal_body)
    func = func_template.format(func=row["Nonterminal"], func_body=func_body)
    # print(func)
    all_code += func

python_file = open('c_parser.py','w+')
python_file.write(all_code)


