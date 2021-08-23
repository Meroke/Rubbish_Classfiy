import cv2

image_path = '/home/meroke/图片/Pic/banana_half/Bh1.jpg'
image = cv2.imread(image_path)
col_row = image.shape
row = col_row[0]
col = col_row[1]

print(row,col)
x_start = int(row/2 - 60)
x_end = int(row/2 + 60)
y_start = int(col/2 - 60)
y_end = int(col/2 + 60)

img = image[130:340,190:500]
img = cv2.blur(img,(5,5))
img2 = img.copy()
cv2.imwrite('opencv_test.jpg',img)
img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) # 灰度处理
img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,3)
#img = cv2.threshold(img,160,255,cv2.THRESH_BINARY_INV)[1] # 二值化
cv2.imwrite('opencv_test_sec.jpg',img)
# cv2.imshow('tet',img)

contours,hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
cnt = cnts[0]
area = cv2.contourArea(cnt)
print(area)
res = cv2.drawContours(img2,[cnt],-1,(0,0,255),2)

# cv2.imshow('res',res)
cv2.imwrite('opencv-test_thr.jpg',res)
cv2.waitKey(0)
cv2.destroyAllWindows()
