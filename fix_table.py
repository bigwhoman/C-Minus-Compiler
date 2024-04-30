file = open("parse_table.txt")
fixed = open("fixed_table.txt",'+w')
for line in file.readlines() : 
    x = line.split("->")
    splited = [x[1]]
    if '|' in x[1] : 
        splited = x[1].split('|')
    for loo in splited :
        print(f'{x[0]} -> {loo}')
        fixed.write(f'{x[0]} -> {loo}\n')
