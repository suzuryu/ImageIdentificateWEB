import numpy as np
import os
import sys

import cv2


def create_canny_img(gray_img_src):
    ave_square = (5, 5)
    # x軸方向の標準偏差
    sigma_x = 1

    # もしカラー画像だったら　グレースケール画像に変換する
    if type(gray_img_src[0][0]) == np.ndarray:
        gray_img_src = cv2.cvtColor(gray_img_src, cv2.COLOR_BGR2GRAY)
    can_img = cv2.Canny(gray_img_src, 100, 200)

    gau_img = cv2.GaussianBlur(gray_img_src, ave_square, sigma_x)
    gau_can_img = cv2.Canny(gau_img, 100, 200)

    med_img = cv2.medianBlur(gray_img_src, ksize=5)
    med_can_img = cv2.Canny(med_img, 100, 200)

    return can_img, gau_can_img, med_can_img


def get_color(img_src):
    same_colors = {}
    if type(img_src[0][0]) == np.ndarray:
        for row in img_src:
            for at in row:
                at = tuple(at)
                if at in same_colors:
                    same_colors[at] += 1
                else:
                    same_colors[at] = 0
    else:
        for row in img_src:
            for at in row:
                if at in same_colors:
                    same_colors[at] += 1
                else:
                    same_colors[at] = 0

    result = max(same_colors.values()) / len(img_src)

    return result


def cal_diff(mat, c_mat):
    sum_mat = 0
    for m in mat:
        for n in m:
            sum_mat += n
    sum_mat /= 255
    diff = mat - c_mat
    sum_diff = 0
    for d in diff:
        for n in d:
            sum_diff += n
    sum_diff /= 255
    result = sum_diff / sum_mat

    return result


def cal_score(gau_result, med_result, color_result):
    result1 = gau_result + med_result
    return ((1 / result1) * 0.8 + (color_result / 100) * 0.2) * 0.625

def resize_img(img_name):
    img_src = cv2.imread(img_name, cv2.IMREAD_UNCHANGED)

    if len(img_src) > 2000 or len(img_src[0]) > 2000:
        img_src = cv2.resize(img_src,(len(img_src) // 2, len(img_src[0]) // 2))

    return img_src


def identifies_img(img_name):
    img_src = resize_img(img_name)
    can_img, gau_can_img, med_can_img = create_canny_img(img_src)
    gau_result = cal_diff(can_img, gau_can_img)
    med_result = cal_diff(can_img, med_can_img)
    color_result = get_color(img_src)
    score = cal_score(gau_result, med_result, color_result)

    result = "score : {0} --> ".format(round(score, 3))
    if score >= 0.5:
        return result + "illust"
    else:
        return result + "picture"


if __name__ == "__main__":
    # FOR TEST
    argv = sys.argv
    if len(argv) != 2:
        print("argument error")
        sys.exit()

    img_name = argv[1]
    img_src = resize_img(img_name)
    result = identifies_img(img_src)
    print(result)
