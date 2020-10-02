# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 13:19:26 2020

@author: olivi
"""

from sympy import *
from scipy.special import kv
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

Lambda = 1.55e-6
Lamb_SiO2 = [0.068404e-6, 0.116241e-6, 9.896161e-6] #um
Lamb_GeO2 = [0.068972e-6, 0.153966e-6, 11.84193e-6] #um

A_SiO2 = [0.696166, 0.407942, 0.897479]
A_GeO2 = [0.806866, 0.718158, 0.854168]

x = 0.04

c = 3e8
a = 4.6e-6
u_inf = 2.405

Lambda_symb = Symbol('Lambda_symb') # pour dériver


# Dispersion matérielle de la gaine
somme_gaine = 0
for i in range(3):
    CoteGauche = A_SiO2[i]*Lambda_symb**2/(Lambda_symb**2-Lamb_SiO2[i]**2)
    somme_gaine = somme_gaine + CoteGauche
n_gaine = sp.sqrt(somme_gaine+1)
n_primegaine = n_gaine.diff(Lambda_symb)
n_primeprimegaine = n_primegaine.diff(Lambda_symb)

D_m = -n_primeprimegaine.subs(Lambda_symb,Lambda)*Lambda/c*1e6


# Dispersion de guidage de la gaine
somme_coeur = 0
for i in range(3):
    CoteGauche = (A_SiO2[i]+x*(A_GeO2[i]-A_SiO2[i]))*Lambda**2/ \
    (Lambda**2-(Lamb_SiO2[i]+x*(Lamb_GeO2[i]-Lamb_SiO2[i]))**2)
    somme_coeur = somme_coeur + CoteGauche
n_coeur = np.sqrt(somme_coeur+1)



n_gaine = float(n_gaine.subs(Lambda_symb, Lambda))
N_gaine = n_gaine-Lambda*n_primegaine.subs(Lambda_symb, Lambda) # Grand N2 de la formule de dispersion de guidage


NA = np.sqrt(n_coeur**2-n_gaine**2)
Delta = NA**2/(2*n_coeur**2)
V = 2*np.pi*NA*a/Lambda
u = u_inf*V/(V+1)*(1-u_inf**2/(6*(V+1)**3)-u_inf**4/(20*(V+1)**5))
w = np.sqrt(V**2-u**2)
psi = kv(0,w)**2/(kv(-1,w)*kv(1,w))

VVb_primeprime = 2*(u/V)*(psi*(1-2*psi)+2/w*(w**2+u**2*psi)*np.sqrt(psi)*(psi+np.sqrt(psi)/w-1))
D_w = -N_gaine**2*Delta*VVb_primeprime/(n_gaine*c*Lambda)*1e6


# Dispersion totale
D = D_m+D_w
print("La Dispersion totale est de %5.3f [ps/nm*km]." % (D))

Beta = -Lambda**2*D/(2*np.pi*c)*1e21
print("Bêta est de %5.3f [ps2/km]." % (Beta))