import pandas as pd

df = pd.read_csv("source_data/guo2011_table_1.csv")

for i, row in df.iterrows():
    tail_1 = row.Tail_1
    tail_2 = row.Tail_2
    ion_1 = row.Ion_1
    ion_2 = row.Ion_2
    spacer = row.Spacer

    print(tail_1, ion_1, spacer, ion_2, tail_1)
