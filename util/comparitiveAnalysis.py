'''
Created on 16-Apr-2014

@author: pushkar
'''

from analyze import Analyze
from sys import argv
from os import listdir, pardir
from os.path import join as pjoin, isdir, abspath, basename
import matplotlib.pyplot as plt
from HTML import table
from pylab import mean, GridSpec
from scipy.stats import ttest_ind


# Leg order
legs = ['L1', 'R1', 'L2', 'R2', 'L3', 'R3']
# Contra pair order
contralateral_pairs = map(str, [1, 2, 3])
# Ipsi pair order
ipsilateral_pairs = map(str, [1, 2, 3, 4])
concurrency_states = map(str, [3, 2, 1, 0])



datasets = ["CTRL", "EXP"]
# datasets = ["CTRL"]

paths = [argv[1], argv[2]]
# paths = [argv[1]]



rootpath = abspath(pjoin(argv[1], pardir))

dpaths = dict(zip(datasets, paths))

colors = ['#348ABD', '#7A68A6', '#A60628', '#467821', '#CF4457', '#188487', '#E24A33']
colors_grad = dict(zip(datasets, [['#348ABD', '#459BCE', '#56ACDF', '#67BDEF'], ['#7A68A6', '#8B79B7', '#9C8AC8', '#AD9BD9']]))
colormap = dict(zip(datasets, colors))

megabucket = dict(zip(datasets, [[] for k in range(len(datasets))]))

#ext = '.png'
ext = '.svg'



def plotMegaBucket(plot_type, entities, datasets, MegaBucket, ylimspec=None, label=None, title=None):
    fig = None
    ax = None
    
    if plot_type == 'PIE':
        ax = []
        fig = plt.figure()
        ctr = 0
        for dset in datasets:
            meanps = [mean(MegaBucket[dset][entity]) for entity in entities]
            print 'Fracs', meanps
            ax.append(plt.subplot(1, 2, ctr + 1))
            wedges, texts = plt.pie(meanps, labels=map(str, entities), explode=[0.08, 0, 0, 0], colors=['r', 'g', 'b', 'w'])  # colors=colors_grad[dset])
            for w in wedges:
                # w.set_linewidth(1)
                w.set_edgecolor('black')
            ctr += 1
        # for axis in ax: axis.set_title(label)
        fig.suptitle(title, size=20)

    if plot_type == 'BOX':
        fig, ax = plt.subplots()
        data2d = []
        ticks = []
        for entity in entities:
            for dset in datasets:
                print dset
                data2d.append(MegaBucket[dset][entity])
                ticks.append(entity)
        print 'DATA', data2d
        print 'MAX', max(data2d)    
        bp = plt.boxplot(data2d, patch_artist=True)
        [bp['boxes'][box].set_facecolor(colors[0]) for box in range(len(bp['boxes'])) if box % 2 == 0]
        [bp['boxes'][box].set_facecolor(colors[1]) for box in range(len(bp['boxes'])) if box % 2 != 0]
        
        if(ylimspec):
            plt.ylim(ylimspec)
        locs, oldticks = plt.xticks()
        # ticks = entities
        plt.xticks(locs, ticks)
            
        if label:
            ax.set_ylabel(label)
        if title:
            ax.set_title(title)
            
        # calc. and disp. stats
        # assumes that data2d has data arranged as [(ctrl,exp), (ctrl,exp), (ctrl,exp), ...]
        tstats = [ttest_ind(data2d[samk], data2d[samk + 1], equal_var=False)[1] for samk in range(0, len(data2d), 2)]
        print 'P values', tstats
        marker_tstats = []
        tstats_mem = []
        for k in range(len(tstats)):
            if tstats[k] < 0.05:
                marker_tstats.append((k * 2) + 1 + 1)
                tstats_mem.append(tstats[k])
            else:
                tstats_mem.append('n.s.')
        print marker_tstats
        h = max(ylimspec) * 0.95
        statx = marker_tstats
        staty = [h] * len(marker_tstats)
        sp = plt.plot(statx, staty, linestyle="None", color='black', marker="*", markersize=15)
        for i, j in zip(statx, staty):
            pvalue = round(tstats_mem[(i - 1) / 2], 3)
            ax.annotate(pvalue, xy=(i + 0.05, j + 0.5))
        #

    # plt.show(block=True)
    print MegaBucket['PARAM']
    imgpath = pjoin(MegaBucket['IMGPATH'], MegaBucket['PARAM'] + "_box" + ext)
    plt.savefig(imgpath)


def filledBucket(bucket, entities, func):
    # fill the bucket
    for entity in entities:
            bucket[entity].extend(func(entity))
    # return the bucket
    return bucket


