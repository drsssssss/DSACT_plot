from easydict import EasyDict as edict
import palettable as pltt
from palettable.colorbrewer.qualitative import Set1_9
colors = Set1_9.hex_colors

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i / inch for i in tupl[0])
    else:
        return tuple(i / inch for i in tupl)

# reformate to easydict

cfg = edict()

cfg.fig_size = cm2inch((7, 6))
cfg.smooth_alpha = 0.3
cfg.downsample = 1
cfg.dpi = 600
cfg.pad = 0.01
cfg.line_width = 1
cfg.tick_size = 6
cfg.bwidth = 0.35
cfg.blength = 2.5
cfg.tick_label_font = "Arial"
cfg.legend_font = {
    "family": "Arial",
    "size": "6",
    "weight": "normal",
}
cfg.label_font = {
    "family": "Arial",
    "size": "6",
    "weight": "normal",
}

cfg.color = colors
cfg.legend_loc = "lower right"
cfg.legend_ncol = 2
cfg.save_format = "png"
print(colors)


