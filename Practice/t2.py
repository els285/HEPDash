import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import seaborn as sns
import uproot
import boost_histogram as bh



file = uproot.open("~/Documents/feb15_test1.root")
tree=file["smeared"]
caz=tree["mu_pt"].array(library="pd")



bins = np.linspace(0,5e5,51)
h = bh.Histogram(bh.axis.Variable(bins))
h.fill(caz)

y =h/h

# print(y)
# exit()

fig,ax = plt.subplots()
hep.histplot(h)

# hep.atlas.text(text='hjhkjhkj')

# plt.show()
# input()
import streamlit as st



st.title("HEP Dashboard")

if st.button('Say hello'):
	st.write('Why hello there')
else:
	st.write('Goodbye')
#
st.write("""
# HEP Dashboard
Welcome to the HEP Dashboard, designed to display your HEP plots in an interactive way!
""")

st.pyplot(fig)


st.write("hello")
# st.write(plt.run(window=15))
