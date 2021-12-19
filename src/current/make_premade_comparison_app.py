'''
HEP-Dash
Ethan L Simpson
December 10th 2021

Notes:
- Require that the primary function for creating the web-app must be called main()
- How to re-factor this into something more user freindly?
- Just now, the only thing the user is required to do is edit the input dic - this could come from a config file
- Or it could come from a parser but probably complex
'''

# Imports
# Base imports
import sys
from dataclasses import dataclass

# Third-party imports
import streamlit as st
from streamlit import cli as stcli

# Package imports
from BiColumn import PhysOb_Page_TwoColumn, MultiPage
# from Apps2 import Premade_Tree_Comparison_App
from Tree_Apps import Preset 

input_dic = {"file1": {"file_path":"~/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_particleLevel_even.root" ,"tree_name": "particleLevel_even" , "colour":"blue" },
             "file2": {"file_path":"~/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_reco_even.root"          ,"tree_name": "reco_even"           , "colour":"red" }}
 

def main():

    # Initialsie the streamlit web-app object
    st.set_page_config(layout='wide')
    st.title("HEP Dash")

    # Import the data
    data_object = Preset(input_dic)

    # Pass list of trees here
    muon        =  PhysOb_Page_TwoColumn(phys_ob="Muon",      input_object=data_object,  branches2plot=["mu_pt","mu_eta","mu_phi","mu_e"])
    electron    =  PhysOb_Page_TwoColumn(phys_ob="Electron",  input_object=data_object,  branches2plot=["el_pt","el_eta","el_phi","el_e"])
    jet         =  PhysOb_Page_TwoColumn(phys_ob="Jet",       input_object=data_object,  branches2plot=["jet_pt","jet_eta","jet_phi","jet_e"])

    print("Pages written")

    MP = MultiPage()
    # MP.add_page(muon)
    # MP.add_page(electron)
    MP.add_page(jet)

    MP.Build_MultiPage()


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        # file_name   = sys.argv[1]
        # tree_name   = sys.argv[2]
        # branch_name = sys.argv[3]
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]#,sys.argv[1],sys.argv[2]]#,sys.argv[3]]
        sys.exit(stcli.main())
