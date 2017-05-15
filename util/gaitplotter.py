import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


colordefs = ['#ffffff', '#188487','#A60628', ]

a = [0,0,0,1,1,1,2,2,2,2,1,1,1,1,1,0,0,0,0,0,0]*10

acolors = [colordefs[k] for k in a]

l = range(len(a))

h = [5] * len(a)

b = [1] * len(a)

fig, ax = plt.subplots()

for bv in range(1,7):
	plt.bar(l,h,bottom=[bv*6]*len(a), color=acolors)


ax.set_ylim(0,50)

plt.show(block=True)





