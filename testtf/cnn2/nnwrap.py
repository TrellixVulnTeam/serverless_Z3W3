# Under development, will be takin g shots for calibration
import cv2
import numpy as np
import time
# from testtf.cnn2.new1cnn2a import DB1_infer
# from new4cnn2a import *
# from new1cnn2a import *

rwidth = 170
rheight = 170
fullwidth = 640 
fullheight = 480
IMAGECOUNT = 100

def sqdist(v1, v2):
    d = v1-v2
    return 1-d*d


def normalize_image(img):
    # Normalizes the input image to range (0, 1) for visualization
    img = img - np.min(img)
    img = img/np.max(img)
    return img



def nn_wrap(nom, denom):
    wrap = np.zeros((rheight, rwidth), dtype=np.float)
    im_wrap = np.zeros((rheight, rwidth), dtype=np.float)
 
    for i in range(rheight):
        for j in range(rwidth):
            wrap[i, j] = np.arctan2(nom[i, j], denom[i, j])
            if wrap[i, j] < 0:
                if nom[i, j] < 0:
                    wrap[i, j] += 2*np.pi
                else:
                    wrap[i, j] += 1 * np.pi
            im_wrap[i, j] = 128/np.pi * wrap[i, j]

    # wrap = cv2.GaussianBlur(wrap, (3, 3), 0)
    # im_wrap = cv2.GaussianBlur(im_wrap, (3, 3), 0)
    return(im_wrap)




def nn2_wrap(nom, denom):
    image = cv2.imread(nom)
    greynom = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.imread(denom)
    greydenom = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    wrap = np.zeros((rheight, rwidth), dtype=np.float)
    im_wrap = np.zeros((rheight, rwidth), dtype=np.float)
 
    for i in range(rheight):
        for j in range(rwidth):
            wrap[i, j] = np.arctan2(greynom[i, j], greydenom[i, j])
            if wrap[i, j] < 0:
                if nom[i, j] < 0:
                    wrap[i, j] += 2*np.pi
                else:
                    wrap[i, j] += 1 * np.pi
            im_wrap[i, j] = 128/np.pi * wrap[i, j]

    # wrap = cv2.GaussianBlur(wrap, (3, 3), 0)
    # im_wrap = cv2.GaussianBlur(im_wrap, (3, 3), 0)
    return(im_wrap)

def save4swat(i, nom, denom):
    folder = '/home/samir/serverless/new1/4/'
    np.save(folder+ 'nnnom/' + str(i) + '.npy', nom, allow_pickle=False)
    np.save(folder+ 'nndenom/' + str(i) + '.npy', denom, allow_pickle=False)

def save1swat(i, nom, denom):
    folder = '/home/samir/serverless/new1/1/'
    np.save(folder+ 'nnnom/' + str(i) + '.npy', nom, allow_pickle=False)
    np.save(folder+ 'nndenom/' + str(i) + '.npy', denom, allow_pickle=False)
    nom = normalize_image(nom)
    denom = normalize_image(denom)
    cv2.imwrite(folder+ 'nnnom/' + str(i) + '.png', 256/np.pi*nom)
    cv2.imwrite(folder+ 'nndenom/' + str(i) + '.png', 256/np.pi*denom)


def loadswat(i):
    folder ='/home/samir/serverless/' 
    nnnom = np.load(folder+ 'newnnnom/' + str(i) + '.npy')
    nndenom = np.load(folder+ 'newnndenom/' + str(i) + '.npy')
    return(nnnom, nndenom)

def testarctan(folder):
    nominator = folder + 'v22/b1nom.png'
    denominator = folder + 'v22/b1denom.png'
    test_im_wrap = nn2_wrap(nominator, denominator)
    png_file = folder + 'v22/npy_im_wrap.png'
    cv2.imwrite(png_file, test_im_wrap)


# folder = '/home/samir/serverless/testtf/data/' 
# testarctan(folder)


def nnfull_wrap(nom, denom):
    wrap = np.zeros((fullheight, fullwidth), dtype=np.float)
    im_wrap = np.zeros((fullheight, fullwidth), dtype=np.float)
    greynom = np.load(nom)
    greydenom = np.load(denom)
    for i in range(fullheight):
        for j in range(fullwidth):
            wrap[i, j] = np.arctan2(greynom[i, j], greydenom[i, j])
            if wrap[i, j] < 0:
                if greynom[i, j] < 0:
                    wrap[i, j] += 2*np.pi
                else:
                    wrap[i, j] += 1 * np.pi
            im_wrap[i, j] = 128/np.pi * wrap[i, j]

    # wrap = cv2.GaussianBlur(wrap, (3, 3), 0)
    # im_wrap = cv2.GaussianBlur(im_wrap, (3, 3), 0)
    return(wrap, im_wrap)

def nnswat_wrap(nom, denom):
    wrap = np.zeros((rheight, rwidth), dtype=np.float)
    im_wrap = np.zeros((rheight, rwidth), dtype=np.float)
    greynom = np.load(nom)
    greydenom = np.load(denom)
    for i in range(rheight):
        for j in range(rwidth):
            wrap[i, j] = np.arctan2(greynom[i, j], greydenom[i, j])
            if wrap[i, j] < 0:
                if greynom[i, j] < 0:
                    wrap[i, j] += 2*np.pi
                else:
                    wrap[i, j] += 1 * np.pi
            im_wrap[i, j] = 128/np.pi * wrap[i, j]

    # wrap = cv2.GaussianBlur(wrap, (3, 3), 0)
    # im_wrap = cv2.GaussianBlur(im_wrap, (3, 3), 0)
    return(wrap, im_wrap)

