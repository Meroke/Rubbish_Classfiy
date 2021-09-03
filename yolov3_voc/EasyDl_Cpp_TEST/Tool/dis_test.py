import cv2

img = cv2.imread("/home/ubuntu/Pictures/test/1068.jpg")
cv2.line(img,(264,105),(264,123),(0,255,0),3)
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()