from rdkit import Chem

sm = "CCCCCCSC[C@@H](O)[C@H](O)[C@H](O)CO"

mol = Chem.MolFromSmiles(sm)
ch_centres = Chem.FindMolChiralCenters(mol)

if len(ch_centres) > 0 and ch_centres[-1][-1] == "S":
    print("Left handed: L")
else:
    print("Right handed: D")
