#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: image.py
@time: 2023/7/12 16:57
"""
import ddddocr


def ocr(image_base64):
    # 解码base64图片数据
    # image_data = base64.b64decode(image_base64)
    #
    # # 将数据写入到图片文件
    # with open('../../static/imag.png', 'wb') as file:
    #     file.write(image_data)

    ocr = ddddocr.DdddOcr(show_ad=False)
    # ocr.use_import_onnx = True
    res = ocr.classification(image_base64)
    return res


if __name__ == '__main__':
    res = 'iVBORw0KGgoAAAANSUhEUgAAAGQAAAAeCAYAAADaW7vzAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAKISURBVGhD7Zg7bsMwDEB9np7EB/IBeoeuXnuEzO7SKWvQqYMRoFOAAh3aVSVdUlZkSZYjyWYKP4CAP0kg6ZmknEoFqKpqD0+Uotwv/xOeHx7oaB12ITPsQgSyppQIIZ1qrPpZtz3duxPODawqRAJrSQkL6VtVWzJ01K26Cy2DDJjma0cXbkOAkF61NS1+Y05mzJiryytTPUYk9yt8BmVgnNIfnzWk+GfVNf5M4HtbGgG8Uk71KILjTPcSKS3FMyOsVrU/C7iUlRTycqSDMBMpZlYcWjoHQV90PwMlpViziYNlBZs7SIMP+SNmY4BSMC507mGUAr95gGPdL+gcxWRElhDd6BvoJgFA2kSCDrjn8/FGEsyIwFm+vkAEZkpiQ3dRSopjFgG4d8CChh9wuFnfss38UeqbDi/vfzLePunCPBMpvMPK0NBdlJASLaRrUAREzHYXxCVvwThTZsqVzZUUbu6ZGrrNRkKMF8PYRQZ54Xo2B2TKEYWcxoxZgJYyNPS0F8I5cksJC4kuUSZgAvrLIAW+O0agb0yAMoXZcfyg8+UMUnindUfAiD1oGTPN24ab+dWXUBJKsa97uKF/TICG3hdq6CXxCOEytVBGCOwrKAR60Cw9lCoU0kPpuhVq6P2TZ4pCcY6W3zNCsbhn6/eSuZqe1j80xgshlq/JDkwojlEa/2F5Y0lPIWKFcLlKEgKDwxdCq6Hfg5T1Rsgly5lanBWuSMwUC+lSMo4OnkrIrGHRXWvOuy4BPVaylHwj4wxwlaRgdmyDVCkZRwWLjYtu76J4GyxIBiNRSuYRGWVLhyNjBCFNiqzRbIQkKbsQQoqUXYiBBCm7EIutpexCHGwpZRfiYRspSv0CnVQ8ipcNhD4AAAAASUVORK5CYII='
    print(ocr(res))
