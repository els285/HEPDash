

class Root_Hist_Comparison_App:

    """
    Root_Hist_Comparison_App is a class for generating a streamlit-based web app for comparing ROOT histograms defined in separate ROOT files
    Intention: for visual inspection of pre-generated histograms where some NTuple post-processing has already been achieved in ROOT
    The app will be split by object and observable
    Pulls out all commonly-named histograms, or a specified sub-set
    """

    def __init__(self, list_of_ROOT_files):
        self.list_of_ROOT_files = list_of_ROOT_files