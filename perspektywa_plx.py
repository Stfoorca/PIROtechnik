def hellothere(im, thresh):
    dst = cv2.cornerHarris(np.float32(thresh), 2, 3, 0.04)

    im = np.zeros((dst.shape[0], dst.shape[1]), dtype=np.uint8)
    im[dst != 0] = [255]
    cv2.medianBlur(im, 5)
    im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cntNumber = 0
    for j in contours:
        if len(j) >= 20:
            break
        else:
            cntNumber += 1
    cnt = contours[cntNumber]
    cv2.drawContours(im, [cnt], 0, (0,0,255), 10)
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    #cv2.drawContours(im, approx, -1, (255,255,0), 10)#seledynowe

    x,y,w,h = cv2.boundingRect(cnt)
    #cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)#zielone

    hull = cv2.convexHull(cnt)
    #print(hull)
    #cv2.drawContours(im, hull, -1, (0,255,255), 10)#zolte

    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    #cv2.drawContours(im,[box],0,(0,0,255),2)#czerwone

    # Apply edge detection method on the image





    coords = []


    for coordsHull in hull:
        # for i in range(20):
        if (coordsHull[0][0],coordsHull[0][1]) in cnt:
            coords.append(coordsHull)
            # elif (coordsHull[0][0]+i,coordsHull[0][1]) in cnt:
            #     coords.append(coordsHull)
            # elif (coordsHull[0][0]-i, coordsHull[0][1]) in cnt:
            #     coords.append(coordsHull)
            # elif (coordsHull[0][0], coordsHull[0][1]+i) in cnt:
            #     coords.append(coordsHull)
            # elif (coordsHull[0][0], coordsHull[0][1]-i) in cnt:
            #     coords.append(coordsHull)
            # elif (coordsHull[0][0]+i, coordsHull[0][1]+i) in cnt:
            #     coords.append(coordsHull)
            # elif (coordsHull[0][0]+i, coordsHull[0][1]-i) in cnt:
            #     coords.append(coordsHull)
            # elif (coordsHull[0][0]-i, coordsHull[0][1]+i) in cnt:
            #     coords.append(coordsHull)
            # elif (coordsHull[0][0]-i, coordsHull[0][1]-i) in cnt:
            #     coords.append(coordsHull)
    print(coordsHull)