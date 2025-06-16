import os,glob,json,traceback
from abacustest.lib_collectdata.collectdata import RESULT
import numpy as np
# Can install abacustest by `pip install git+https://github.com/pxlxingliang/abacus-test.git@develop`

def plotvs(results,refs):
    all_examples = [i for i in results.keys()]
    ref_names = [i for i in refs.keys()]

    xys = {"abacus":[]}
    for i in ref_names:
        xys[i] = []

    for ie in all_examples:
        xys["abacus"].append(results[ie].get("band_gap",None))
        for iref in ref_names:
            xys[iref].append(refs[iref].get(ie,{}).get("band_gap",None))

    if "exp" in ref_names:
        x_name = "exp"
        x_title = "Experiment"
        y_names = ["abacus"] + ref_names
        y_names.remove("exp")
    else:
        x_name = x_title = "abacus"
        y_names = ref_names

    x = xys[x_name]
    y = [xys[i] for i in y_names]
    labels = y_names
    
    imax = max(x)
    imin = min(x)
    import matplotlib.pyplot as plt
    for idx,i in enumerate(y):
        plt.scatter(x,i,label=labels[idx],s=10)
        imax = max(imax,max(i))
        imin = min(imin,min(i))

    plt.xlim(imin-0.1,imax+0.1)
    plt.ylim(imin-0.1,imax+0.1)
    plt.plot([imin-0.1,imax+0.1],[imin-0.1,imax+0.1],linestyle="--",color="gray")
    plt.legend(title="")
    plt.xlabel(x_title+" band gap (eV)",fontsize=12)
    plt.ylabel('Other band gap (eV)',fontsize=12)
    #plt.title('',fontsize=16)
    plt.savefig('vs.png', dpi=300)

def plotvsbar(results,refs):
    all_examples = [i for i in results.keys()]
    ref_names = [i for i in refs.keys()]

    xys = {"abacus":[]}
    for i in ref_names:
        xys[i] = []

    for ie in all_examples:
        xys["abacus"].append(results[ie].get("band_gap",None))
        for iref in ref_names:
            xys[iref].append(refs[iref].get(ie,{}).get("band_gap",None))
    
    legend = ["abacus"] + ref_names
    
    plotbar(xys,(12, 5),all_examples,legend,"vsbar.png","Band gap (eV)","Band gap of different methods")

    if "exp" in legend:
        # plot the delta image
        delta = {}
        delta_percent = {}
        delta_legend = []
        for i in legend:
            if i != "exp":
                delta_percent[i] = []
                delta[i] = []
                for j in range(len(xys[i])):
                    if xys[i][j] != None and xys["exp"][j] != None :
                        delta[i].append(xys[i][j] - xys["exp"][j])
                        delta_percent[i].append((xys[i][j] - xys["exp"][j])*100/xys["exp"][j])
                    else:
                        delta[i].append(None)
                        delta_percent[i].append(None)
                delta_legend.append(i)
        plotbar(delta,(12, 5),all_examples,delta_legend,"delta-vsbar.png","Band gap (eV)","Relative error betweeen different methods and experiment")

        import matplotlib.pyplot as plt
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        plotsubbar(ax1,xys,all_examples,legend,"Band gap (eV)","Band gap of different methods and experiment")
        plotsubbar(ax2,delta,all_examples,delta_legend,"Band gap error (eV)","Band gap error betweeen different methods and experiment")
        plt.tight_layout()
        plt.savefig("all.png", dpi=300)

        plt.clf()
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        plotsubbar(ax1,xys,all_examples,legend,"Band gap (eV)","Band gap of different methods and experiment")
        plotsubbar(ax2,delta_percent,all_examples,delta_legend,"Relative error (%)","The relative error of different methods related to experimental band gap")
        plt.tight_layout()
        plt.savefig("all-percent.png", dpi=300)



