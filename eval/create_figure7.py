import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

font = {'family' : 'normal',
        # 'weight' : 'bold',
        'size'   : 18}
font_label = {'family' : 'normal',
        # 'weight' : 'bold',
        'size'   : 18}

plt.rc('font', **font)
plt.rc('legend', fontsize=16)

data_bl = np.genfromtxt(sys.argv[1], delimiter=',')
data_cu = np.genfromtxt(sys.argv[2], delimiter=',')
data_cb = np.genfromtxt(sys.argv[3], delimiter=',')

fig, ax1 = plt.subplots()
plt.grid()
plt.ylabel(r'Insert tput (KOPS)',**font_label)
plt.xlabel(r'$\alpha$: table occupancy',**font_label)

# ax1.set_ylim(0, 400)
# ax1.set_xticklabels(["", "0.001%","0.01%","0.1%","1%","10%"])
# plt.xticks(['a','b'])
for spine in plt.gca().spines.values():
        spine.set_visible(False)

x1 = np.arange(len(data_bl))
x2 = np.arange(len(data_cu))
x3 = np.arange(len(data_cb))

p1 = plt.plot(x1, data_bl/1000, 'r', linewidth=5,  markersize=10,label=r'Bloom Filter')
p2 = plt.plot(x2, data_cu/1000, 'b', linewidth=5,  markersize=10,label=r'Cuckoo Filter')
p3 = plt.plot(x3, data_cb/1000, 'g', linewidth=5,  markersize=10,label=r'Cuckoo Filter(Bit)')

plt.legend()
plt.savefig('fig7.png', format='png', dpi=300, bbox_inches='tight')
plt.show()