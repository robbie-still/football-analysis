import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from PIL import Image
import requests
from io import BytesIO
from highlight_text import htext

background = "#242424"
text_colour = "w"
filler = "darkslategray"
primary = "#F59F45"
secondary = "#136D99"
title_font = "Helvetica"
mpl.rcParams['xtick.color'] = text_colour
mpl.rcParams['ytick.color'] = text_colour

def _invert(x, limits):
    """inverts a value x on a scale from
    limits[0] to limits[1]"""
    return limits[1] - (x - limits[0])

def _scale_data(data, ranges):
    """scales data[1:] to ranges[0],
    inverts if the scale is reversed"""
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        assert (y1 <= d <= y2) or (y2 <= d <= y1)
    x1, x2 = ranges[0]
    d = data[0]
    if x1 > x2:
        d = _invert(d, (x1, x2))
        x1, x2 = x2, x1
    sdata = [d]
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        if y1 > y2:
            d = _invert(d, (y1, y2))
            y1, y2 = y2, y1
        sdata.append((d-y1) / (y2-y1)
                     * (x2 - x1) + x1)
    return sdata

class ComplexRadar():
    def __init__(self, fig, variables, ranges,
                 n_ordinate_levels=6):
        angles = np.arange(0, 360, 360./len(variables))
        axes = [fig.add_axes([0.1,0.1,0.9,0.9],polar=True,
                label = "axes{}".format(i), zorder = 1)
                for i in range(len(variables))]
        l, text = axes[0].set_thetagrids(angles,
                                         labels=variables, color = text_colour, zorder = 1)
        [txt.set_rotation(angle-90) for txt, angle
             in zip(text, angles)]
        for ax in axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)
        for i, ax in enumerate(axes):
            grid = np.linspace(*ranges[i],
                               num=n_ordinate_levels)
            gridlabel = ["{}".format(round(x,2), color = text_colour, zorder = 1)
                         for x in grid]
            if ranges[i][0] > ranges[i][1]:
                grid = grid[::-1] # hack to invert grid
                          # gridlabels aren't reversed
            gridlabel[0] = "" # clean up origin
            ax.set_rgrids(grid, labels=gridlabel,
                         angle=angles[i], color = text_colour, zorder = 1)
            ax.spines["polar"].set_visible(False)
            ax.set_ylim(*ranges[i])
            ax.tick_params(axis='both', which='major', pad=15, color = text_colour, labelsize = 7, zorder = 1)
            ax.set_facecolor(background)
        # variables for plotting
        self.angle = np.deg2rad(np.r_[angles, angles[0]])
        self.ranges = ranges
        self.ax = axes[0]
    def plot(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)
    def fill(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)


df = pd.read_excel(r'radar templates/radar full back template.xlsx')
print(df)

playerone = tuple(df.iloc[1:11,1])
print(playerone)
playertwo = tuple(df.iloc[1:11,2])
print(playertwo)

columnsNamesArr = df.columns.values

variables = tuple(df.iloc[1:11,0])

ranges = list(zip(df.Max[1:11], df.Min[1:11]))

fig1 = plt.figure(figsize=(6, 6))
fig1.set_facecolor(background)
radar = ComplexRadar(fig1, variables, ranges, 6)
radar.plot(playerone, color = primary, zorder =2)
radar.fill(playerone, alpha=0.3, color = primary, zorder =2)
radar.plot(playertwo, color = secondary, zorder =2)
radar.fill(playertwo, alpha=0.5, color = secondary, zorder =2)

s = "Comparing <{}> with <{}>\n"
htext.fig_htext(s.format(columnsNamesArr[1],columnsNamesArr[2]),0.16,1.12,highlight_colors=[primary, secondary],
                highlight_weights=["bold"],string_weight="bold",fontsize=14,
                fontfamily=title_font,color=text_colour)
fig1.text(0.16,1.12,"English Premier League "+df.iloc[0,1],fontweight="regular",fontsize=14,
         color=text_colour, fontfamily=title_font)
# add logo
ax2=fig1.add_axes([0,1.05,0.2,0.2])
ax2.axis("off")
url = "https://logos-world.net/wp-content/uploads/2020/05/Arsenal-Logo.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
ax2.imshow(img)

#add credit
fig1.text(0, -0.025, "Created by Robbie Still / @datarobbie1. Data provided by WhoScored.com",
                       fontstyle="italic", fontsize=9, fontfamily=title_font, color=text_colour)

#plt.show()

plt.savefig(columnsNamesArr[1] + " and " + columnsNamesArr[2]+'.jpg', bbox_inches='tight', dpi=240)