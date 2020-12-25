from lights import max_filter



try:
    print("Elementary imports: ")
    import os
    import json
    import glob
    import argparse
    print("numpy/scipy imports:")
    import numpy as np
    from scipy import signal as sg
    import scipy.ndimage as ndimage
    from scipy.ndimage.filters import maximum_filter

    print("PIL imports:")
    from PIL import Image

    print("matplotlib imports:")
    import matplotlib.pyplot as plt
except ImportError:
    print("Need to fix the installation")
    raise

print("All imports okay. Yay!")


def find_tfl_lights(c_image: np.ndarray, **kwargs):
    kernel = np.ones((3, 3)) / 9
    kernel[1, 1] = 8 / 9
    # convolved = sg.convolve2d(c_image, kernel, "same")
    plt.imshow(c_image)
    # green_list = max_filter(sg.convolve2d(c_image[:, :, 0], kernel, "same"))
    # red_list = max_filter(sg.convolve2d(c_image[:, :, 1], kernel, "same"))
    # green_list,red_list = remove_dups(green_list,red_list)
    # x_red = [p[0] for p in red_list]
    # y_red = [p[1] for p in red_list]
    # x_green = [p[0] for p in red_list]
    # y_green = [p[1] for p in red_list]
    #
    x_red, y_red = max_filter(sg.convolve2d(c_image[:, :, 0], kernel, "same"))
    x_green, y_green = max_filter(sg.convolve2d(c_image[:, :, 1], kernel, "same"))
    return x_red, y_red, x_green, y_green
    #
    # """
    #x_blue, y_blue = max_filter(sg.convolve2d(c_image[:, :, 2], kernel, "same"))
    # Detect candidates for TFL lights. Use c_image, kwargs and you imagination to implement
    # :param c_image: The image itself as np.uint8, shape of (H, W, 3)
    # :param kwargs: Whatever config you want to pass in here
    # :return: 4-tuple of x_red, y_red, x_green, y_green
    # """
    # gray_image = cv2.cvtColor(c_image, cv2.COLOR_BGR2GRAY)/255.
    # c_image = c_image[:,:,0]
    # ker = plt.imread("C:/Users/RENT/Desktop/projects/mobileye/project/pic.png")
    # gray_ker = cv2.cvtColor(ker, cv2.COLOR_BGR2GRAY)
    # kernel = np.array([[-1/9,-1/9,-1/9],[-1/9,8/9,-1/9],[-1/9,-1/9,-1/9]])  # create first central finite difference kernel
    # pdx = sg.convolve2d(c_image, kernel, "same")
    # # print(pdx)
    # print("___________________________________________________")
    # res = scipy.ndimage.maximum_filter(pdx,size=10)
    # cor = c_image[res == pdx]
    # plt.imshow(cor)
    # plt.show()
    # print(cor)
    # max_filter(res)
    #
    #
    #
    # # print(res)
    # plt.imshow(pdx)
    # plt.show()
    # # x = np.arange(-100, 100, 20) + c_image.shape[1] / 2
    # # y_red = [c_image.shape[0] / 2 - 120] * len(x)
    # # y_green = [c_image.shape[0] / 2 - 100] * len(x)
    # # return x, y_red, x, y_green
    # return [],[],[],[]

def show_image_and_gt(image, objs, fig_num=None):
    # plt.imshow(image)
    # plt.show()
    labels = set()
    if objs is not None:
        for o in objs:
            poly = np.array(o['polygon'])[list(np.arange(len(o['polygon']))) + [0]]
            plt.plot(poly[:, 0], poly[:, 1], 'r', label=o['label'])
            labels.add(o['label'])
        if len(labels) > 1:
            plt.legend()


def test_find_tfl_lights(image_path, json_path=None, fig_num=None):
    """
    Run the attention code
    """
    image = np.array(Image.open(image_path))
    if json_path is None:
        objects = None
    else:
        gt_data = json.load(open(json_path))
        what = ['traffic light']
        objects = [o for o in gt_data['objects'] if o['label'] in what]

    show_image_and_gt(image, objects, fig_num)
    red_x, red_y, green_x, green_y = find_tfl_lights(image, some_threshold=42)
    plt.plot(red_x, red_y, 'ro', color='r', markersize=4)
    plt.plot(green_x, green_y, 'ro', color='g', markersize=4)


def main(argv=None):
    """It's nice to have a standalone tester for the algorithm.
    Consider looping over some images from here, so you can manually exmine the results
    Keep this functionality even after you have all system running, because you sometime want to debug/improve a module
    :param argv: In case you want to programmatically run this"""
    parser = argparse.ArgumentParser("Test TFL attention mechanism")
    parser.add_argument('-i', '--image', type=str, help='Path to an image')
    parser.add_argument("-j", "--json", type=str, help="Path to json GT for comparison")
    parser.add_argument('-d', '--dir', type=str, help='Directory to scan images in')
    args = parser.parse_args(argv)
    default_base = '../../data'
    if args.dir is None:
        args.dir = default_base
    flist = glob.glob(os.path.join(args.dir, '*_leftImg8bit.png'))
    for image in flist:
        json_fn = image.replace('_leftImg8bit.png', '_gtFine_polygons.json')
        if not os.path.exists(json_fn):
            json_fn = None
        test_find_tfl_lights(image, json_fn)
    if len(flist):
        print("You should now see some images, with the ground truth marked on them. Close all to quit.")
    else:
        print("Bad configuration?? Didn't find any picture to show")
    plt.show(block=True)


if __name__ == '__main__':
    main()
