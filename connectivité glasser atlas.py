from nilearn.input_data import NiftiLabelsMasker, NiftiMasker
from nilearn import image
import os
from nilearn import datasets
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

def matrice_binaire(matrice,threshold):
    """conversion de matrice en matrice binaire selon le threshold choisi"""
    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            if matrice[i][j]>threshold:
                matrice[i][j]=1
            else:
                matrice[i][j]=0
            
    return matrice

### Changement de répertoire de travail+téléchangement des données IRMf pour rest et active

os.chdir("E:/COURS-IMT/CODEV_Recherche/Données_Analysées/fmriprep/sub-02CB/func")
data_rest="sub-02CB_task-rest_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
#data_active="??????"

###Telechangement de l'atlas

path_Glasser="E:/COURS-IMT/CODEV_Recherche/Ressources/glasser/Glasser_masker.nii.gz"
glasser_atlas=image.load_img(path_Glasser)


###Création des connectomes et des masker pour les états rest et active

connectome_measure = ConnectivityMeasure(kind='correlation')
glassermasker = NiftiLabelsMasker(labels_img=path_Glasser)
glassermasker.fit()
#connectome_measure_active = ConnectivityMeasure(kind='correlation')
connectome_measure_rest = ConnectivityMeasure(kind='correlation')


###Extraction des times series

time_series_rest = []
#time_series_active = []
time_series_rest.append(glassermasker.fit_transform(data_rest))
#time_series_active.append(glassermasker.fit_transform(data_active))

### calcul de la matrice de corrélation+ Moyenne 

correlation_matrices_rest = connectome_measure_rest.fit_transform(time_series_rest)
correlation_matrices_rest = connectome_measure_rest.mean_
# correlation_matrices_active = connectome_measure_active.fit_transform(time_series_active)
# correlation_matrices_active = connectome_measure_active.mean_
np.fill_diagonal(correlation_matrices_rest, 0)
#np.fill_diagonal(correlation_matrices_active, 0)

###Conversion en matrice binaire


correlation_matrices_rest=matrice_binaire(correlation_matrices_rest,0.25)
#correlation_matrices_active=matrice_binaire(correlation_matrices_active,0.3)

###Afficher les connectomes


coordinates = plotting.find_parcellation_cut_coords(labels_img=path_Glasser)
plotting.plot_connectome(correlation_matrices_rest, coordinates,
                         edge_threshold="80%")
                         
plotting.show()
### afficher la matrice de correlation

plotting.plot_matrix(correlation_matrices_rest,vmax=0.8, vmin=-0.8)
#plotting.plot_matrix(correlation_matrices_active, vmax=0.8, vmin=-0.8)

plotting.show()

###Calcul de la matrice Laplacienne et affichage des valeurs propres
matrice_deg=matrice_degré(correlation_matrices_rest)
L=matrice_deg-correlation_matrices_rest
D,V=eig(L)

print(sorted(D))
