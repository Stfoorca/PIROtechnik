def unwarp(img, src, dst, testing):
    h, w = img.shape[:2]
    # use cv2.getPerspectiveTransform() to get M, the transform matrix, and Minv, the inverse
    M = cv2.getPerspectiveTransform(src, dst)
    # use cv2.warpPerspective() to warp your image to a top-down view
    warped = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LINEAR)

    if testing:
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        f.subplots_adjust(hspace=.2, wspace=.05)
        ax1.imshow(img)
        x = [src[0][0], src[2][0], src[3][0], src[1][0], src[0][0]]
        y = [src[0][1], src[2][1], src[3][1], src[1][1], src[0][1]]
        ax1.plot(x, y, color='red', alpha=0.4, linewidth=3, solid_capstyle='round', zorder=2)
        ax1.set_ylim([h, 0])
        ax1.set_xlim([0, w])
        ax1.set_title('Original Image', fontsize=30)
        ax2.imshow(cv2.flip(warped, 1))
        ax2.set_title('Unwarped Image', fontsize=30)
        plt.show()
    else:
        return warped, M


def distance(pt1, pt2):
    (x1, y1), (x2, y2) = pt1, pt2
    dist = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    return dist


def fixPerspective(gray):
    bi = cv2.bilateralFilter(gray, 5, 75, 75)
    dst = cv2.cornerHarris(bi, 2, 3, 0.04)
    #--- create a black image to see where those corners occur ---
    mask = np.zeros_like(gray)

    #--- applying a threshold and turning those pixels above the threshold to white ---           
    mask[dst>0.01*dst.max()] = 255
    
    
    coor = np.argwhere(mask)
    coor_list = [l.tolist() for l in list(coor)]
    coor_tuples = [tuple(l) for l in coor_list]
    
    
    thresh = 50

    coor_tuples_copy = coor_tuples

    i = 1    
    for pt1 in coor_tuples:
        for pt2 in coor_tuples[i::1]:
            if(distance(pt1, pt2) < thresh):
                coor_tuples_copy.remove(pt2)      
        i+=1

    print(coor_tuples)
    #plt.imshow(mask)
    w, h = gray.shape[0], gray.shape[1]
    src = np.float32([
        (coor_tuples[3][1], coor_tuples[3][0]),
        (coor_tuples[1][1], coor_tuples[1][0]),
        (coor_tuples[2][1], coor_tuples[2][0]),
        (coor_tuples[0][1], coor_tuples[0][0])
    ])
    
    dst = np.float32([
        (h, 0),
        (0, 0),
        (h, w),
        (0, w)
    ])
    unwarp(gray, src, dst, True)