def save1nnwrap():
    for i in range(IMAGECOUNT):
        print('nnwrap1:', str(i))
        nnnom = '/home/samir/serverless/new1/1/' +'nnnom/' + str(i) +'.npy'
        nndenom = '/home/samir/serverless/new1/1/' +'nndenom/' + str(i) +'.npy'
        nnnpywrap, nnimwrap = nnswat_wrap(nnnom, nndenom)
        pngfile = '/home/samir/serverless/new1/1/' + 'nnwrap/' + str(i) + '.png'
        cv2.imwrite(pngfile, nnimwrap)
        npyfile ='/home/samir/serverless/new1/1/' + 'nnwrap/' + str(i) + '.npy'
        np.save( npyfile, nnnpywrap, allow_pickle=False)

        
def save4nnwrap():
    for i in range(IMAGECOUNT):
        print('nnwrap4:', str(i))
        nnnom = '/home/samir/serverless/new1/4/' +'nnnom/' + str(i) +'.npy'
        nndenom = '/home/samir/serverless/new1/4/' +'nndenom/' + str(i) +'.npy'
        nnnpywrap, nnimwrap = nnswat_wrap(nnnom, nndenom)
        pngfile = '/home/samir/serverless/new1/4/' + 'nnwrap/' + str(i) + '.png'
        cv2.imwrite(pngfile, nnimwrap)
        npyfile = '/home/samir/serverless/new1/4/' + 'nnwrap/' + str(i) + '.npy'
        np.save(npyfile, nnnpywrap, allow_pickle=False)


def save1wrap():
    for i in range(IMAGECOUNT):
        print('wrap1:', str(i))
        nom = '/home/samir/serverless/new1/1/' +'nom/' + str(i) +'.npy'
        denom = '/home/samir/serverless/new1/1/' +'denom/' + str(i) +'.npy'
        npywrap, imwrap = nnswat_wrap(nom, denom)
        pngfile = '/home/samir/serverless/new1/1/' + 'wrap/' + str(i) + '.png'
        cv2.imwrite(pngfile, imwrap)
        npyfile = '/home/samir/serverless/new1/1/' + 'wrap/' + str(i) + '.npy'
        np.save(npyfile, npywrap, allow_pickle=False)

def save4wrap():
    for i in range(IMAGECOUNT):
        print('wrap4:', str(i))
        nom = '/home/samir/serverless/' +'new1/4/nom/' + str(i) +'.npy'
        denom = '/home/samir/serverless/' +'new1/4/denom/' + str(i) +'.npy'
        npywrap, imwrap = nnswat_wrap(nom, denom)
        pngfile = '/home/samir/serverless/new1/4/' + 'wrap/' + str(i) + '.png'
        cv2.imwrite(pngfile, imwrap)
        npyfile = '/home/samir/serverless/new1/4/' + 'wrap/' + str(i) + '.npy'
        np.save(npyfile, npywrap, allow_pickle=False)


def testfullarctan(folder):
    nominator = folder + '1nom.npy'
    denominator = folder + '1denom.npy'
    test_im_wrap = nnfull_wrap(nominator, denominator)
    png_file = folder + 'npy_im_wrap.png'
    cv2.imwrite(png_file, test_im_wrap)

def testswatarctan(folder):
    nominator = folder + 'newnnnom/12.npy'
    denominator = folder + 'newnndenom/12.npy'
    test_im_wrap = nnswat_wrap(nominator, denominator)
    png_file = folder + 'npy_nn_im_wrap.png'
    cv2.imwrite(png_file, test_im_wrap)

# folder = '/home/samir/serverless/testtf/data/new_train/2scan_im_folder/' 
# testfullarctan(folder)
# greynom = np.load(folder + '1denom.npy')
# cv2.imwrite(folder + 'npy1denom.png',
#             (greynom).astype(np.uint8))
# greynom = np.load(folder + '1nom.npy')
# cv2.imwrite(folder + 'npy1nom.png',
#             (greynom).astype(np.uint8))

# folder = '/home/samir/serverless/' 
# testswatarctan(folder)
# greynom = np.load(folder + 'newnnnom/12.npy')
# greynom = 255.0*greynom
# cv2.imwrite(folder + 'npy0nom.png',
#             (greynom).astype(np.uint8))
# greynom = np.load(folder + 'newnndenom/12.npy')
# greynom = 255.0*greynom
# cv2.imwrite(folder + 'npy0denom.png',
#             (greynom).astype(np.uint8))

# save1nnwrap()
# save4nnwrap()
# save1wrap()
# save4wrap()

def infer():
    folder = '/home/samir/serverless/infer/scan_im_folder/'
    nom1, denom1 = DB1_infer(folder + 'image0.png', folder + 'image2.png')
    nom4, denom4 = DB4_infer(folder + 'image0.png', folder + 'image1.png')
    cv2.imwrite(folder+ 'nom1.png', 255*nom1)
    cv2.imwrite(folder+ 'denom1.png', 255*denom1)
    cv2.imwrite(folder+ 'nom4.png', 255*nom4)
    cv2.imwrite(folder+ 'denom4.png', 255*denom4)

