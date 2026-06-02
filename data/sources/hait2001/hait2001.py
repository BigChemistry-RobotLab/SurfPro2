from string import Template

# Myrj
"CCCCCCCCCCCCCCCCCC(=O)O$chain"
i = 8
i = 40
i = 50
i = 100
"CCCCCCCCCCCCCCCCCC(=O)OCCOCCOCCOCCOCCOCCOCCOCCO"
"CCCCCCCCCCCCCCCCCC(=O)OCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCO"
"CCCCCCCCCCCCCCCCCC(=O)OCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCO"
"CCCCCCCCCCCCCCCCCC(=O)OCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCO"

# TX
"CC(C)(C)CC(C)(C)c1ccc($chain)cc1"

n = 1
n = 3
n = 5
n = 7.5
n = 9.5
n = 12.5
n = 16
n = 30
n = 40
n = 70

"CC(C)(C)CC(C)(C)c1ccc(OCCO)cc1"
"CC(C)(C)CC(C)(C)c1ccc(OCCOCCOCCO)cc1"
"CC(C)(C)CC(C)(C)c1ccc(OCCOCCOCCOCCOCCO)cc1"
"-"
"-"
"-"
"CC(C)(C)CC(C)(C)c1ccc(OCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCO)cc1"
"CC(C)(C)CC(C)(C)c1ccc(OCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCO)cc1"
"CC(C)(C)CC(C)(C)c1ccc(OCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCO)cc1"
"CC(C)(C)CC(C)(C)c1ccc(OCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCOCCO)cc1"

# Brij
brij = [
    "POE(4) lauryl_ether",
    "POE(23) lauryl_ether",
    "POE(2) cetyl_ether",
    "POE(10) cetyl_ether",
    "POE(20) cetyl_ether",
    "POE(2) stearyl_ether",
    "POE(10) stearyl_ether",
    "POE(20) stearyl_ether",
    "POE(2) oleyl_ether",
    "POE(10) oleyl_ether",
    "POE(20) oleyl_ether",
    "POE(100) stearyl_ether",
    "POE(21) stearyl_ether",
]

brij_chains = {
    "lauryl_ether": "CCCCCCCCCCCCO",
    "cetyl_ether": "CCCCCCCCCCCCCCCCO",
    "stearyl_ether": "CCCCCCCCCCCCCCCCCCO",
    "oleyl_ether": "CCCCCCCCCCCCCCCCCCO",
}

for b in brij:
    po_number = int(b[b.find("(") + 1 : b.find(")")])
    peo_chain = po_number * "CCO"
    chain = b.split(" ")[1]
    result = brij_chains[chain] + peo_chain
    print(result)


# Tween
tweens = [
    "POE(20) sorbitan monolaurate",
    "POE(20) sorbitan monopalmitate",
    "POE(20) sorbitan monostearate",
    "POE(20) sorbitan monooleate",
    "POE(20) sorbitan tristearate",
    "POE(20) sorbitan trioleate",
]

tween_chains = {
        "sorbitan monolaurate": "CCCCCCCCCCCC(=O)OCC(C1C(C(CO1)O)O)O",
        "sorbitan monopalmitate": "",
        "sorbitan monostearate": "",
        "sorbitan monooleate": "",
        "sorbitan tristearate": "",
        "sorbitan trioleate": "",
        }

for t in tweens:
    po_number = int(b[b.find("(") + 1 : b.find(")")])
    peo_chain = po_number * "CCO"


