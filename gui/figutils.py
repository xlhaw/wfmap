import matplotlib.pyplot as plt
import numpy as np
import io
#from PIL import Image


def fig2arr(fig):
    byte = io.BytesIO()
    fig.savefig(byte, format='png')
    byte.seek(0)
    bimg = io.BytesIO(byte.read())
    # np.asarray(bytearray(byte.read()),dtype=np.uint8)
    return plt.imread(bimg)  # np.array(Image.open(bimg))


def arr2fig(img_arr, figsize=None, save=True, fname=None):
    plt.close('all')
    plt.imshow(img_arr)
    plt.axis('off')
    fig = plt.gcf()
    if figsize:
        fig.set_size_inches(figsize)
    if save:
        fig.savefig(f'{fname}.jpg', dpi=200)
    return fig
# get|set_size_inches


def tight_arr(img_arr, padding=4):  # 3 channels
    r_channel = img_arr[:, :, 0]
    h, w = r_channel.shape
    x = np.argmin(r_channel, axis=0)
    y = np.argmin(r_channel, axis=1)

    left_margin = np.argmax(x > 0)  # white is all 255, max,min all the same
    right_margin = np.argmax(x[::-1] > 0)
    top_margin = np.argmax(y > 0)
    bot_margin = np.argmax(y[::-1] > 0)
    return img_arr[top_margin-padding:h-bot_margin+padding, left_margin-padding:w-right_margin+padding, :]


def fig_concat(figs, axis=1, title=None, fname=None, dpi=200):
    # TODO unify all figs' size referring to concat orientation
    # TODO trim the margin, latest
    plt.close('all')
    assert axis in [0, 1], 'Only by Row/0 and Col/1 Concat Supported!'
    qty = len(figs)
    w, h = figs[0].get_figwidth(), figs[0].get_figheight()
    #axis=1 if orient=='col' else 0
    w_ = w*qty if axis == 1 else w
    h_ = h*qty if axis == 0 else h
    # won't throw error if includes wrong size
    figa = np.concatenate([fig2arr(f) for f in figs], axis=axis)
    plt.imshow(figa)
    plt.axis('off')
    fig = plt.gcf()
    fig.set_size_inches(w_, h_)  # fig.set_figwidth(w) or fig.set_figheight(h)
    plt.title(title)  # this may also change the size and margin
    # 6,4 default, 18,4,plt.title did not change the figsize
    print(fig.get_figwidth(), fig.get_figheight())
    if fname:
        fig.savefig(f'{fname}.jpg', dpi=dpi)  # ppi
    else:
        return fig


def fig_concat2d(fig_list2d, fname=None, title=None):  # what about different aspect raio??
    plt.close('all')
    fig_r = [np.concatenate([fig2arr(f) for f in fig_list2d[row]], axis=1)
             for row in range(len(fig_list2d))]
    figall = np.concatenate(fig_r, axis=0)
    plt.imshow(figall)
    plt.axis('off')
    fig = plt.gcf()
    w, h = 0, 0
    for f in fig_list2d[0]:
        w += f.get_figwidth()
        h += f.get_figheight()
    fig.set_size_inches(w, h)
    if title:
        plt.suptitle(title)
    if fname:
        fig.savefig(f'{fname}.jpg', dpi=300)
    else:
        return fig


# need to make sure the size is the same
def figs2img(figs, axis=1, title=None, fname=None, dpi=200):
    assert axis in [0, 1], 'Only by Row/0 and Col/1 Concat Supported!'
    # won't throw error if includes wrong size
    figa = np.concatenate([fig2arr(f) for f in figs], axis=axis)
    figa = tight_arr(figa)  # Key
    if fname:
        plt.imsave(f'{fname}_i.jpg', figa, dpi=dpi)  # best practice!
    else:
        return figa
    # resize or interpolation?


def groupplot(data, pltfunc, groupby=[], items=[], *args, **kwargs):  # what about title scheme?
    # unless necessary, data processing should not include in pltfunc
    for k, df in data.groupby(groupby):
        figs = []
        for i in items:
            figs.append(pltfunc(df, i, title=f'{k} {i}', *args, **kwargs))
        fig_concat(figs, fname=f'{k}')
