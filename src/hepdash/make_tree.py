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
import sys
import os
import argparse

# Third-party imports
import streamlit as st
from streamlit import cli as stcli
import yaml

# Package imports
from hepdash.apps.Tree_Apps import Preset, General, Specific


def parse_args():

    """
    Function for parsing command line arguments of defined form
    Streamlit has an issue with such commands, the base streamlit command is 'streamlit run file.py',
      we then require ' -- ' to distinguish between streamlit and hepdash-specific commands
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--config"     ,  help="A YAML config file containing the ROOT information and plotting meta-data")
    parser.add_argument("--mode"       ,  help="The mode you which to run. Determines the branches of the TTree projected. You can run: general,preset,specific"  )
    parser.add_argument("--specifics"  ,  help="YAML file containing the specific branches to be used.")

    parser_arguments = parser.parse_args()

    assert hasattr(parser_arguments,"mode")    , "Mode not selected"
    assert hasattr(parser_arguments,"config")  , "Config file not passed"

    app_type    = getattr(parser_arguments,"mode")
    config_file = getattr(parser_arguments,"config")
    specifics_file = None

    # Depending on mode, select the correct app class
    if app_type=="preset" or app_type=="Preset":
        app_func = Preset
    elif app_type=="general" or app_type=="General":
        app_func = General
    elif app_type=="specific" or app_type=="Specific":
        if hasattr(parser_arguments,"specifics"):
            app_func = Specific
            specifics_object = Specific.parse_specifics(getattr(parser_arguments,"specifics"))
        else:
            print("Specifics config file not given. Resorting to General mode.")
            app_func = General

    return app_func , config_file 


def main():

    # Pull objects from argparse
    app_func , config_file  = parse_args()

    # Initialsie the streamlit web-app object
    st.set_page_config(layout='wide')
    st.title("HEP Dash")

    # Import the data
    App1 = app_func.make_from_config(config_file)
    # print("ROOT files loaded")

    App1.add_object_pages()
    # print("Pages written")

    # print("Construction complete")


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        # file_name   = sys.argv[1]
        # tree_name   = sys.argv[2]
        # branch_name = sys.argv[3]
        main()
    else:
        # sys.argv = ["streamlit", "run", sys.argv[0]," -- ",sys.argv[1],sys.argv[2]]#,sys.argv[3]]
        # sys.exit(stcli.main())

        sys.argv = ["streamlit", "run", sys.argv[0]," -- "] + sys.argv[1:]
        os.system(' '.join(sys.argv))
