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

data = np.genfromtxt(sys.argv[1], delimiter=',')

fig, ax1 = plt.subplots()
plt.grid()
plt.ylabel(r'$\alpha$: Load Factor',**font_label)
plt.xlabel("Fingerprint Size in bits",**font_label)

ax1.set_ylim(0, 1)
# plt.xticks(np.arange(50, 1000, 50))
# plt.xticks(['a','b'])
for spine in plt.gca().spines.values():
        spine.set_visible(False)

p1 = plt.plot(data[:20,2], data[:20,-1], 'r', linewidth=5,  markersize=10,label=r'b=$2^{15}$')
p2 = plt.plot(data[21:40,2], data[21:40,-1], 'g', linewidth=5,  markersize=10,label=r'b=$2^{16}$')
p3 = plt.plot(data[41:60,2], data[41:60,-1], 'b', linewidth=5,  markersize=10,label=r'b=$2^{17}$')
p4 = plt.plot(data[61:80,2], data[61:80,-1], 'm', linewidth=5,  markersize=10,label=r'b=$2^{18}$')

plt.legend()
plt.savefig('fig2a.png', format='png', dpi=300, bbox_inches='tight')
plt.show()