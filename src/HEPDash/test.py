import uproot
import pandas as pd

file_path = "~/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_particleLevel_even.root"
tree_name = "particleLevel_even"

file = uproot.open(file_path)
tree = file[tree_name]

df1 = tree.arrays("el_pt","(el_pt>100000)")
df2 = tree.arrays("mu_pt","(el_pt>100000)")

print(df1)
print(df2)
