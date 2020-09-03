# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 21:56:46 2020

@author: olivi
"""

import numpy as np
import matplotlib.pyplot as plt # Pour trouver l'intersection n_eff rapidement
import pylab as pl # Pour trouver l'intersection n_eff rapidement
from scipy.special import jv, kn

#%% Numero 2 a)

PasReseau = 0.93 # en um
nu = 1 # (visibilité des franges)
L = 5000 # en um
dn_coeur_peak2peak = 5e-4
a = 2.5 # en um
Lambda = np.linspace(1,3,2000)



A_SiO2 = [0.696166, 0.407942, 0.897479]
Lamb_SiO2 = [0.068404, 0.116241, 9.896161] # en um

x = 0.06 # pourcentage molaire
A_GeO2 = [0.806866, 0.718158, 0.854168]
Lamb_GeO2 = [0.068972, 0.153966, 11.84193] # en um

n_gaine = []
for j in range(len(Lambda)):
    somme_gaine = 0
    for i in range(3):
        CoteGauche = A_SiO2[i]*Lambda[j]**2/(Lambda[j]**2-Lamb_SiO2[i]**2)
        somme_gaine = somme_gaine + CoteGauche
    n_gaine.append(np.sqrt(somme_gaine+1))

n_coeur = []
for j in range(len(Lambda)):
    somme_coeur = 0
    for i in range(3):
        CoteGauche = (A_SiO2[i]+x*(A_GeO2[i]-A_SiO2[i]))*Lambda[j]**2/ \
        (Lambda[j]**2-(Lamb_SiO2[i]+x*(Lamb_GeO2[i]-Lamb_SiO2[i]))**2)
        somme_coeur = somme_coeur + CoteGauche
    n_coeur.append(np.sqrt(somme_coeur+1))
   
NA = []
V = []
u_miyagi = []
n_effBragg = []
n_effMiyagi = []
u_inf = 2.405
for j in range(len(Lambda)):
    NA.append(np.sqrt(n_coeur[j]**2-n_gaine[j]**2))
    V.append(2*np.pi*a*NA[j]/Lambda[j])
    u_miyagi.append(u_inf*V[j]/(V[j]+1)*(1-u_inf**2/(6*(V[j]+1)**3)-u_inf**4/(20*(V[j]+1)**5)))
    n_effBragg.append(Lambda[j]/(2*PasReseau))
    n_effMiyagi.append(np.sqrt(n_coeur[j]**2-(u_miyagi[j]*Lambda[j]/(2*np.pi*a))**2))
    
    
plt.plot(Lambda,n_effMiyagi)
plt.plot(Lambda,n_effBragg)
ax = pl.gca()
ylim = ax.get_ylim()
plt.vlines(2.653, ylim[0], ylim[1])
plt.show()

LambBragg = 2.653 # en um et la 1653e donnée
print("La longueur d'onde de Bragg du reseau est de %5.3f microns." % (LambBragg))

#%% Numero 2b)

# Le code suivant a ete fait en considerant une fibre a saut d'indice, ce qui n'est pas bon.
#b = (n_effMiyagi[1653]**2-n_gaine[1653]**2)/NA[1653]**2
#w = np.sqrt(V[1653]**2-u_miyagi[1653]**2)
#
#
#Gamma1 = b**2/V[1653]**2*(1-jv(0,V[1653]*np.sqrt(1-b))**2/ \
#        (jv(1,V[1653]*np.sqrt(1-b))*jv(-1,V[1653]*np.sqrt(1-b)))) # Formule dans Erdogan
#
#Gamma2 = 1-u_miyagi[1653]**2/V[1653]**2*(1-kn(0,w)**2/(kn(1,w)*kn(-1,w))) # Formule dans les notes
#
#Gamma3 = 0.18 # Figure1 dans Erdogan (approximation)
#
#Gamma = [Gamma1, Gamma2, Gamma3]
#
#dn_eff_av = []
#kappa = []
#r_max = []
#t_max = []
#PertesTransmission = []
#for i in range(3):
#    dn_eff_av.append(Gamma[i]*dn_coeur_peak2peak/2) # Approximation dans Erdogan
#    kappa.append(np.pi*nu*dn_eff_av[i]/LambBragg)
#    r_max.append(np.tanh(kappa[i]*L)**2) # reflectivite
#    t_max.append(1-r_max[i]) # transmitivite
#    PertesTransmission.append(10*np.log10(t_max[i]))
#
#
#print("La reflectivite du reseau est de %5.3f et ses pertes \
#en transmission sont de %5.3f dB." % (r_max[1], PertesTransmission[1]))

dn_eff_av = dn_coeur_peak2peak/2 # Approximation, car le coeur est petit
kappa = np.pi*nu*dn_eff_av/LambBragg
r_max = np.tanh(kappa*L)**2
t_max = 1-r_max
PertesTransmission = 10*np.log10(t_max)
print("La reflectivite du reseau est de %5.3f et ses pertes \
en transmission sont de %5.3f dB." % (r_max, PertesTransmission))


#%% Numero 2 c)
LambBragg_second = LambBragg/2 

print("La longueur d'onde de Bragg du second ordre est de %5.3f microns." % (LambBragg_second))