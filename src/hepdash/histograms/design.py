# Design config
import mplhep as hep

experiment_labels = {

    "ATLAS"  :  hep.atlas, 
    "CMS"    :  hep.cms,
    "LHCb2"  :  hep.lhcb,
    "ALICE"  :  hep.alice
}



HEP_histogram_design_parameters = {

    "experiment" : "ATLAS",
    "HEP label text"  : "Internal"

}


HEP_histogram_design_parameters["HEP experiment label"] = experiment_labels[HEP_histogram_design_parameters["experiment"]]