def makePlotFor(param):
    for dset in datasets:
        print 'Extracting from', dset
        print '-------------------------------'
        path = dpaths[dset]
        
        print 'ANALYZING', path
    
        stack_names = sorted(
                    [ name for name in listdir(path)
                            if not name.lower().count("unusable")
                            if not name.lower().count("ignore")
                            if isdir(pjoin(path, name))]
                    )
        
        print 'Stacks', stack_names

        specs = {
                  'LEG_BODY_ANGLE'    :   {'PLOT':'BOX', 'ENTITIES':legs, 'YLIMS':(-200, 200), 'YLABEL':'Degrees', 'TITLE':'Leg-Body Angle'},
                  'SWING_AMPLITUDE'   :   {'PLOT':'BOX', 'ENTITIES':legs, 'YLIMS':(0, 2000), 'YLABEL':'um', 'TITLE':'Swing Amplitude'},
                  'SWING_DURATION'    :   {'PLOT':'BOX', 'ENTITIES':legs, 'YLIMS':(0, 70), 'YLABEL':'ms', 'TITLE':'Swing Duration'},
                  'STANCE_DURATION'   :   {'PLOT':'BOX', 'ENTITIES':legs, 'YLIMS':(0, 200), 'YLABEL':'ms', 'TITLE':'Stance Duration'},
                  'AEPx'              :   {'PLOT':'BOX', 'ENTITIES':legs, 'YLIMS':(-2500, 2500), 'YLABEL':'um', 'TITLE':'Anterior Extreme Position w.r.t. X'},
                  'PEPx'              :   {'PLOT':'BOX', 'ENTITIES':legs, 'YLIMS':(-2500, 2500), 'YLABEL':'um', 'TITLE':'Posterior Extreme Position w.r.t. X'},
                  'AEA'               :   {'PLOT':'BOX', 'ENTITIES':legs, 'YLIMS':(-200, 200), 'YLABEL':'Degrees', 'TITLE':'Anterior Extreme Angle'},
                  'PEA'               :   {'PLOT':'BOX', 'ENTITIES':legs, 'YLIMS':(-200, 200), 'YLABEL':'Degrees', 'TITLE':'Posterior Extreme Angle'},
                  'CCI'               :   {'PLOT':'BOX', 'ENTITIES':contralateral_pairs, 'YLIMS':(0.75, 1.02), 'YLABEL':'/s', 'TITLE':'Contra-lateral Coordination Index'},
                  'ICI'               :   {'PLOT':'BOX', 'ENTITIES':ipsilateral_pairs, 'YLIMS':(0.75, 1.02), 'YLABEL':'/s', 'TITLE':'Ipsi-lateral Coordination Index'},
                  'WALK_SPEED'        :   {'PLOT':'BOX', 'ENTITIES':['Speed'], 'YLIMS':(0, 40), 'YLABEL':'mm/s', 'TITLE':'Average Walking Speed'},
                  'STOLEN_SWINGS'     :   {'PLOT':'BOX', 'ENTITIES':['Swings/cycle'], 'YLIMS':(0, 1.2), 'YLABEL':'#/cycle', 'TITLE':'Stolen Swings Per Cycle'},
                  'CONCURRENCY'       :   {'PLOT':'PIE', 'ENTITIES':concurrency_states, 'YLIMS':(0, 100.0), 'YLABEL':'%', 'TITLE':'Proportional Concurrency States\n%'},
                  }

        holder = [[] for k in range(len(specs[param]['ENTITIES']))]
        bucket = dict(zip(specs[param]['ENTITIES'], holder))
        
        for stack_name in stack_names:
            ana = Analyze(pjoin(path, stack_name))
            
            funcky = {
                      # legs
                      'LEG_BODY_ANGLE'  : ana.getLegBodyAngles,
                      'SWING_AMPLITUDE' : ana.getSwingAmplitude,
                      'SWING_DURATION'  : ana.getSwingDuration,
                      'STANCE_DURATION' : ana.getStanceDuration,
                      'AEPx'            : ana.getAEPx,
                      'PEPx'            : ana.getPEPx,
                      'AEA'             : ana.getAEA,
                      'PEA'             : ana.getPEA,
                      
                      # contralateral_pairs
                      'CCI'             : ana.getCCI,
                      
                      # ipsi_lateral_pairs
                      'ICI'             : ana.getICI,
                      
                      'WALK_SPEED'      : ana.getWalkingSpeed,
                      
                      'STOLEN_SWINGS'   : ana.getStolenSwings,
                      'CONCURRENCY'     : ana.getConcurrency
                      }
            
            bucket = filledBucket(bucket, specs[param]['ENTITIES'], funcky[param])
    
        
 
        # print bucket
        megabucket[dset] = bucket
        
        megabucket['PARAM'] = param
        megabucket['X-TICKS'] = specs[param]['ENTITIES']
        megabucket['IMGPATH'] = rootpath
    
    spec = specs[param]
    plotMegaBucket(spec['PLOT'], spec['ENTITIES'], datasets, megabucket, spec['YLIMS'], spec['YLABEL'], spec['TITLE'])


def html(stuff):
    return '<HTML><BODY>' + rootpath + stuff + '</BODY></HTML>'


def img(path):
    # return ['<img src="' + path + '" width="500" height="400">']
    return ['<img src="' + basename(path) + '" width="500" height="400">']


def save(stuff, path):
    with open(path, 'w') as f:
        f.write(stuff)


plots = ['WALK_SPEED', 'SWING_AMPLITUDE', 'SWING_DURATION', 'STANCE_DURATION', 'AEPx', 'PEPx', 'LEG_BODY_ANGLE', 'AEA', 'PEA', 'CCI', 'ICI', 'STOLEN_SWINGS', 'CONCURRENCY']
#plots = ['CONCURRENCY']
#plots = ['SWING_AMPLITUDE']
#plots = ['PEA']

map(makePlotFor, plots)

print 'MegaBucket >>', megabucket


print 'Generating HTML report...'
implots = [pjoin(rootpath, im + '_box' + ext) for im in plots]
imgs = map(img, implots)
save(html(table(imgs)), pjoin(rootpath, 'index.html'))
print 'Saved.'







