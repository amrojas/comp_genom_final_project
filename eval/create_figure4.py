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
plt.ylabel(r'Bits per item to achieve $\epsilon$',**font_label)
plt.xlabel(r'$\epsilon$: target false positive probability',**font_label)

ax1.set_ylim(0, 400)
ax1.set_xticklabels(["", "0.001%","0.01%","0.1%","1%","10%"])
# plt.xticks(['a','b'])
for spine in plt.gca().spines.values():
        spine.set_visible(False)

x = np.arange(len(data_cu))

p1 = plt.plot(x, data_bl[:,-2], 'r', linewidth=5,  markersize=10,label=r'Bloom Filter')
p2 = plt.plot(x, data_cu[:,-2], 'b', linewidth=5,  markersize=10,label=r'Cuckoo Filter')
p3 = plt.plot(x, data_cb[:,-2], 'g', linewidth=5,  markersize=10,label=r'Cuckoo Filter(Bit)')

plt.legend()
plt.savefig('fig4.png', format='png', dpi=300, bbox_inches='tight')
plt.show()