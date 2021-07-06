import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import seaborn as sns
import uproot
import boost_histogram as bh

# x = st.slider('x',min_value=0.0,max_value=10.0,value=0.0)  # 👈 this is a widget
# st.write(x, 'squared is', x * x)
#
# color = st.select_slider(
#     'Select a color of the rainbow',
#     options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'])
# st.write('My favorite color is', color)


# slider histogram binning

slider_range = st.slider('end points of bins',value=[0,500])
st.write(slider_range)
# st.title("Variable Bin-Width HEP Dashboard")
#
# x = st.slider('number of bins',min_value=1,max_value=100)
#
# file = uproot.open("~/Documents/feb15_test1.root")
# tree=file["smeared"]
# caz=tree["mu_pt"].array(library="pd")
#
# @st.cache
# def Generate_Histogram(x,caz):
#     bins = np.linspace(0,5e5,x+1)
#     h = bh.Histogram(bh.axis.Variable(bins))
#     h.fill(caz)
#     return h
#
# h = Generate_Histogram(x,caz)
#
# fig,ax = plt.subplots()
# hep.histplot(h)
# st.pyplot(fig)
