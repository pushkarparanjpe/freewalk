'''
Created on 16-Apr-2014

@author: pushkar
'''

from analyze import Analyze
from sys import argv
from os import listdir, pardir
from os.path import join as pjoin, isdir, abspath
import matplotlib.pyplot as plt
from HTML import table


# Leg order
legs = ['L1', 'R1', 'L2', 'R2', 'L3', 'R3']
# Contra pair order
contralateral_pairs = map(str, [1, 2, 3])
# Ipsi pair order
ipsilateral_pairs = map(str, [1, 2, 3, 4])



# datasets = ["CTRL", "EXP"]
datasets = ["CTRL"]

# paths = [argv[1], argv[2]]
paths = [argv[1]]



rootpath = abspath(pjoin(argv[1], pardir))

dpaths = dict(zip(datasets, paths))

colors = ['#348ABD', '#7A68A6', '#A60628', '#467821', '#CF4457', '#188487', '#E24A33']
colormap = dict(zip(datasets, colors))

megabucket = dict(zip(datasets, [[] for k in range(len(datasets))]))

ext = '.png'

def plotMegaBucket(entities, datasets, MegaBucket, ylimspec=None, label=None):
    fig, ax = plt.subplots()
    data2d = []
    for entity in entities:
        for dset in datasets:
            print(dset)
            data2d.append(MegaBucket[dset][entity])
    print data2d
    bp = plt.boxplot(data2d, patch_artist=True)
    [bp['boxes'][box].set_facecolor(colors[0]) for box in range(len(bp['boxes'])) if box % 2 == 0]
    [bp['boxes'][box].set_facecolor(colors[1]) for box in range(len(bp['boxes'])) if box % 2 != 0]
    if(ylimspec):
        plt.ylim(ylimspec)
    if label:
        ax.set_ylabel(label[0])
        ax.set_title(label[1])
    locs, ticks = plt.xticks()
    ticks = entities
    plt.xticks(locs, ticks)
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
    
        stack_names = sorted(
                    [ name for name in listdir(path)
                        if not name.lower().count("unusable")
                        if not name.lower().count("ignore")
                        if isdir(pjoin(path, name))]
                    )
        
        print stack_names

        entities = {
                      # legs
                      'LEG_BODY_ANGLE' : legs,
                      'SWING_AMPLITUDE' : legs,
                      'SWING_DURATION'  : legs,
                      'STANCE_DURATION' : legs,
                      'AEPx'            : legs,
                      'PEPx'            : legs,
                      'AEA'             : legs,
                      'PEA'             : legs,
                      
                      # contralateral_pairs
                      'CCI'             : contralateral_pairs,
                      
                      # ipsi_lateral_pairs
                      'ICI'             : ipsilateral_pairs,
                      
                      'WALK_SPEED'      : ['Speed']
                    }

        holder = [[] for k in range(len(entities[param]))]
        bucket = dict(zip(entities[param], holder))
        
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
                      }
            
            bucket = filledBucket(bucket, entities[param], funcky[param])
    
    
        ylims = {
                      # legs
                      'LEG_BODY_ANGLE'  : (-200, 200),
                      'SWING_AMPLITUDE' : (0, 1600),
                      'SWING_DURATION'  : (0, 70),
                      'STANCE_DURATION' : (0, 150),
                      'AEPx'            : (-2000, 2000),
                      'PEPx'            : (-2000, 2000),
                      'AEA'             : (-200, 200),
                      'PEA'             : (-200, 200),
                      
                      # contralateral_pairs
                      'CCI'             : (-1.0, 1.0),
                      
                      # ipsi_lateral_pairs
                      'ICI'             : (-1.0, 1.0),

                      'WALK_SPEED'      :(0, 40),
                 }
        
        labels = {
                      # legs
                      'LEG_BODY_ANGLE'  : ('Degrees', 'Leg-Body Angle'),
                      'SWING_AMPLITUDE' : ('um', 'Swing Amplitude'),
                      'SWING_DURATION'  : ('ms', 'Swing Duration'),
                      'STANCE_DURATION' : ('ms', 'Stance Duration'),
                      'AEPx'            : ('um', 'Anterior Extreme Position w.r.t. X'),
                      'PEPx'            : ('um', 'Posterior Extreme Position w.r.t. X'),
                      'AEA'             : ('Degrees', 'Anterior Extreme Angle'),
                      'PEA'             : ('Degrees', 'Posterior Extreme Angle'),
                      
                      # contralateral_pairs
                      'CCI'             : ('/s', 'Contra-lateral Coordination Index'),
                      
                      # ipsi_lateral_pairs
                      'ICI'             : ('/s', 'Ipsi-lateral Coordination Index'),

                      'WALK_SPEED'      : ('mm/s', 'Average Walking Speed'),
                 }
        
        # print bucket
        megabucket[dset] = bucket
        
        megabucket['PARAM'] = param
        megabucket['X-TICKS'] = entities[param]
        megabucket['IMGPATH'] = rootpath
    
    plotMegaBucket(entities[param], datasets, megabucket, ylims[param], labels[param])


def html(stuff):
    return '<HTML><BODY>' + rootpath + stuff + '</BODY></HTML>'


def img(path):
    return ['<img src="' + path + '" width="500" height="400">']


def save(stuff, path):
    with open(path, 'w') as f:
        f.write(stuff)


plots = ['WALK_SPEED', 'SWING_AMPLITUDE', 'SWING_DURATION', 'STANCE_DURATION', 'AEPx', 'PEPx', 'LEG_BODY_ANGLE', 'AEA', 'PEA', 'CCI', 'ICI']

map(makePlotFor, plots)

print 'MegaBucket >>', megabucket


print 'Generating HTML report...'
implots = [pjoin(rootpath, im + '_box' + ext) for im in plots]
imgs = map(img, implots)
save(html(table(imgs)), pjoin(rootpath, 'index.html'))
print 'Saved.'







