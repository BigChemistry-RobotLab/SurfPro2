from string import Template

temp = Template(
    "${R}Oc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)${S}(=O)Nc2ccc(O${R})cc2)cc1.[Br-].[Br-]"
)

codes = {
    "8-2-8": (8, 2),
    "8-4-8": (8, 4),
    "8-6-8": (8, 6),
    "10-2-10": (10, 2),
    "10-4-10": (10, 4),
    "10-6-10": (10, 6),
    "12-2-12": (12, 2),
    "12-4-12": (12, 4),
    "12-6-12": (12, 6),
    "14-2-14": (14, 2),
    "14-4-14": (14, 4),
    "14-6-14": (14, 6),
    "16-2-16": (16, 2),
    "16-4-16": (16, 4),
    "16-6-16": (16, 6),
}

for c in codes:
    smiles = temp.substitute(R=codes[c][0]*"C", S=codes[c][1]*"C")
    print(smiles)

"""
CCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CC(=O)Nc2ccc(OCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CCCC(=O)Nc2ccc(OCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CCCCCC(=O)Nc2ccc(OCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CC(=O)Nc2ccc(OCCCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CCCC(=O)Nc2ccc(OCCCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CCCCCC(=O)Nc2ccc(OCCCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CC(=O)Nc2ccc(OCCCCCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CCCC(=O)Nc2ccc(OCCCCCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CCCCCC(=O)Nc2ccc(OCCCCCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CC(=O)Nc2ccc(OCCCCCCCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CCCC(=O)Nc2ccc(OCCCCCCCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CCCCCC(=O)Nc2ccc(OCCCCCCCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCCCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CC(=O)Nc2ccc(OCCCCCCCCCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCCCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CCCC(=O)Nc2ccc(OCCCCCCCCCCCCCCCC)cc2)cc1.[Br-].[Br-]
CCCCCCCCCCCCCCCCOc1ccc(NC(=O)C[N+](C)(C)CCCCCC[N+](C)(C)CCCCCC(=O)Nc2ccc(OCCCCCCCCCCCCCCCC)cc2)cc1.[Br-].[Br-]
"""
