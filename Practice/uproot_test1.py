import uproot
file = uproot.open("~/Documents/feb15_test1.root")
# print(file.keys())
tree=file["smeared"]
# [print(file["smeared"][x]) for x in file["smeared"].keys()]


caz=file["smeared"]["mu_pt"].array(library="pd")
print(caz)
# input()
# print(type(caz))


def get_branch_extrema(branch_pd):

	return branch_pd.max(),branch_pd.min()





# def Project_Branch_AutoHist(TTree,branch_name):

# 	df = TTree[branch_name].array(library="pd")

# 	maxv,minv = get_branch_extrema(df)






import matplotlib.pyplot as plt 

# from hist import Hist
import boost_histogram as bh 


# h = bh.Histogram(bh.axis.Regular(100,0,1e6))
import numpy as np
bins = np.linspace(0,5e5,51)
# arr=[0.0,0.1,0.2,0.5,1.0]
# bins = np.asarray(arr)*1e6
h = bh.Histogram(bh.axis.Variable(bins))
h.fill(caz)


import mplhep as hep

hep.style.use(hep.style.ATLAS)
# hep.label("MC")#, data=True, lumi=50, year=2017)
fig, ax = plt.subplots()



hep.histplot(h)

plt.show()
# hep.style.use("ATLAS")
# plt.bar(h.axes[0].centers, h, h.axes[0].widths)
# plt.show()
# input()
# plt.close()

# print(caz.__dict__)
# # print(tree)