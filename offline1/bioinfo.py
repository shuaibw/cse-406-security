from prettytable import PrettyTable
from termcolor import colored
import os
os.system('color')
cols = ['(A(B(C,D)))', '((A,C)(B,D))', '(C(A(B,D)))']
rows = ['(A(B(C,D)))', '(A(C(B,D)))', '(A(D(C,B)))', '(B(A(C,D)))', '(B(C(A,D)))', '(B(D(C,A)))', '(C(A(B,D)))',
        '(C(B(A,D)))', '(C(D(B,A)))', '(D(A(B,C)))', '(D(B(A,C)))', '(D(C(B,A)))', '((A,B)(C,D))', '((A,C)(B,D))', '((A,D)(C,B))']
table=PrettyTable()
id=0
table.field_names = ['ID','GeneTree', 'SpeciesTree']
for c in cols:
    for r in rows:
        id+=1
        table.add_row([colored(id, 'white'),colored(c, 'blue'),colored(r, 'green')])
print(table)