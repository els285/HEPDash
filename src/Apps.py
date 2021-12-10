
from X import import_ROOT_file


# class Physics_Object:

#     def __init__(self,name,tree,**kwargs):
#                         # df = tree[page_data["observable"]].array(library="pd")   # Pulling 

#         self.Pt  = tree[name+"_pt"].array(library="pd")
#         self.Eta =
#         self.Phi = 
#         self.E   =

from dataclasses import dataclass
@dataclass
class InputObject:
    name: str
    ROOT_file_path: str
    tree_name: str 
    tree: any 

class HL_Tree_Comparison_App:

    """
    Tree_Comparison_App is a class for generating a streamlit-based web app for comparing the contents of TTrees in separate ROOT files
    Intention: the TBrowser() extension: for visual inspection of branches in NTuples
    The app will be split by object and observable
    Pulls out all common branches in the ROOT files, or a specified sub-set
    """

    physics_objects = ["el","mu","jet"]
    observable_branches = ["_pt","_eta","_phi","_e"]
    all_branches = [''.join(p) for p in itertools.product(letters, numbers)]

    def __init__(self,input_dictionary):

        '''
        input dictionary should be of the form {name: [ROOT_file_path,tree_name])}
        '''
        self.list_of_input_objects = {}

        for k,v in input_dictionary.items():
            io = InputObject(k,v[0],v[1],None)
            self.list_of_input_objects.append(io)
            # self.dic_of_data[k] = {"ROOT_file_path":v[0] , "tree_name":v[1] , "uproot_object":None} 

    def load(self):

        for io in self.list_of_input_objects:
            v.tree = import_ROOT_file(v.ROOT_file_path)

    def check_trees_for_branches(self):

        for io in self.list_of_input_objects:
            assert any([branch_name in io.tree.keys() for branch_name in 


    

            # import_ROOT_file(k[0])

        # if "list_of_ROOT_files" in kwargs and "tree_name" in kwargs:
        #     self.list_of_ROOT_files = kwargs["list_of_ROOT_files"] 
        #     self.dic_of_ROOT_files  = {rf}
        # self.dic_of_ROOT_files  = kwargs["dic_of_ROOT_files"]  if "dic_of_ROOT_files"  in kwargs else []


# def make_HL_app()


class Root_Hist_Comparison_App:

    """
    Root_Hist_Comparison_App is a class for generating a streamlit-based web app for comparing ROOT histograms defined in separate ROOT files
    Intention: for visual inspection of pre-generated histograms where some NTuple post-processing has already been achieved in ROOT
    The app will be split by object and observable
    Pulls out all commonly-named histograms, or a specified sub-set
    """

    def __init__(self, list_of_ROOT_files):
        self.list_of_ROOT_files = list_of_ROOT_files