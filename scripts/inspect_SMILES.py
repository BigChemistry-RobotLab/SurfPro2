import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw
import pandas as pd
from pathlib import Path

# ---- Discover available datasets ----
BASE_DIR = Path("data/sources")

# Find all CSV files under subdirectories
csv_files = list(BASE_DIR.rglob("*.csv"))

# Create nice labels (e.g. sugihara2003)
options = {
    str(f.relative_to(BASE_DIR)): f
    for f in csv_files
}

# ---- Dropdown selection ----
selected_key = st.selectbox("Select dataset", list(options.keys()))
FILE = options[selected_key]

# ---- Load data ----
df = pd.read_csv(FILE)

# Reset index if dataset changes
if "last_file" not in st.session_state or st.session_state.last_file != str(FILE):
    st.session_state.idx = 0
    st.session_state.last_file = str(FILE)

if "idx" not in st.session_state:
    st.session_state.idx = 0


def mol_from_smiles(smiles: str):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        st.error(f"Invalid SMILES: {smiles}")
    return mol


def render_mol(smiles: str, size=(300, 300)):
    mol = mol_from_smiles(smiles)
    if mol is None:
        return None
    return Draw.MolToImage(mol, size=size)


st.title("SurfPro Inspector")

row = df.loc[st.session_state.idx]

nav_left, nav_mid, nav_right = st.columns([1, 2, 1])
col_left, col_right = st.columns(2)

with nav_left:
    if st.button("⬅ Previous", disabled=st.session_state.idx == 0):
        st.session_state.idx -= 1
        st.rerun()

with nav_mid:
    st.markdown(
        f"<div style='text-align:center;'>Pair {st.session_state.idx + 1} / {df.shape[0]}</div>",
        unsafe_allow_html=True,
    )

with nav_right:
    if st.button("Next ➡", disabled=st.session_state.idx == df.shape[0] - 1):
        st.session_state.idx += 1
        st.rerun()

with col_left:
    st.subheader("Structure")
    st.code(row.SMILES)
    img = render_mol(row.SMILES)
    if img:
        st.image(img)

with col_right:
    st.subheader("Database record")

    for col in df.columns:
        if col in ["compound_name", "ref_key", "SMILES"]:
            continue
        st.markdown(f"**{col}:** {row[col]}")

    st.markdown("---")
