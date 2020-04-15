import sys
import os
import cv2
import matplotlib.pyplot as plt
from scipy import ndimage
import numpy as np
from collections import defaultdict


def rotateImage(image):
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def cropImage(img):
    _, img_rotated = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img_rotated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntNumber = 0
    for j in contours:
        if len(j) >= 20:
            break
        else:
            cntNumber += 1
    cnt = contours[cntNumber]
    x, y, w, h = cv2.boundingRect(cnt)

    img_cropped = img_rotated[y:y + h, x:x + w].copy()
    return img_cropped


def resizeImage(img):
    img = cv2.resize(img, (30, 30))
    return img


def showStepImages(images):
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    ax1.imshow(images[0], cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    ax2 = fig.add_subplot(222)
    ax2.imshow(images[1], cmap='gray')
    plt.title('Rotated Image'), plt.xticks([]), plt.yticks([])
    ax3 = fig.add_subplot(223)
    ax3.imshow(images[2], cmap='gray')
    plt.title('Cropped Image'), plt.xticks([]), plt.yticks([])
    ax4 = fig.add_subplot(224)
    ax4.imshow(images[3], cmap='gray')
    plt.title('Final Image'), plt.xticks([]), plt.yticks([])


def fixRotation(image):
    mask = np.uint8(np.where(image >= 10, 1, 0))
    row_counts = cv2.reduce(mask, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32SC1)
    col_counts = cv2.reduce(mask, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32SC1)
    rows = row_counts.flatten().tolist()
    cols = col_counts.flatten().tolist()
    up = sum(rows[:5])
    down = sum(rows[-5:])
    left = sum(cols[:5])
    right = sum(cols[-5:])
    if (left > up and left > down) or (right > up and right > down):
        image = ndimage.rotate(image, 90)
    return image


def findSimilar(finalImages):
    whitePixelLists = defaultdict(list)

    for i, image in enumerate(finalImages):
        mask = np.uint8(np.where(image >= 10, 1, 0))

        col_counts = cv2.reduce(mask, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32SC1)
        whitePixelLists[i] = np.array(col_counts.flatten().tolist())

    pixelsStd = defaultdict(list)
    for i in range(len(whitePixelLists)):
        pixelStd = []
        for j in range(len(whitePixelLists)):
            if j != i:
                if (np.std(whitePixelLists[i] + whitePixelLists[j]) <= np.std(
                        whitePixelLists[i] + whitePixelLists[j][::-1])):
                    pixelStd.append((j, np.std(whitePixelLists[i] + whitePixelLists[j])))
                else:
                    pixelStd.append((j, np.std(whitePixelLists[i] + whitePixelLists[j][::-1])))
            else:
                pixelStd.append((j, 1000000))
        pixelsStd[i] = pixelStd
    toRet = ''
    for i in range(len(pixelsStd)):
        sortedPixelsStd = (sorted(pixelsStd[i], key=lambda x: x[1]))
        for j in sortedPixelsStd:
            toRet += str(j[0]) + ' '
        toRet += '\n'
    print(toRet)


def doMagic(directory, n, showImages):
    finalImages = []

    for i in range(0, n):
        try:
            path = os.path.normpath(directory + '/' + str(i) + '.png')
            img = cv2.imread(path, 0)
            img_rotated = rotateImage(img.copy())
            img_cropped = cropImage(img_rotated.copy())
            img_final = resizeImage(img_cropped.copy())
            img_final = fixRotation(img_final)
            if showImages:
                showStepImages([img, img_rotated, img_cropped, img_final])
            finalImages.append(img_final)
        except:
            print('Some error occured while processing image ', i)

    findSimilar(finalImages)


if __name__ == "__main__":
    directory = sys.argv[1]
    n = int(sys.argv[2])
    no_files = len([image for image in os.listdir(directory) if image.endswith('.png')])
    if n < 0:
        n = 0
        print('N musi byc wieksze lub rowne 0')
        pass
    elif n > no_files:
        print('Zbyt wysoka wartosc N, zmniejszona do ilosci obrazow w folderze')
        n = no_files
    doMagic(directory, n, True)
