import matplotlib.pyplot as plt
plt.style.use("bmh")

def general_plot(*args,firstFig=True,xlabel="",ylabel="",title="",linewidth=3,**kwargs):
    if firstFig:
        plt.figure(figsize=(10,7))
    plt.plot(linewidth=linewidth,*args,**kwargs)
    if xlabel != "":
        plt.xlabel(xlabel,fontsize=20)
    if ylabel != "":
        plt.ylabel(ylabel,fontsize=20)
    if title != "":
        plt.title(title,fontsize=20)

    plt.legend(loc=0,prop={'size': 15})
    plt.tick_params(labelsize=15)
    plt.tight_layout()
