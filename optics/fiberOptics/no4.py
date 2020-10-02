# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 12:02:10 2020

@author: olivi
"""
from sympy import *
from scipy.special import kv
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

Lambda = np.linspace(1e-6,1.5e-6,100)
LambdaSiO2 = [0.068404e-6, 0.116241e-6, 9.896161e-6] #um
LambdaGeO2 = [0.068972e-6, 0.153966e-6, 11.84193e-6] #um

ASiO2 = [0.696166, 0.407942, 0.897479]
AGeO2 = [0.806866, 0.718158, 0.854168]

x1 = 0.02
x2 = 0.08

c = 3e8
a = 3e-6
u_inf = 2.405
L = 10000

Lambda_symb = Symbol('Lambda_symb') # pour dériver


# Dispersion matérielle de la gaine
ngaine = sp.sqrt(ASiO2[0]*Lambda_symb**2/(Lambda_symb**2-LambdaSiO2[0]**2)+ \
                  ASiO2[1]*Lambda_symb**2/(Lambda_symb**2-LambdaSiO2[1]**2)+ \
                  ASiO2[2]*Lambda_symb**2/(Lambda_symb**2-LambdaSiO2[2]**2)+ 1)
n_primegaine = ngaine.diff(Lambda_symb)
n_primeprimegaine = n_primegaine.diff(Lambda_symb)

NPRIMEPRIMEGAINE = []
D_M = []
for i in range(len(Lambda)):
    NPRIMEPRIMEGAINE.append(float(n_primeprimegaine.subs(Lambda_symb,Lambda[i])))
    D_M.append(-Lambda[i]/c*NPRIMEPRIMEGAINE[i]*1e6)


# Dispersion de guidage de la gaine
n1 = sp.sqrt((ASiO2[0]+x1*(AGeO2[0]-ASiO2[0]))*Lambda_symb**2/(Lambda_symb**2-(LambdaSiO2[0]+x1*(LambdaGeO2[0]-LambdaSiO2[0]))**2)+ \
(ASiO2[1]+x1*(AGeO2[1]-ASiO2[1]))*Lambda_symb**2/(Lambda_symb**2-(LambdaSiO2[1]+x1*(LambdaGeO2[1]-LambdaSiO2[1]))**2)+ \
(ASiO2[2]+x1*(AGeO2[2]-ASiO2[2]))*Lambda_symb**2/(Lambda_symb**2-(LambdaSiO2[2]+x1*(LambdaGeO2[2]-LambdaSiO2[2]))**2)+1)
n_prime1 = n1.diff(Lambda_symb)
n_primeprime1 = n_prime1.diff(Lambda_symb)

n2 = sp.sqrt((ASiO2[0]+x2*(AGeO2[0]-ASiO2[0]))*Lambda_symb**2/(Lambda_symb**2-(LambdaSiO2[0]+x2*(LambdaGeO2[0]-LambdaSiO2[0]))**2)+ \
(ASiO2[1]+x2*(AGeO2[1]-ASiO2[1]))*Lambda_symb**2/(Lambda_symb**2-(LambdaSiO2[1]+x2*(LambdaGeO2[1]-LambdaSiO2[1]))**2)+ \
(ASiO2[2]+x2*(AGeO2[2]-ASiO2[2]))*Lambda_symb**2/(Lambda_symb**2-(LambdaSiO2[2]+x2*(LambdaGeO2[2]-LambdaSiO2[2]))**2)+1)
n_prime2 = n2.diff(Lambda_symb)
n_primeprime2 = n_prime2.diff(Lambda_symb)

N1 = []
N2 = []
NGAINE = []

V1 = []
V2 = []

u1 = []
u2 = []

w1 = []
w2 = []

psi1 = []
psi2 = []

VbPRIME1 = []
VbPRIME2 = []

NGAINEPRIME = []

VVbPRIMEPRIME1 = []
VVbPRIMEPRIME2 = []

D_W1 = []
D_W2 = []

Tg1 = []
Tg2 = []
for i in range(len(Lambda)):
    N1.append(float(n1.subs(Lambda_symb,Lambda[i]))) 
    N2.append(float(n2.subs(Lambda_symb,Lambda[i])))
    NGAINE.append(float(ngaine.subs(Lambda_symb,Lambda[i])))
    
    V1.append(2*np.pi*np.sqrt(N1[i]**2-NGAINE[i]**2)*a/(Lambda[i]))
    V2.append(2*np.pi*np.sqrt(N2[i]**2-NGAINE[i]**2)*a/(Lambda[i]))
    
    u1.append(u_inf * V1[i]/(V1[i]+1) * (1 - u_inf**2/(6*(V1[i]+1)**3) - u_inf**4/(20*(V1[i]+1)**5)))
    u2.append(u_inf * V2[i]/(V2[i]+1) * (1 - u_inf**2/(6*(V2[i]+1)**3) - u_inf**4/(20*(V2[i]+1)**5)))
    
    w1.append(np.sqrt(V1[i]**2-u1[i]**2))
    w2.append(np.sqrt(V2[i]**2-u2[i]**2))
    
    psi1.append(kv(0,w1[i])**2/(kv(1,w1[i])*kv(-1,w1[i])))
    psi2.append(kv(0,w2[i])**2/(kv(1,w2[i])*kv(-1,w2[i])))
    
    VbPRIME1.append(1-(u1[i]/V1[i])**2*(1-2*psi1[i]))
    VbPRIME2.append(1-(u2[i]/V2[i])**2*(1-2*psi2[i]))
    
    NGAINEPRIME.append(float(n_primegaine.subs(Lambda_symb,Lambda[i])))
    
    VVbPRIMEPRIME1.append(2*(u1[i]/V1[i])**2*(psi1[i]*(1-2*psi1[i])+2/w1[i]*(w1[i]**2+u1[i]**2*psi1[i])*np.sqrt(psi1[i])*(psi1[i]+np.sqrt(psi1[i])/w1[i]-1)))
    VVbPRIMEPRIME2.append(2*(u2[i]/V2[i])**2*(psi2[i]*(1-2*psi2[i])+2/w2[i]*(w2[i]**2+u2[i]**2*psi2[i])*np.sqrt(psi2[i])*(psi2[i]+np.sqrt(psi2[i])/w2[i]-1)))
    
    D_W1.append(1e6*(N1[i]**2-NGAINE[i]**2)/(2*N1[i]**2)*(-VVbPRIMEPRIME1[i]/(c*Lambda[i]*NGAINE[i])*(NGAINE[i]-Lambda[i]*NGAINEPRIME[i])**2))
    D_W2.append(1e6*(N2[i]**2-NGAINE[i]**2)/(2*N1[i]**2)*(-VVbPRIMEPRIME2[i]/(c*Lambda[i]*NGAINE[i])*(NGAINE[i]-Lambda[i]*NGAINEPRIME[i])**2))
    
    Tg1.append(1e6*L/c*(NGAINE[i]-Lambda[i]*NGAINEPRIME[i])*(1+(N1[i]**2-NGAINE[i]**2)/(2*N1[i]**2)*VbPRIME1[i]))
    Tg2.append(1e6*L/c*(NGAINE[i]-Lambda[i]*NGAINEPRIME[i])*(1+(N2[i]**2-NGAINE[i]**2)/(2*N2[i]**2)*VbPRIME2[i]))

plt.figure(1)
plt.plot(Lambda*1e6, D_M, label='$D_M$ de la gaine')
plt.plot(Lambda*1e6,D_W1, label='$D_W$ 2% molaire GeO$_2$')
plt.plot(Lambda*1e6,D_W2, label='$D_W$ 8% molaire GeO$_2$')
plt.xlabel('$\lambda$ [$\mu$m]')
plt.ylabel('$D$ [ps/nm$\cdot$km]')
plt.xlim([1,1.5])
plt.legend()
plt.savefig('num4.jpg', dpi=600)
plt.show()

plt.figure(2)
plt.plot(Lambda*1e6,Tg1)
plt.plot(Lambda*1e6,Tg2)
plt.show()