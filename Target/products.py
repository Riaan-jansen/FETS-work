import matplotlib.pyplot as plt
import numpy as np

dict1 = {
        'proton'    : 4.28E-3,
        # 'deuteron'  : 2.16E-6,
        # 'tritium'   : 1.03E-7,
        # 'alpha'     : 2.81E-4,
        # 'helium-3'  : 3.67E-5,
        # # 'lithium-7' : 2.94E-8,
        # # ignoring li-7 and li-6
        # 'beryllium-7': 2.91E-4,
        # 'boron-10'  : 1.18E-7
        'other'     : 6.11E-4
        }

dict2 = {
        # 'proton'    : 4.28E-3,
        # 'deuteron'  : 2.16E-6,
        # 'tritium'   : 1.03E-7,
        'alpha'     : 2.81E-4 / 4.893e-3 ,
        'helium-3'  : 3.67E-5 / 4.893e-3 ,
        # 'lithium-7' : 2.94E-8,
        # ignoring li-7 and li-6
        'beryllium-7': 2.91E-4 / 4.893e-3 ,
        # 'boron-10'  : 1.18E-7
        'other'      : 2.3E-6 / 4.893e-3 
        }


labels1 = []
sizes1 = []

for key, value in dict1.items():
    labels1.append(key)
    sizes1.append(value)

#plt.pie(sizes1, labels=labels1, autopct='%1.1f%%')
#plt.show()

# https://matplotlib.org/stable/gallery/pie_and_polar_charts/bar_of_pie.html
from matplotlib.patches import ConnectionPatch

fig, (ax1, ax2) = plt.subplots(1,2, figsize=(9,5))
fig.subplots_adjust(wspace=0)

# pie chart parameters
overall_ratios = [ele for ele in dict2.values()]
labels = dict2.keys()
explode = [0.1, 0, 0]
# rotate so that first wedge is split by the x-axis
angle = -180 * overall_ratios[0]

wedges, *_ = ax1.pie(overall_ratios, autopct='%1.1f%%', startangle=angle,
                     labels=labels)

# bar chart parameters
other_lis = ['boron-10', 'deuteron', 'triton', 'beryllium-9']
other_tab = [1.18E-7 / 4.893e-3  ,  2.16E-6 / 4.893e-3  ,  1.03E-7 / 4.893e-3 ,  6.54E-9 / 4.893e-3 ]
bottom = 1
width = .2

# Adding from the top matches the legend.
for j, (height, label) in enumerate(reversed([*zip(other_tab, other_lis)])):
    bottom -= height
    bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                 alpha=0.1 + 0.25 * j)
    ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

ax2.set_title('Age of approvers')
ax2.legend()
ax2.axis('off')
ax2.set_xlim(- 2.5 * width, 2.5 * width)

# use ConnectionPatch to draw lines between the two plots
theta1, theta2 = wedges[0].theta1, wedges[0].theta2
center, r = wedges[0].center, wedges[0].r
bar_height = 1

# draw top connecting line
x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = r * np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
con.set_linewidth(4)
ax2.add_artist(con)

# draw bottom connecting line
x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = r * np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(4)

plt.show()