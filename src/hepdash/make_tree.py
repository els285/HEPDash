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
from hepdash.apps.Tree_Apps import Preset, General


import sys
app_type    = sys.argv[1]
config_file = sys.argv[2]

if app_type=="preset":
    app_func = Preset
elif app_type=="general":
    app_func = General
elif app_type=="specific":
    pass

def main():

    # Initialsie the streamlit web-app object
    st.set_page_config(layout='wide')
    st.title("HEP Dash")

    # Import the data
    App1 = app_func.make_from_config(config_file)
    print("ROOT files loaded")

    App1.add_object_pages()
    print("Pages written")

    # App1.make_multipage()
    print("Construction complete")



if __name__ == '__main__':
    if st._is_running_with_streamlit:
        # file_name   = sys.argv[1]
        # tree_name   = sys.argv[2]
        # branch_name = sys.argv[3]
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0],sys.argv[1],sys.argv[2]]#,sys.argv[3]]
        sys.exit(stcli.main())
