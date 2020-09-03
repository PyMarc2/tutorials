import numpy as np
import matplotlib.pyplot as plt
from general_plot import *
from scipy.special import jn_zeros, kn

## Paramètres connus

a = 4.6e-6            # [m] (rayon du coeur)
r = 62.5e-6           # [m] (rayon de la gaine)
wvl_pulse = 1.55e-6   # [m] (longueur d'onde du pulse)
T0 = 0.1e-12         # [s] (largeur de l'impulsion)
x = 0.04              # [-] (fraction molaire de GeO2)
prop = 0.0435         # [-] (propriétés de la silice = |p11 - p12|(1+\nu) )
c0 = 3e8              # [m/s] (Vitesse de la lumière dans le vide)


## Dispersion et Sellmeier

A_SiO2 = [0.6961663, 0.4079426, 0.8974794]     # Coefficients A de Sellmeier du SiO2 (https://refractiveindex.info/?shelf=main&book=SiO2&page=Malitson)
l_SiO2 = [0.0684043, 0.1162414, 9.896161]      # Coefficients lambda de Sellmeier du SiO2 (https://refractiveindex.info/?shelf=main&book=SiO2&page=Malitson)
A_GeO2 = [0.80686642, 0.71815848, 0.85416831]  # Coefficients A de Sellmeier du GeO2 (https://refractiveindex.info/?shelf=main&book=GeO2&page=Fleming)
l_GeO2 = [0.068972606, 0.15396605, 11.841931]  # Coefficients lambda de Sellmeier du GeO2 (https://refractiveindex.info/?shelf=main&book=GeO2&page=Fleming)


def Sellmeier(wvl):
    """
    Fonction qui calcule l'indice de réfraction (n) et la dérivée de l'indice de réfraction (dn/dl) en fonction de la
    longueur d'onde (Éq. de Sellmeier à 3 termes), pour le coeur (Si+Ge) (1) et la gaine (2) (Si pur).
    :param wvl: Longueur d'onde [µm]
    :return: n et dn/dl évalué à la longueur d'onde voulue.
    """
    wvl = wvl * 1e6
    sum_sellmeier1 = 0
    sum_sellmeier_deriv1 = 0
    sum_sellmeier2 = 0
    sum_sellmeier_deriv2 = 0
    i = 0
    while i < 3:
        A = A_SiO2[i] + x*(A_GeO2[i] - A_SiO2[i])
        l = l_SiO2[i] + x*(l_GeO2[i] - l_SiO2[i])
        term_sellmeier1 = (A * wvl**2) / (wvl**2 - l**2)
        term_sellmeier_deriv1 = (2 * A * l**2 * wvl) / (wvl**2 - l**2)**2
        sum_sellmeier1 += term_sellmeier1
        sum_sellmeier_deriv1 += term_sellmeier_deriv1
        term_sellmeier2 = (A_SiO2[i] * wvl**2) / (wvl**2 - l_SiO2[i]**2)
        term_sellmeier_deriv2 = (2 * A_SiO2[i] * l_SiO2[i]**2 * wvl) / (wvl**2 - l_SiO2[i]**2)**2
        sum_sellmeier2 += term_sellmeier2
        sum_sellmeier_deriv2 += term_sellmeier_deriv2
        i += 1

    n1 = np.sqrt(1 + sum_sellmeier1)
    nprime1 = -1 / (2*n1) * sum_sellmeier_deriv1
    n2 = np.sqrt(1 + sum_sellmeier2)
    nprime2 = -1 / (2*n2) * sum_sellmeier_deriv2

    return n1, nprime1, n2, nprime2

n1, n1prime, n2, n2prime = Sellmeier(wvl_pulse)


## Longueurs de fibre nécessaires en fonction du rayon de courbure imposé:

R = np.linspace(0.0001,0.05,1000)  # [m] (Vecteur de rayons de courbures)

print("T0 = ",T0)
L = (2*T0 * c0 * R**2) / (prop * r**2 * n1**2) * 1/(n1 - 3*wvl_pulse * n1prime)  # [m] (Vecteur de longueurs de fibre)


## Graphique
general_plot(R*100,L,"-",xlabel="Rayon de courbure de la boucle [cm]",ylabel="Longueur de fibre nécessaire [m]",color="C1")
#plt.show()

## Considération de la dispersion de la vitesse de groupe
# n1_fct = lambda wvl: Sellmeier(wvl)[0]
# n2_fct = lambda wvl: Sellmeier(wvl)[2]
# k0_fct = lambda wvl: 2*np.pi / wvl
# V_fct = lambda wvl: k0_fct(wvl) * a * np.sqrt(n1_fct(wvl)**2 - n2_fct(wvl)**2)
# K_fct = lambda wvl: V_fct(wvl)/a
# Delta_fct = lambda wvl: (n1_fct(wvl) - n2_fct(wvl)) / n1_fct(wvl)
# beta_fct = lambda wvl: (K_fct(wvl)**2 + np.sqrt(K_fct(wvl)**4 - 4*k0_fct(wvl)*n2_fct(wvl)*Delta_fct(wvl)*(K_fct(wvl)**2 * k0_fct(wvl) * n2_fct(wvl) - k0_fct(wvl)**3 * n2_fct(wvl)**3 * Delta_fct(wvl)))) / (2*k0_fct(wvl)*n2_fct(wvl)*Delta_fct(wvl))
# w_fct = lambda wvl: a*np.sqrt(beta_fct(wvl)**2 - k0_fct(wvl)**2 * n2_fct(wvl)**2)
# n_effx_fct = lambda wvl: n2_fct(wvl) * (1 + Delta_fct(wvl) * (w_fct(wvl)/V_fct(wvl))**2)
# # B = prop * n1**3 * (r/R)**2
# # n_effy = n_effx + B  # ou -
#
# list_wvl = np.linspace(1525e-9,1575e-9,1000)
# param = np.polyfit(list_wvl,n_effx_fct(list_wvl),1)
# print(param)
# general_plot(list_wvl*1e9,n_effx_fct(list_wvl))
# plt.show()


