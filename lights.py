import numpy as np
import scipy
from PIL import Image
from scipy import signal as sg

def max_filter(img):
    peaks = scipy.ndimage.maximum_filter(img, size=200)
    peaks = np.argwhere(peaks == img)
    peaks = list(filter(lambda l: img[l[0]][l[1]] > 200, peaks))
    x = [p[0] for p in peaks]
    y = [p[1] for p in peaks]
    #print(x)
    #print(peaks)
    return y,x

# def remove_dups(greee_list,red_list):
#     red = [list(r) for r in  ]
#     x_green = [x[0] for x in greee_list]
#     y_green = [y[0] for y in greee_list]
#     for index,r in enumerate(red_list):
#         if r[0] in x_green[index] and r[1] in y_green[index] :
#             greee_list.remove(r)
#     #         greee_list.remove(r)
#     return greee_list,red_list