
import os
from nilearn import datasets
from nilearn.input_data import NiftiMapsMasker
from nilearn.connectome import ConnectivityMeasure
import numpy as np
from nilearn import plotting


def matrice_binaire(matrice,threshold):
    """conversion de matrice en matrice binaire selon le threshold choisi"""
    matrice=matrice.copy()
    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            if matrice[i][j]>threshold:
                matrice[i][j]=1
            else:
                matrice[i][j]=0
            
    return matrice



os.chdir("E:/COURS-IMT/CODEV_Recherche/Données_Analysées/fmriprep")
liste_sujets=["sub-02CB","sub-04HD","sub-04SG","sub-17NA","sub-19AK","sub-19SA","sub-22CY","sub-22TK","sub-30AQ"]
#liste_sujets=["sub-02CB","sub-04HD","sub-04SG","sub-19AK","sub-22CY","sub-22TK","sub-30AQ"]


somme_matrix_correlation=np.zeros((39,39))
atlas = datasets.fetch_atlas_msdl()
atlas_filename = atlas['maps']
labels = atlas['labels']
masker = NiftiMapsMasker(maps_img=atlas_filename, standardize=True,
                    memory='nilearn_cache', verbose=5)
correlation_measure = ConnectivityMeasure(kind='correlation')
             
             
## somme des matrices binaires de chaque sujets                    
for nom in liste_sujets:
    data=nom+"/func/"+nom+"_task-movie_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
    
    time_series = masker.fit_transform(data)
    correlation_matrix = correlation_measure.fit_transform([time_series])[0]
    np.fill_diagonal(correlation_matrix, 0)
    correlation_matrix=matrice_binaire(correlation_matrix,0.3)
    somme_matrix_correlation+=correlation_matrix
 
## On applique un threshold pour selectionner les pourcentages de connectivité partagée voulu
somme_matrix_correlation_binaire=  matrice_binaire(somme_matrix_correlation,7.1) 
    
##Affichage des conectomes
    
# coords = atlas.region_coords
# plotting.plot_connectome(somme_matrix_correlation_binaire, coords,
#                          edge_threshold="100%", colorbar=True)


## Affichage de la matrice
    
plotting.plot_matrix(somme_matrix_correlation_binaire, labels=labels, colorbar=True,
                     vmax=1, vmin=0)
    
plotting.show()
    
    
    