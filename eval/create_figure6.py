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

data_bl = 527733.3773939166 / 1000
data_cu = 137303.61457201128 / 1000
data_cb = 62394.489534628825 / 1000

fig, ax1 = plt.subplots()
plt.grid(axis="y")
plt.ylabel(r'Query tput (KQPS)',**font_label)
plt.xlabel(r'Data Structure',**font_label)

# ax1.set_ylim(0, 400)
ax1.set_xticklabels(["", "Bloom \nFilter", "Cuckoo \nFilter","Cuckoo \nFilter\n(Bitarray)"])
# plt.xticks(['a','b'])
for spine in plt.gca().spines.values():
        spine.set_visible(False)

width = 0.2
ind = np.arange(1)

p1 = plt.bar(ind - width, data_bl, width=width, color='red', label=r'Bloom Filter')
p2 = plt.bar(ind, data_cu,  width=width, color='blue', label=r'Cuckoo Filter')
p3 = plt.bar(ind + width, data_cb,  width=width,color='green', label=r'Cuckoo Filter(Bit)')

# plt.legend()
plt.savefig('fig6.png', format='png', dpi=300, bbox_inches='tight')
plt.show()