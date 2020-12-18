from tabulate import tabulate
    
def printTable(*arg):
    row_header = ["Alice's Bits", "Alice's Bases", "Encoded Qubits", "Eve's Bases", "Bob's Bases", "Bob's Bits",
            "Alice's Sifted Bits", "Bob's Sifted Bits", "Alice's Bits After Disclosure", 
            "Bob's Bits After Disclosure", "Alice's Key After CASCADE", "Bob's Key After CASCADE",
            "Alice's Final Key", "Bob's Final Key"]

    arguments = list(locals().values())[0]
    lists = [arguments[i] for i in range(len(arguments))]
    strLists = ((''.join(str(j) for j in i)) for i in lists)


    table = [list(i) for i in zip(row_header, strLists)]

    with open('table.txt', 'w') as f:
        f.write(tabulate(table, tablefmt = 'fancy_grid'))
		
