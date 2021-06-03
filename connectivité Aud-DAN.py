import os
from nilearn import datasets
from nilearn.input_data import NiftiLabelsMasker, NiftiMasker
from nilearn.connectome import ConnectivityMeasure
from nilearn import plotting
import numpy as np
from graph import *
from numpy.linalg import eig
from nilearn.input_data import NiftiMapsMasker



def matrice_degré(G):
    """permet de calculer la matrice de degrés à partir du graph G"""
    matrice_d=np.zeros(np.shape(G))

    for i in range(len(G)):
        for j in range(len(G[0])) :
            if i!=j:

                matrice_d[i,i]+=G[i,j]

    return(matrice_d)




### Changement de répertoire de travail+téléchangement des données IRMf pour rest et active

os.chdir("E:/COURS-IMT/CODEV_Recherche/Données_Analysées/fmriprep/sub-30AQ/func")
#data_active = "sub-02CB_task-movie_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
data_rest="sub-30AQ_task-movie_run-4_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"

###Telechangement de l'atlas

atlas_data = datasets.fetch_atlas_msdl()
atlas_filename = atlas_data['maps']
MSDL_network=atlas_data.networks


###Création des connectomes et des masker pour les états rest et active


# connectome_measure_active = ConnectivityMeasure(kind='correlation')
connectome_measure_rest = ConnectivityMeasure(kind='correlation')
masker =  NiftiMapsMasker(maps_img=atlas_filename, standardize=True,
                         memory='nilearn_cache', verbose=5)

###Extraction des times series

#time_series_active = []
time_series_rest = []
#time_series_active.append(masker.fit_transform(data_active))
time_series_rest.append(masker.fit_transform(data_rest))

### calcul de la matrice de corrélation+ Moyenne

#correlation_matrices_active = connectome_measure_active.fit_transform(time_series_active)
correlation_matrices_rest = connectome_measure_rest.fit_transform(time_series_rest)
#correlation_matrices_active =  connectome_measure_active.mean_
correlation_matrices_rest = connectome_measure_rest.mean_
np.fill_diagonal(correlation_matrices_rest, 0)
#np.fill_diagonal(correlation_matrices_active, 0)


###Afficher la connectivité audio-dorsal moyenne

connectivite_moy= (correlation_matrices_rest[0][17]+correlation_matrices_rest[1][17]+correlation_matrices_rest[0][18]+correlation_matrices_rest[1][18])/4
print(connectivite_moy)