## V2
n1_fct = lambda wvl: Sellmeier(wvl)[0]
n2_fct = lambda wvl: Sellmeier(wvl)[2]
n2prime_fct = lambda wvl: Sellmeier(wvl)[3]
N2_fct = lambda wvl: n2_fct(wvl) - wvl * n2prime_fct(wvl)
Delta_fct = lambda wvl: (n1_fct(wvl) - n2_fct(wvl)) / n1_fct(wvl)
V_fct = lambda wvl: (2 * np.pi * a) / wvl * np.sqrt(n1_fct(wvl)**2 - n2_fct(wvl)**2)
u_inf = jn_zeros(0,1)[0]
u_fct = lambda wvl: u_inf * V_fct(wvl)/(V_fct(wvl)+1) * (1 - (u_inf**2)/(6*(V_fct(wvl)+1)**3) - (u_inf**4)/(20*(V_fct(wvl)+1)**5))
w_fct = lambda wvl: np.sqrt(V_fct(wvl)**2 - u_fct(wvl)**2)
psi_fct = lambda wvl: kn(0,w_fct(wvl))**2 / (kn(1,w_fct(wvl))*kn(-1,w_fct(wvl)))
Vbprime_fct = lambda wvl: 1 - (u_fct(wvl)/V_fct(wvl))**2 * (1-2*psi_fct(wvl))

N_fct = lambda wvl: N2_fct(wvl)*(1 + Delta_fct(wvl) * Vbprime_fct(wvl))

wvl_sampling = np.linspace(1.53e-6,1.57e-6,1000)
h = wvl_sampling[1] - wvl_sampling[0]
Nprime = (N_fct(1.55e-6 + h) - N_fct(1.55e-6 - h)) / (2*h)

beta_2 = - wvl_pulse**2 / (2*np.pi * c0**2) * Nprime

L_lim = T0**2 / beta_2 * np.sqrt(3)
print("Longueur maximale de fibre = ",L_lim*100, " cm")


## Atténuation
alpha_IR = 7.81e11 * np.exp(-48.48/(wvl_pulse*1e6)) * 1e-3  # atténuation dans l'IR (1.55 µm) [dB/m]
delta_nGe = abs(n2 - n1)  # Variation de n due au Ge
alpha_R = (0.75 + 66*delta_nGe) / ((wvl_pulse*1e6)**4) * 1e-3  # [dB/m]
Ac = (1/2) * np.sqrt(np.pi / (a * w_fct(wvl_pulse)**3)) * (u_fct(wvl_pulse) / (w_fct(wvl_pulse) * kn(0,w_fct(wvl_pulse))))**2
K = (4 * (n1 - n2) * w_fct(wvl_pulse)**3) / (3*a*V_fct(wvl_pulse)**2 * n2)
alpha_c = Ac / np.sqrt(R) * np.exp(-K*R)  # [dB/m]
alpha_c_tot = alpha_c * 2*np.pi*R

alpha_tot = (alpha_IR + alpha_R) * L + alpha_c_tot
P = np.exp(-alpha_tot*np.log(10)/10)
general_plot(R*100,np.exp(-alpha_IR*L*np.log(10)/10),label="Absorption intrinsèque",linestyle="--",linewidth=1)
general_plot(R*100,np.exp(-alpha_R*L*np.log(10)/10),firstFig=False,label="Diffusion de Rayleigh",linestyle="--",linewidth=1)
general_plot(R*100,np.exp(-alpha_c_tot*np.log(10)/10),firstFig=False,label="Pertes par courbure",linestyle="--",linewidth=1)
general_plot(R*100,P,firstFig=False,xlabel="Rayon de courbure de la boucle [cm]",ylabel="Fraction de puissance transmise [-]",label="Pertes totales")
plt.xlim(0.8,5.0)
plt.ylim(0.86,1.01)
plt.tight_layout()
#plt.show()
general_plot(R*100,np.exp(-alpha_IR*L*np.log(10)/10),label="Absorption intrinsèque",linestyle="--",linewidth=1)
general_plot(R*100,np.exp(-alpha_R*L*np.log(10)/10),firstFig=False,label="Diffusion de Rayleigh",linestyle="--",linewidth=1)
general_plot(R*100,np.exp(-alpha_c_tot*np.log(10)/10),firstFig=False,label="Pertes par courbure",linestyle="--",linewidth=1)
general_plot(R*100,P,firstFig=False,xlabel="Rayon de courbure de la boucle [cm]",ylabel="Fraction de puissance transmise [-]",label="Pertes totales")


print("R suggéré pour pertes min = ",R[np.argmax(P)] * 100," cm")
print("Longueur associée = ",L[np.argmax(P)]," m")
print("Puissance max () = ",np.max(P))
plt.show()
