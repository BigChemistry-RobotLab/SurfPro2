from string import Template

smiles_base = "O=C(C[N+](C)(C)$n_group[N+](C)(C)CC(NC1=CC=C(O($R_group))C=C1)=O)NC2=CC=C(O($R_group))C=C2"

chains = [
    (8, 2, 8),
    (8, 4, 8),
    (8, 6, 8),
    (10, 2, 10),
    (10, 4, 10),
    (10, 6, 10),
    (12, 2, 12),
    (12, 4, 12),
    (12, 6, 12),
    (14, 2, 14),
    (14, 4, 14),
    (14, 6, 14),
    (16, 2, 16),
    (16, 4, 16),
    (16, 6, 16),
]

for c in chains:
    r_group = "C" * c[0]
    n_group = "C" * c[1]

    smiles = Template(smiles_base).safe_substitute(n_group=n_group, R_group=r_group)

    print(smiles)
