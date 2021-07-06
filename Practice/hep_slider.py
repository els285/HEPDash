import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import seaborn as sns
import uproot
import boost_histogram as bh
import sys

file_name = sys.argv[1]

@st.cache
def Generate_Histogram(num_bins,hist_range,df):
    bins = np.linspace(hist_range[0]*1e3,hist_range[1]*1e3,nb+1)
    h = bh.Histogram(bh.axis.Variable(bins))
    h.fill(df)
    return h

st.title("Variable Bin-Width HEP Dashboard")

file = uproot.open(file_name)
tree=file["smeared"]
caz=tree["mu_pt"].array(library="pd")


nb = st.slider('number of bins',min_value=1,max_value=100)
hist_range = st.slider('end points of bins',value=[0.0,500.0])

h=Generate_Histogram(nb,hist_range,caz)
fig,ax = plt.subplots()
hep.histplot(h)
st.pyplot(fig)
