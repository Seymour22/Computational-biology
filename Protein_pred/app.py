# This is app is created by Chanin Nantasenamat (Data Professor) https://youtube.com/dataprofessor
# Credit: This app is inspired by https://huggingface.co/spaces/osanseviero/esmfold

import numpy as np
import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

#st.set_page_config(layout = 'wide')
st.sidebar.title('🎈 ESMFold')
st.sidebar.write('[*ESMFold*](https://esmatlas.com/about) is an end-to-end single sequence protein structure predictor based on the ESM-2 language model. For more information, read the [research article](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) and the [news article](https://www.nature.com/articles/d41586-022-03539-1) published in *Nature*.')

# stmol
def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({'cartoon':{'color':'spectrum'}})
    pdbview.setBackgroundColor('white')#('0xeeeeee')
    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(True)
    showmol(pdbview, height = 500,width=800)

# Protein sequence input
DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
txt = st.sidebar.text_area('Input sequence', DEFAULT_SEQ, height=275)

# ESMfold
def update(sequence=txt):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence)
    name = sequence[:3] + sequence[-3:]
    pdb_string = response.content.decode('utf-8')

    with open('predicted.pdb', 'w') as f:
        f.write(pdb_string)

    struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
    b_value = round(struct.b_factor.mean(), 4)

    # Display protein structure
    st.subheader('Visualization of predicted protein structure')
    render_mol(pdb_string)

    # plDDT value is stored in the B-factor field
    st.subheader('plDDT')
    st.write('plDDT is a per-residue estimate of the confidence in prediction on a scale from 0-100.')
    st.info(f'plDDT: {b_value}')

    st.download_button(
        label="Download PDB",
        data=pdb_string,
        file_name='predicted.pdb',
        mime='text/plain',
    )

predict = st.sidebar.button('Predict', on_click=update)


if not predict:
    st.warning('👈 Enter protein sequence data!')


# Function to calculate structural properties
def calculate_properties(structure):
    # Example: Calculate RMSD
    rmsd = np.random.uniform(0, 3.0)  # Placeholder value, replace with actual calculation
    return rmsd

# Function to display structural properties
def display_properties(properties):
    st.subheader('Structural Properties')
    st.write('Here are some calculated structural properties of the predicted protein structure:')
    st.write(f'- Root Mean Square Deviation (RMSD): {properties["rmsd"]}')
    # Add more properties as needed

# Function to compare two protein structures
def compare_structures(structure1, structure2):
    # Example: Calculate structural alignment score
    alignment_score = np.random.uniform(0.5, 1.0)  # Placeholder value, replace with actual calculation
    return alignment_score

# Function to display structural comparison results
def display_comparison_result(score):
    st.subheader('Structural Comparison Result')
    st.write('The structural alignment score between the predicted structure and the reference structure is:')
    st.write(f'- Alignment Score: {score}')

# Add option for structural analysis or comparison in the sidebar
analysis_option = st.sidebar.radio('Select Analysis or Comparison', ['Analysis', 'Comparison'])

if analysis_option == 'Analysis':
    # Perform structural analysis
    properties = calculate_properties(predicted_structure)
    display_properties(properties)
else:
    # Perform structural comparison
    reference_structure = st.sidebar.file_uploader('Upload Reference Structure (PDB)', type='pdb')
    if reference_structure:
        comparison_score = compare_structures(predicted_structure, reference_structure)
        display_comparison_result(comparison_score)
    else:
        st.warning('Please upload a reference structure for comparison.')