def plotbar(init_xys,figsize,all_examples,legend,save_name,y_label,title):
    import matplotlib.pyplot as plt
    import copy
    xys = copy.deepcopy(init_xys)
    for ik,iv in xys.items():
        for j in range(len(iv)):
            if iv[j] == None:
                xys[ik][j] = 0

    plt.figure(figsize=figsize)
    bar_width = 0.15
    index = np.arange(len(all_examples))
    indexs = [index + bar_width*i for i in range(len(legend))]

    for i in range(len(legend)):
        plt.bar(indexs[i],xys[legend[i]],width=bar_width, label=legend[i])

    plt.xticks(index + 2 * bar_width, all_examples,rotation=30)
    plt.legend()
    #plt.xlabel(x_title+" band gap (eV)",fontsize=12)
    plt.ylabel(y_label,fontsize=12)
    plt.title(title)
    plt.savefig(save_name, dpi=300)

def plotsubbar(ax,init_xys,all_examples,legend,y_label,title):
    import copy
    xys = copy.deepcopy(init_xys)
    for ik,iv in xys.items():
        for j in range(len(iv)):
            if iv[j] == None:
                xys[ik][j] = 0

    bar_width = 0.15
    index = np.arange(len(all_examples))
    indexs = [index + bar_width*i for i in range(len(legend))]

    ymin = min(xys[legend[0]])
    ymax = max(xys[legend[0]])
    for i in range(len(legend)):
        ax.bar(indexs[i],xys[legend[i]],width=bar_width, label=legend[i])
        ymin = min(ymin,min(xys[legend[i]]))
        ymax = max(ymax,max(xys[legend[i]]))

    ax.set_xticks(index +  (len(xys)/2 - 0.5) * bar_width)
    ax.set_xticklabels(all_examples,rotation=15)
    ax.set_ylim(ymin-0.1,ymax+0.1)
    ax.legend()
    #plt.xlabel(x_title+" band gap (eV)",fontsize=12)
    ax.set_ylabel(y_label,fontsize=12)
    ax.set_title(title)

def gen_report(metrics,metrics_ref):
    report = {}
    for ik,iv in metrics.items():
        report[ik] = {}
        report[ik]["ABACUS"] = iv.get("band_gap",None)
        report[ik]["VASP"] = metrics_ref.get("vasp",{}).get(ik,{}).get("band_gap",None)
        report[ik]["QE"] = metrics_ref.get("qe",{}).get(ik,{}).get("band_gap",None)
        report[ik]["FHI-AIMS"] = metrics_ref.get("fhi-aims",{}).get(ik,{}).get("band_gap",None)
        report[ik]["Exp."] = metrics_ref.get("exp",{}).get(ik,{}).get("band_gap",None)
        comp_ref = [i for i in [report[ik]["VASP"],report[ik]["QE"],report[ik]["FHI-AIMS"]] if i != None]
        if len(comp_ref) == 0:
            report[ik]["comp_ref_mean"] = None
        else:
            report[ik]["comp_ref_mean"] = sum(comp_ref)/len(comp_ref)
        report[ik]["RE(Exp,%)"] = None if report[ik]["Exp."] == None or report[ik]["ABACUS"] == None else (report[ik]["ABACUS"] - report[ik]["Exp."])/report[ik]["Exp."]*100
        report[ik]["RE(comp_ref_mean,%)"] = None if report[ik]["comp_ref_mean"] == None or report[ik]["ABACUS"] == None else (report[ik]["ABACUS"] - report[ik]["comp_ref_mean"])/report[ik]["comp_ref_mean"]*100
    json.dump(report,open("report.json","w"),indent=4)
    

def produce_super_metrics(ref_file_name,metrics_file,example_list):
    results = json.load(open(metrics_file))
    ref_data = json.load(open(ref_file_name))
    
    gen_report(results,ref_data)
    plotvsbar(results,ref_data)

if __name__ == "__main__":
    produce_super_metrics("metrics_ref.json","metrics.json",["*"])

