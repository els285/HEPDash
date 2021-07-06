import sys
from streamlit import cli as stcli
import streamlit as st

def main():
    slider_range = st.slider('end points of bins',value=[0,500])
    st.write(slider_range)
# Your streamlit code

if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
