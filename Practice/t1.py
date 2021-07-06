import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import seaborn as sns

# Correct style syntax
hep.style.use(hep.style.CMS)

# Create matplotlib object
fig,ax = plt.subplots()


"""
The following lines define a prototype example histogram.
Will eventually include some macro for turning ROOT histograms, perhaps using uproot, mplhep directly, or my own work
"""

# Define histogram binning
# xbins, ybins = [0, 1, 2, 3], [0, 1, 3]

# # Define histogram content
# H = np.array([[2,1], [1,2], [3,5]])
# hep.hist2dplot(H, xbins, ybins)

import streamlit as st

#
st.write("""
# HEP Dashboard
Welcome to the HEP Dashboard, designed to display your HEP plots in an interactive way!
""")

st.pyplot(fig)


st.write("hello")
# st.write(plt.run(window=15))
