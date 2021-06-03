import os
from nilearn import datasets
from nilearn.input_data import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure
from nilearn import plotting
import numpy as np
from graph import *
from numpy.linalg import eig
os.chdir("E:/COURS-IMT/CODEV_Recherche/Données_Analysées/fmriprep/sub-02CB/func")

yeo = datasets.fetch_atlas_yeo_2011()

# data_active = "sub-02CB_task-movie_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"



data_rest="sub-02CB_task-rest_run-3_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"



#confounds="sub-02CB_task-rest_run-3_desc-confounds_timeseries.tsv"


# connectome_measure_active = ConnectivityMeasure(kind='correlation')


connectome_measure_rest = ConnectivityMeasure(kind='correlation')


masker = NiftiLabelsMasker(labels_img=yeo['thick_17'], standardize=True,
                           memory='nilearn_cache')

# extract time series from all subjects and concatenate them
# time_series_active = []
time_series_rest = []
# time_series_active.append(masker.fit_transform(data_active))
time_series_rest.append(masker.fit_transform(data_rest))

# calculate correlation matrices across subjects and display
# correlation_matrices_active = connectome_measure_active.fit_transform(time_series_active)
correlation_matrices_rest = connectome_measure_rest.fit_transform(time_series_rest)
# correlation_matrices_active =  connectome_measure_active.mean_
correlation_matrices_rest = connectome_measure_rest.mean_


# grab center coordinates for atlas labels
# coordinates = plotting.find_parcellation_cut_coords(labels_img=yeo['thick_17'])
# 


# for i in range(len(correlation_matrices_active)):
#     for j in range(len(correlation_matrices_active[0])):
#         if correlation_matrices_active[i][j]>0.42:
#             correlation_matrices_active[i][j]=1
#         else:
#             correlation_matrices_active[i][j]=0
#             
for i in range(len(correlation_matrices_rest)):
    for j in range(len(correlation_matrices_rest[0])):
        if correlation_matrices_rest[i][j]>0.7:
            correlation_matrices_rest[i][j]=1
        else:
            correlation_matrices_rest[i][j]=0
            
            
np.fill_diagonal(correlation_matrices_rest, 0)
# plotting.plot_matrix(correlation_matrices_rest,vmax=0.8, vmin=-0.8)
# np.fill_diagonal(correlation_matrices_active, 0)
# plotting.plot_matrix(correlation_matrices_active,title="active" ,colorbar=True,
#                      vmax=0.8, vmin=-0.8)

# plotting.show()

def matrice_degré(G):
    matrice_d=np.zeros(np.shape(G))
    
    for i in range(len(G)):
        for j in range(len(G[0])) :
            if i!=j:
                
                matrice_d[i,i]+=G[i,j]
            
    return(matrice_d)
matrice_deg=matrice_degré(correlation_matrices_rest)
L=matrice_deg-correlation_matrices_rest

D,V=eig(L)
print(sorted(D))
