import cv2

dataset = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

s_img = cv2.imread("mask_1.png",-1)
capture = cv2.VideoCapture(0)

while True:
    ret, l_img = capture.read()
    gray = cv2.cvtColor(l_img, cv2.COLOR_BGR2GRAY)
    faces = dataset.detectMultiScale(gray, 1.2)
    if len(faces) > 0:
        # For Cap
        x_offset = faces[0][0] - 15
        y_offset = faces[0][1]

        # For Mask
        #x_offset = faces[0][0]
        #y_offset = faces[0][1]

        y1, y2 = y_offset, y_offset + s_img.shape[0]
        x1, x2 = x_offset, x_offset + s_img.shape[1]

        alpha_s = s_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] + alpha_l * l_img[y1:y2, x1:x2, c])

        cv2.imshow('result',l_img)
    if cv2.waitKey(1) == 27:
        break

capture.release()
cv2.destroyAllWindows()
