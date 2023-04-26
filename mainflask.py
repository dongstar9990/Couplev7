import base64
import json
import shutil
import string
from builtins import print, property, reversed, range, list
from calendar import prcal
from io import BytesIO
from os import link
from random import random

import mysql.connector
import requests
from PIL import Image
from PIL._imagingmath import mul_I
from _dlib_pybind11 import points
import pymysql
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import cv2
import argparse

from nacl.utils import random
from numpy.core.defchararray import index
from tqdm import tqdm
from flask_cors import CORS
from yaml import load
from datetime import datetime
from face_detection import select_face, select_all_faces
from face_swap import face_swap
import random

app = Flask(__name__)
cors = CORS(app)


def download_image(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        # print(response.raw ,"****")
    del response


def upload_image_to_imgbb(image_path, api_key):
    # Tải dữ liệu ảnh
    with open(image_path, "rb") as file:
        payload = {
            "key": api_key,
            "image": base64.b64encode(file.read()),
        }

    # Gửi yêu cầu POST tải lên ảnh đến API của ImgBB
    response = requests.post("https://api.imgbb.com/1/upload", payload)

    # Trích xuất đường dẫn trực tiếp đến ảnh từ JSON response
    json_data = json.loads(response.text)
    direct_link = json_data["data"]["url"]

    # Trả về đường dẫn trực tiếp đến ảnh
    return direct_link


@app.route('/home', methods=['GET', 'POST'])
def index():
    loaded = {}
    choose_case=0
    link_full1 = request.headers.get('Link_img1')
    link_full2 = request.headers.get('Link_img2')
    # link_full3 = request.headers.get('Link_img3')
    # link_full4 = request.headers.get('Link_img4')
    # khởi tạo thanh tiến trình
    progress_bar = tqdm(total=55, unit="records")
    if (link_full1[0:19] == 'https://github.com/'):
        link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
        if "blob/" in link_full1:
            link_full1 = link_full1.replace("blob/", '')
        if "/main" in link_full1:
            link_full1 = link_full1.replace("/raw/", "/")
    progress_bar.update(1)
    # print("process1 ",progress_bar)
    loaded["loaddata1"] = f'{progress_bar}'
    if (link_full2[0:19] == 'https://github.com/'):
        link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
        if "blob/" in link_full2:
            link_full2 = link_full2.replace("blob/", '')
        if "/main" in link_full2:
            link_full2 = link_full2.replace("/raw/", "/")
    progress_bar.update(2)
    loaded["loaddata2"] = f'{progress_bar}'
    # if (link_full3[0:19] == 'https://github.com/'):
    #     link_full3 = link_full3.replace("github.com/", "raw.githubusercontent.com/")
    #     if "blob/" in link_full3:
    #         link_full3 = link_full3.replace("blob/", '')
    #     if "/main" in link_full3:
    #         link_full3 = link_full3.replace("/raw/", "/")
    # progress_bar.update(3)
    # loaded["loaddata3"] = f'{progress_bar}'
    # if (link_full4[0:19] == 'https://github.com/'):
    #     link_full4 = link_full4.replace("github.com/", "raw.githubusercontent.com/")
    #     if "blob/" in link_full4:
    #         link_full4 = link_full4.replace("blob/", '')
    #     if "/main" in link_full4:
    #         link_full4 = link_full4.replace("/raw/", "/")

    progress_bar.update(4)
    loaded["loaddata4"] = f'{progress_bar}'
    filename1 = 'imgs/anhtam1.jpg'
    filename2 = 'imgs/anhtam2.jpg'
    filename3 = 'imgs/anhtam3.jpg'
    filename4 = 'imgs/anhtam4.jpg'
    download_image(link_full1, filename1)
    download_image(link_full2, filename2)
    # download_image(link_full3, filename3)
    # download_image(link_full4, filename4)

    config = {
        'user': 'root',
        'password': 'BAdong14102001!',
        'host': 'localhost',
        'port': 3306,
        'database': 'swapcouple'
    }

    def make_counter(start, step):
        count = start

        def counter():
            nonlocal count
            result = count
            count += step
            return result

        return counter

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor  = connection.cursor()
        mycursor1 = connection.cursor()
        # mycursor1.execute("Select * from skhanhphuc")
        # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
        # print('maek', make_counter(8, 1))
        # date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        # val = (link_full1, link_full2, link_full3, link_full4 )
        # sql = f"INSERT INTO dataset2(id,img_husband, img_wife, img_root1, img_root2,update_time) VALUES     {val}"

        # mycursor.execute(sql, val)
        random_sukien =['skhanhphuc','skchiatay','skkethon','sklyhon','skmuasam', 'sknym']
        random_sk=random.choice(random_sukien)
        print(random_sk)
        index_sk = random.randint(1,12)

        # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
        mycursor.execute(f"SELECT thongtin FROM skkethon where id=2")
        result2 = mycursor.fetchall()
        print('result2', result2[0])
        my_string = ', '.join(result2[0])
        print('mystring', my_string)

        mycursor.execute(f"SELECT image FROM skkethon where id=2")
        result5 = mycursor.fetchall()
        print('result5', result5[0])
        my_string12 = ', '.join(result5[0])
        print('mystring', my_string12)

        mycursor.execute(f"SELECT vtrinam FROM skkethon where id=2")
        result6 = mycursor.fetchall()
        print('result6', result6[0])
        my_string13 = ', '.join(result6[0])
        print('mystring', my_string13)


        mycursor.execute(f"SELECT nam FROM skkethon where id=2")
        result3 = mycursor.fetchall()
        print('result3', result3[0])
        print("***")
        my_string1 = ', '.join(result3[0])
        print('mystring', my_string1)

        mycursor.execute(f"SELECT nu FROM skkethon where id=2")
        result4 = mycursor.fetchall()
        print('result4', result4[0])
        print("***")
        my_string2 = ', '.join(result4[0])
        print('mystring', my_string2)
        if my_string1=="0" and my_string2=="0":
            choose_case=4
            download_image(my_string12 , "results/output.jpg")
        elif my_string1=="0":
            choose_case=1
            download_image(my_string2, filename4)
        elif my_string2=="0":
            choose_case=2
            download_image(my_string1, filename3)

        else:
            choose_case=3
            download_image(my_string1, filename3)
            download_image(my_string2, filename4)
        print("choose_Case ",choose_case)


        loaded["thongtin"]=my_string
        sql = "INSERT INTO datademo (img_husband ,img_wife , img_root1 ,img_root2 , thongtin_sk) VALUES (%s, %s , %s ,%s ,%s )"
        val = (link_full1, link_full2, my_string1, my_string2 , my_string)
        mycursor.execute(sql, val)
        result1 = mycursor.fetchall()

        # Lưu các thay đổi vào database
        connection.commit()
        # mycursor.execute("SELECT thongtin from skhanhphuc")
        print(mycursor.rowcount, "record inserted.")
        # mycursor1.execute("Select thongtin from skhanhphuc")x
        # connection.commit()

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    # mycursor = connection.cursor()
    # # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
    # sql = "INSERT INTO swapcouple (id, img_husband ,img_wife , img_root1 ,img_root2) VALUES (%s, %s , %s ,%s ,%s)"
    # val = (1, link_full1 , link_full2 ,link_full3 ,link_full4)
    # mycursor.execute(sql, val)
    # # Lưu các thay đổi vào database
    # connection.commit()
    #
    # print(mycursor.rowcount, "record inserted.")

    # print("https://github.com/ngahuynh1/ctanh/blob/main/wi6.jpg")
    # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
    # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
    # print("download thanh cong")
    # download_image(link_full3 , filename3)
    # rescale image

    # img_scale = Image.open("imgs/anhtam1.jpg")
    # print("hihia")
    # img_scale = Image.open(BytesIO(response.content))

    # new_image = img_scale.resize((500, 700))
    # new_image.save('imgs/example_resized1.jpg')
    #
    #
    # img_scale1 = Image.open("imgs/anhtam2.jpg")
    # new_image1 = img_scale1.resize((500, 700))
    # new_image1.save('imgs/example_resized2.jpg')
    progress_bar.update(5)
    loaded["loaddata5"] = f'{progress_bar}'
    # return f"{progress_bar}"
    # # Get the uploaded files
    # src_file = request.files['src']

    # dst_file = request.files['dst']
    # from_file=request.files['from']
    # my_list=[src_file , dst_file]
    # val=random.choice(my_list)
    # print(val)
    # Save the uploaded files to disk
    # src_path =  'imgs/src_img1.jpg'
    # dst_path =  'imgs/src_img2.jpg'
    # from_path=  'imgs/couple.jpg'
    # val.save(src_path)
    # src_file.save(src_path)
    # dst_file.save(dst_path)
    # from_file.save(from_path)

    # open image
    # index=0
    # img = Image.open("imgs/anhtam3.jpg")
    # # new_image = img.resize((500, 500))
    # # new_image.save('example_resized.jpg')
    # # lấy kích thước ảnh
    # width, height = img.size
    #
    # # cắt lấy nửa ảnh đầu trên
    # img_cropped1 = img.crop((0, 0, width//2 -40, height))
    # # lưu ảnh đã cắt
    # img_cropped1.save("imgs/img_1.jpg")
    # # cắt lấy nửa ảnh đầu trên
    # img_cropped2 = img.crop((width//2-40, 0, width, height))
    # # lưu ảnh đã cắt
    # img_cropped2.save("imgs/img_2.jpg")
    print("choose case" ,choose_case)
    if choose_case==1:

        # Swap faces
        args = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output1.jpg', warp_2d=False,
                                  correct_color=False, no_debug_window=True)
        src_img = cv2.imread(args.src)
        dst_img = cv2.imread(args.dst)
        src_points, src_shape, src_face = select_face(src_img)
        dst_faceBoxes = select_all_faces(dst_img)
        #
        # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False,
        #                            correct_color=False, no_debug_window=True)
        # src_img2 = cv2.imread(args1.src)
        # dst_img2 = cv2.imread(args1.dst)
        # src_points2, src_shape2, src_face2 = select_face(src_img2)
        # dst_faceBoxes2 = select_all_faces(dst_img2)
        # progress_bar.update(6)
        progress_bar.update(6)
        loaded["loaddata6"] = f'{progress_bar}'
        print("process6 ", progress_bar)
        if dst_faceBoxes is None:
            print('Detect 0 Face !!!')
        output = dst_img

        # if dst_faceBoxes2 is None:
        #     print('Detect 0 Face !!!')
        #     exit(-1)
        # output2 = dst_img2
        progress_bar.update(7)
        loaded["loaddata7"] = f'{progress_bar}'
        print("process7 ", progress_bar)
        for k, dst_face in dst_faceBoxes.items():
            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"], output, args)
        output_path = 'results/output1.jpg'
        cv2.imwrite(output_path, output)

        # for k, dst_face2 in dst_faceBoxes2.items():
        #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2,
        #                         args1)
        # output_path2 = 'results/output2.jpg'
        # cv2.imwrite(output_path2, output2)
        progress_bar.update(8)
        loaded["loaddata8"] = f'{progress_bar}'
        # print("thanh cong ")
        # image = cv2.imread('results/output1.jpg')
        # # print()
        # image1 = Image.open('results/output1.jpg')
        # image2 = Image.open('results/output2.jpg')
        # image_1 = cv2.imread('results/output1.jpg')
        # image_2 = cv2.imread('results/output2.jpg')
        #
        # progress_bar.update(9)
        # width1, height1 = image1.size
        # width2, height2 = image2.size
        # max_width = max(width1, width2)
        # max_height = max(height1, height2)
        # new_image = Image.new('RGB', (max_width * 2, max_height))
        # new_image.paste(image1, (0, 0))
        # # chuyen anh dau vao vi tri (max_width,0)
        # new_image.paste(image2, (max_width, 0))
        # new_image.save('results/output.jpg')
        # image_1 = cv2.imread('results/output1.jpg')
        # image_2 = cv2.imread('results/output2.jpg')
        progress_bar.update(9)
        loaded["loaddata9"] = f'{progress_bar}'
        # print("image1",image_1.shape)
        # print("image2",image_2.shape)

        # ghép hai ảnh lại với nhau theo chiều ngang
        # combined_img = cv2.hconcat([image_1, image_2])
        # result_img = 'results/output.jpg'
        # hiển thị ảnh đã ghép
        # cv2.imshow('Combined Image', combined_img)
        # cv2.imwrite(result_img, new_image)
        # Return the output image
        # return send_file(result_img, mimetype='image/jpeg')
        api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
        direct_link = upload_image_to_imgbb(output_path, api_key)
        # loaded.append(direct_link)
        loaded["Link_img"] = direct_link
        progress_bar.update(10)
        loaded["loaddata91=finish"] = f'{progress_bar}'
        # print("process10 ", progress_bar)
        progress_bar.close()
        return loaded
    if choose_case==2:

        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                  warp_2d=False,
                                  correct_color=False, no_debug_window=True)
        src_img = cv2.imread(args.src)
        dst_img = cv2.imread(args.dst)
        src_points, src_shape, src_face = select_face(src_img)
        dst_faceBoxes = select_all_faces(dst_img)
        #
        # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False,
        #                            correct_color=False, no_debug_window=True)
        # src_img2 = cv2.imread(args1.src)
        # dst_img2 = cv2.imread(args1.dst)
        # src_points2, src_shape2, src_face2 = select_face(src_img2)
        # dst_faceBoxes2 = select_all_faces(dst_img2)
        # progress_bar.update(6)
        progress_bar.update(6)
        loaded["loaddata6"] = f'{progress_bar}'
        print("process6 ", progress_bar)
        if dst_faceBoxes is None:
            print('Detect 0 Face !!!')
        output = dst_img

        # if dst_faceBoxes2 is None:
        #     print('Detect 0 Face !!!')
        #     exit(-1)
        # output2 = dst_img2
        progress_bar.update(7)
        loaded["loaddata7"] = f'{progress_bar}'
        print("process7 ", progress_bar)
        for k, dst_face in dst_faceBoxes.items():
            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"], output,
                               args)
        output_path = 'results/output1.jpg'
        cv2.imwrite(output_path, output)

        # for k, dst_face2 in dst_faceBoxes2.items():
        #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2,
        #                         args1)
        # output_path2 = 'results/output2.jpg'
        # cv2.imwrite(output_path2, output2)
        progress_bar.update(8)
        loaded["loaddata8"] = f'{progress_bar}'
        # print("thanh cong ")
        # image = cv2.imread('results/output1.jpg')
        # # print()
        # image1 = Image.open('results/output1.jpg')
        # image2 = Image.open('results/output2.jpg')
        # image_1 = cv2.imread('results/output1.jpg')
        # image_2 = cv2.imread('results/output2.jpg')
        #
        # progress_bar.update(9)
        # width1, height1 = image1.size
        # width2, height2 = image2.size
        # max_width = max(width1, width2)
        # max_height = max(height1, height2)
        # new_image = Image.new('RGB', (max_width * 2, max_height))
        # new_image.paste(image1, (0, 0))
        # # chuyen anh dau vao vi tri (max_width,0)
        # new_image.paste(image2, (max_width, 0))
        # new_image.save('results/output.jpg')
        # image_1 = cv2.imread('results/output1.jpg')
        # image_2 = cv2.imread('results/output2.jpg')
        progress_bar.update(9)
        loaded["loaddata9"] = f'{progress_bar}'
        # print("image1",image_1.shape)
        # print("image2",image_2.shape)

        # ghép hai ảnh lại với nhau theo chiều ngang
        # combined_img = cv2.hconcat([image_1, image_2])
        # result_img = 'results/output.jpg'
        # hiển thị ảnh đã ghép
        # cv2.imshow('Combined Image', combined_img)
        # cv2.imwrite(result_img, new_image)
        # Return the output image
        # return send_file(result_img, mimetype='image/jpeg')
        api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
        direct_link = upload_image_to_imgbb(output_path, api_key)
        # loaded.append(direct_link)
        loaded["Link_img"] = direct_link
        progress_bar.update(10)
        loaded["loaddata91=finish"] = f'{progress_bar}'
        # print("process10 ", progress_bar)
        progress_bar.close()
        return loaded
    if choose_case==3:
        if my_string13=="namsau":
            # Swap faces
            args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                      warp_2d=False,
                                      correct_color=False, no_debug_window=True)
            src_img = cv2.imread(args.src)
            dst_img = cv2.imread(args.dst)
            src_points, src_shape, src_face = select_face(src_img)
            dst_faceBoxes = select_all_faces(dst_img)

            args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg',
                                       warp_2d=False,
                                       correct_color=False, no_debug_window=True)
            src_img2 = cv2.imread(args1.src)
            dst_img2 = cv2.imread(args1.dst)
            src_points2, src_shape2, src_face2 = select_face(src_img2)
            dst_faceBoxes2 = select_all_faces(dst_img2)
            # progress_bar.update(6)
            progress_bar.update(6)
            loaded["loaddata6"] = f'{progress_bar}'
            print("process6 ", progress_bar)
            if dst_faceBoxes is None:
                print('Detect 0 Face !!!')
            output = dst_img

            if dst_faceBoxes2 is None:
                print('Detect 0 Face !!!')
                exit(-1)
            output2 = dst_img2
            progress_bar.update(7)
            loaded["loaddata7"] = f'{progress_bar}'
            print("process7 ", progress_bar)
            for k, dst_face in dst_faceBoxes.items():
                output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"], output,args)
            output_path = 'results/output1.jpg'
            cv2.imwrite(output_path, output)

            for k, dst_face2 in dst_faceBoxes2.items():
                output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"],
                                    output2,
                                    args1)
            output_path2 = 'results/output2.jpg'
            cv2.imwrite(output_path2, output2)
            progress_bar.update(8)
            loaded["loaddata8"] = f'{progress_bar}'
            # print("thanh cong ")
            # image = cv2.imread('results/output1.jpg')
            # print()
            image1 = Image.open('results/output1.jpg')
            image2 = Image.open('results/output2.jpg')

            image_1 = cv2.imread('results/output1.jpg')
            image_2 = cv2.imread('results/output2.jpg')

            progress_bar.update(9)
            width1, height1 = image1.size
            width2, height2 = image2.size
            max_width = max(width1, width2)
            max_height = max(height1, height2)
            new_image = Image.new('RGB', (max_width * 2, max_height))
            new_image.paste(image2, (0, 0))
            # chuyen anh dau vao vi tri (max_width,0)
            new_image.paste(image1, (max_width, 0))
            new_image.save('results/output.jpg')
            # image_1 = cv2.imread('results/output1.jpg')
            # image_2 = cv2.imread('results/output2.jpg')
            progress_bar.update(9)
            loaded["loaddata9"] = f'{progress_bar}'
            # print("image1",image_1.shape)
            # print("image2",image_2.shape)

            # ghép hai ảnh lại với nhau theo chiều ngang
            # combined_img = cv2.hconcat([image_1, image_2])
            result_img = 'results/output.jpg'
            # hiển thị ảnh đã ghép
            # cv2.imshow('Combined Image', combined_img)
            # cv2.imwrite(result_img, new_image)
            # Return the output image
            # return send_file(result_img, mimetype='image/jpeg')
            api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
            direct_link = upload_image_to_imgbb(result_img, api_key)
            # loaded.append(direct_link)
            loaded["Link_img"] = direct_link
            progress_bar.update(10)
            loaded["loaddata91=finish"] = f'{progress_bar}'
            # print("process10 ", progress_bar)
            progress_bar.close()
            return loaded
        else:
            # Swap faces
            args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                      warp_2d=False,
                                      correct_color=False, no_debug_window=True)
            src_img = cv2.imread(args.src)
            dst_img = cv2.imread(args.dst)
            src_points, src_shape, src_face = select_face(src_img)
            dst_faceBoxes = select_all_faces(dst_img)

            args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg',
                                       warp_2d=False,
                                       correct_color=False, no_debug_window=True)
            src_img2 = cv2.imread(args1.src)
            dst_img2 = cv2.imread(args1.dst)
            src_points2, src_shape2, src_face2 = select_face(src_img2)
            dst_faceBoxes2 = select_all_faces(dst_img2)
            # progress_bar.update(6)
            progress_bar.update(6)
            loaded["loaddata6"] = f'{progress_bar}'
            print("process6 ", progress_bar)
            if dst_faceBoxes is None:
                print('Detect 0 Face !!!')
            output = dst_img

            if dst_faceBoxes2 is None:
                print('Detect 0 Face !!!')
                exit(-1)
            output2 = dst_img2
            progress_bar.update(7)
            loaded["loaddata7"] = f'{progress_bar}'
            print("process7 ", progress_bar)
            for k, dst_face in dst_faceBoxes.items():
                output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"],
                                   output, args)
            output_path = 'results/output1.jpg'
            cv2.imwrite(output_path, output)

            for k, dst_face2 in dst_faceBoxes2.items():
                output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"],
                                    output2,
                                    args1)
            output_path2 = 'results/output2.jpg'
            cv2.imwrite(output_path2, output2)
            progress_bar.update(8)
            loaded["loaddata8"] = f'{progress_bar}'
            # print("thanh cong ")
            # image = cv2.imread('results/output1.jpg')
            # print()
            image1 = Image.open('results/output1.jpg')
            image2 = Image.open('results/output2.jpg')

            image_1 = cv2.imread('results/output1.jpg')
            image_2 = cv2.imread('results/output2.jpg')

            progress_bar.update(9)
            width1, height1 = image1.size
            width2, height2 = image2.size
            max_width = max(width1, width2)
            max_height = max(height1, height2)
            new_image = Image.new('RGB', (max_width * 2, max_height))
            new_image.paste(image1, (0, 0))
            # chuyen anh dau vao vi tri (max_width,0)
            new_image.paste(image2, (max_width, 0))
            new_image.save('results/output.jpg')
            # image_1 = cv2.imread('results/output1.jpg')
            # image_2 = cv2.imread('results/output2.jpg')
            progress_bar.update(9)
            loaded["loaddata9"] = f'{progress_bar}'
            # print("image1",image_1.shape)
            # print("image2",image_2.shape)

            # ghép hai ảnh lại với nhau theo chiều ngang
            # combined_img = cv2.hconcat([image_1, image_2])
            result_img = 'results/output.jpg'
            # hiển thị ảnh đã ghép
            # cv2.imshow('Combined Image', combined_img)
            # cv2.imwrite(result_img, new_image)
            # Return the output image
            # return send_file(result_img, mimetype='image/jpeg')
            api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
            direct_link = upload_image_to_imgbb(result_img, api_key)
            # loaded.append(direct_link)
            loaded["Link_img"] = direct_link
            progress_bar.update(10)
            loaded["loaddata91=finish"] = f'{progress_bar}'
            # print("process10 ", progress_bar)
            progress_bar.close()
            return loaded
    if choose_case==4:
        # Swap faces
        # args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
        #                           warp_2d=False,
        #                           correct_color=False, no_debug_window=True)
        # src_img = cv2.imread(args.src)
        # dst_img = cv2.imread(args.dst)
        # src_points, src_shape, src_face = select_face(src_img)
        # dst_faceBoxes = select_all_faces(dst_img)
        #
        # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg',
        #                            warp_2d=False,
        #                            correct_color=False, no_debug_window=True)
        # src_img2 = cv2.imread(args1.src)
        # dst_img2 = cv2.imread(args1.dst)
        # src_points2, src_shape2, src_face2 = select_face(src_img2)
        # dst_faceBoxes2 = select_all_faces(dst_img2)
        # # progress_bar.update(6)
        progress_bar.update(6)
        loaded["loaddata6"] = f'{progress_bar}'
        # print("process6 ", progress_bar)
        # if dst_faceBoxes is None:
        #     print('Detect 0 Face !!!')
        # output = dst_img
        #
        # if dst_faceBoxes2 is None:
        #     print('Detect 0 Face !!!')
        #     exit(-1)
        # output2 = dst_img2
        # progress_bar.update(7)
        loaded["loaddata7"] = f'{progress_bar}'
        print("process7 ", progress_bar)
        # for k, dst_face in dst_faceBoxes.items():
        #     output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"], output,
        #                        args)
        # output_path = 'results/output1.jpg'
        # cv2.imwrite(output_path, output)
        #
        # for k, dst_face2 in dst_faceBoxes2.items():
        #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"],
        #                         output2,
        #                         args1)
        # output_path2 = 'results/output2.jpg'
        # cv2.imwrite(output_path2, output2)
        progress_bar.update(8)
        loaded["loaddata8"] = f'{progress_bar}'
        # # print("thanh cong ")
        # # image = cv2.imread('results/output1.jpg')
        # # print()
        # image1 = Image.open('results/output1.jpg')
        # image2 = Image.open('results/output2.jpg')
        # image_1 = cv2.imread('results/output1.jpg')
        # image_2 = cv2.imread('results/output2.jpg')
        #
        # progress_bar.update(9)
        # width1, height1 = image1.size
        # width2, height2 = image2.size
        # max_width = max(width1, width2)
        # max_height = max(height1, height2)
        # new_image = Image.new('RGB', (max_width * 2, max_height))
        # new_image.paste(image1, (0, 0))
        # # chuyen anh dau vao vi tri (max_width,0)
        # new_image.paste(image2, (max_width, 0))
        # new_image.save('results/output.jpg')
        # image_1 = cv2.imread('results/output1.jpg')
        # image_2 = cv2.imread('results/output2.jpg')
        progress_bar.update(9)
        loaded["loaddata9"] = f'{progress_bar}'
        # print("image1",image_1.shape)
        # print("image2",image_2.shape)

        # ghép hai ảnh lại với nhau theo chiều ngang
        # combined_img = cv2.hconcat([image_1, image_2])
        result_img = 'results/output.jpg'
        # hiển thị ảnh đã ghép
        # cv2.imshow('Combined Image', combined_img)
        # cv2.imwrite(result_img, new_image)
        # Return the output image
        # return send_file(result_img, mimetype='image/jpeg')
        api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
        direct_link = upload_image_to_imgbb(result_img, api_key)
        # loaded.append(direct_link)
        loaded["Link_img"] = direct_link
        progress_bar.update(10)
        loaded["loaddata91=finish"] = f'{progress_bar}'
        # print("process10 ", progress_bar)
        progress_bar.close()
        return loaded

@app.route('/homev1', methods=['GET', 'POST'])
def index1():
    loaded = {}
    link_full1 = request.headers.get('Link_img1')
    link_full2 = request.headers.get('Link_img2')
    # link_full3 = request.headers.get('Link_img3')
    # link_full4 = request.headers.get('Link_img4')
    # khởi tạo thanh tiến trình
    progress_bar = tqdm(total=55, unit="records")
    if (link_full1[0:19] == 'https://github.com/'):
        link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
        if "blob/" in link_full1:
            link_full1 = link_full1.replace("blob/", '')
        if "/main" in link_full1:
            link_full1 = link_full1.replace("/raw/", "/")
    progress_bar.update(1)
    # print("process1 ",progress_bar)
    loaded["loaddata1"] = f'{progress_bar}'
    if (link_full2[0:19] == 'https://github.com/'):
        link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
        if "blob/" in link_full2:
            link_full2 = link_full2.replace("blob/", '')
        if "/main" in link_full2:
            link_full2 = link_full2.replace("/raw/", "/")
    progress_bar.update(2)
    loaded["loaddata2"] = f'{progress_bar}'
    # if (link_full3[0:19] == 'https://github.com/'):
    #     link_full3 = link_full3.replace("github.com/", "raw.githubusercontent.com/")
    #     if "blob/" in link_full3:
    #         link_full3 = link_full3.replace("blob/", '')
    #     if "/main" in link_full3:
    #         link_full3 = link_full3.replace("/raw/", "/")
    # progress_bar.update(3)
    # loaded["loaddata3"] = f'{progress_bar}'
    # if (link_full4[0:19] == 'https://github.com/'):
    #     link_full4 = link_full4.replace("github.com/", "raw.githubusercontent.com/")
    #     if "blob/" in link_full4:
    #         link_full4 = link_full4.replace("blob/", '')
    #     if "/main" in link_full4:
    #         link_full4 = link_full4.replace("/raw/", "/")

    progress_bar.update(4)
    loaded["loaddata4"] = f'{progress_bar}'
    filename1 = 'imgs/anhtam1.jpg'
    filename2 = 'imgs/anhtam2.jpg'
    filename3 = 'imgs/anhtam3.jpg'
    filename4 = 'imgs/anhtam4.jpg'
    download_image(link_full1, filename1)
    download_image(link_full2, filename2)
    # download_image(link_full3, filename3)
    # download_image(link_full4, filename4)
    # print("https://github.com/ngahuynh1/ctanh/blob/main/wi6.jpg")
    # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
    # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
    # print("download thanh cong")
    # download_image(link_full3 , filename3)
    # rescale image

    # img_scale = Image.open("imgs/anhtam1.jpg")
    # print("hihia")
    # img_scale = Image.open(BytesIO(response.content))

    # new_image = img_scale.resize((500, 700))
    # new_image.save('imgs/example_resized1.jpg')
    #
    #
    # img_scale1 = Image.open("imgs/anhtam2.jpg")
    # new_image1 = img_scale1.resize((500, 700))
    # new_image1.save('imgs/example_resized2.jpg')
    progress_bar.update(5)
    loaded["loaddata5"] = f'{progress_bar}'
    # return f"{progress_bar}"
    # # Get the uploaded files
    # src_file = request.files['src']
    # dst_file = request.files['dst']
    # from_file=request.files['from']
    # my_list=[src_file , dst_file]
    # val=random.choice(my_list)
    # print(val)
    # Save the uploaded files to disk
    # src_path =  'imgs/src_img1.jpg'
    # dst_path =  'imgs/src_img2.jpg'
    # from_path=  'imgs/couple.jpg'
    # val.save(src_path)
    # src_file.save(src_path)
    # dst_file.save(dst_path)
    # from_file.save(from_path)

    # open image
    # index=0
    # img = Image.open("imgs/anhtam3.jpg")
    # # new_image = img.resize((500, 500))
    # # new_image.save('example_resized.jpg')
    # # lấy kích thước ảnh
    # width, height = img.size
    #
    # # cắt lấy nửa ảnh đầu trên
    # img_cropped1 = img.crop((0, 0, width//2 -40, height))
    # # lưu ảnh đã cắt
    # img_cropped1.save("imgs/img_1.jpg")
    # # cắt lấy nửa ảnh đầu trên
    # img_cropped2 = img.crop((width//2-40, 0, width, height))
    # # lưu ảnh đã cắt
    # img_cropped2.save("imgs/img_2.jpg")

    # Swap faces
    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam2.jpg', out='results/output1.jpg', warp_2d=False,
                              correct_color=False, no_debug_window=True)
    src_img = cv2.imread(args.src)
    dst_img = cv2.imread(args.dst)
    src_points, src_shape, src_face = select_face(src_img)
    dst_faceBoxes = select_all_faces(dst_img)

    # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False, correct_color=False, no_debug_window=True)
    # src_img2 = cv2.imread(args1.src)
    # dst_img2 = cv2.imread(args1.dst)
    # src_points2, src_shape2, src_face2 = select_face(src_img2)
    # dst_faceBoxes2 = select_all_faces(dst_img2)
    # progress_bar.update(6)
    progress_bar.update(6)
    loaded["loaddata6"] = f'{progress_bar}'
    print("process6 ", progress_bar)
    if dst_faceBoxes is None:
        print('Detect 0 Face !!!')
        exit(-1)
    output = dst_img

    # if dst_faceBoxes2 is None:
    #     print('Detect 0 Face !!!')
    #     exit(-1)
    # output2 = dst_img2
    progress_bar.update(7)
    loaded["loaddata7"] = f'{progress_bar}'
    print("process7 ", progress_bar)
    for k, dst_face in dst_faceBoxes.items():
        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"], output, args)
    output_path = 'results/output1.jpg'
    cv2.imwrite(output_path, output)

    # for k, dst_face2 in dst_faceBoxes2.items():
    #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2, args1)
    # output_path2 = 'results/output2.jpg'
    # cv2.imwrite(output_path2, output2)
    progress_bar.update(8)
    loaded["loaddata8"] = f'{progress_bar}'
    # print("thanh cong ")
    # image = cv2.imread('results/output1.jpg')
    # print()
    # image_1 = cv2.imread('results/output1.jpg')
    # image_2 = cv2.imread('results/output2.jpg')
    # progress_bar.update(9)
    # loaded["loaddata9"] = f'{progress_bar}'
    # # print("image1",image_1.shape)
    # # print("image2",image_2.shape)
    #
    # # ghép hai ảnh lại với nhau theo chiều ngang
    # combined_img = cv2.hconcat([image_1, image_2])
    result_img = 'results/output1.jpg'
    # # hiển thị ảnh đã ghép
    # cv2.imshow('Combined Image', combined_img)
    # cv2.imwrite(result_img, combined_img)
    # Return the output image
    # return send_file(result_img, mimetype='image/jpeg')
    api_key = "fd81b5da86e162ade162a05220c0eb89"
    direct_link = upload_image_to_imgbb(result_img, api_key)
    # loaded.append(direct_link)1
    loaded["Link_img"] = direct_link
    progress_bar.update(10)
    loaded["loaddata91=finish"] = f'{progress_bar}'
    # print("process10 ", progress_bar)
    progress_bar.close()
    return loaded

@app.route('/homevs2', methods=['GET', 'POST'])
def index2():
    list_data = []
    index_demo = 0
    # while (True):
    loaded = {}
    link_full1 = request.headers.get('Link_img1')
    link_full2 = request.headers.get('Link_img2')
    # link_full3 = request.headers.get('Link_img3')
    # link_full4 = request.headers.get('Link_img4')
    # khởi tạo thanh tiến trình
    progress_bar = tqdm(total=55, unit="records")
    if (link_full1[0:19] == 'https://github.com/'):
        link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
        if "blob/" in link_full1:
            link_full1 = link_full1.replace("blob/", '')
        if "/main" in link_full1:
            link_full1 = link_full1.replace("/raw/", "/")
    progress_bar.update(1)
    # print("process1 ",progress_bar)
    loaded["loaddata1"] = f'{progress_bar}'
    if (link_full2[0:19] == 'https://github.com/'):
        link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
        if "blob/" in link_full2:
            link_full2 = link_full2.replace("blob/", '')
        if "/main" in link_full2:
            link_full2 = link_full2.replace("/raw/", "/")
    progress_bar.update(2)
    loaded["loaddata2"] = f'{progress_bar}'
    # if (link_full3[0:19] == 'https://github.com/'):
    #     link_full3 = link_full3.replace("github.com/", "raw.githubusercontent.com/")
    #     if "blob/" in link_full3:
    #         link_full3 = link_full3.replace("blob/", '')
    #     if "/main" in link_full3:
    #         link_full3 = link_full3.replace("/raw/", "/")
    # progress_bar.update(3)
    # loaded["loaddata3"] = f'{progress_bar}'
    # if (link_full4[0:19] == 'https://github.com/'):
    #     link_full4 = link_full4.replace("github.com/", "raw.githubusercontent.com/")
    #     if "blob/" in link_full4:
    #         link_full4 = link_full4.replace("blob/", '')
    #     if "/main" in link_full4:
    #         link_full4 = link_full4.replace("/raw/", "/")

    progress_bar.update(4)
    loaded["loaddata4"] = f'{progress_bar}'
    filename1 = 'imgs/anhtam1.jpg'
    filename2 = 'imgs/anhtam2.jpg'
    filename3 = 'imgs/anhtam3.jpg'
    filename4 = 'imgs/anhtam4.jpg'
    download_image(link_full1, filename1)
    download_image(link_full2, filename2)
    # download_image(link_full3, filename3)
    # download_image(link_full4, filename4)
    config = {
        'user': 'root',
        'password': 'BAdong14102001!',
        'host': 'localhost',
        'port': 3306,
        'database': 'swapcouple'
    }

    def make_counter(start, step):
        count = start

        def counter():
            nonlocal count
            result = count
            count += step
            return result

        return counter

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"You are connected to database: {db_name}")
        mycursor  = connection.cursor()
        random_index = random.randint(1,1)
        index_sk = random.randint(1, 12)

        # mycursor.execute(sql, val)
        random_sukien =['skhanhphuc','skchiatay','skkethon','sklyhon','skmuasam', 'sknym']
        random_sk=random.choice(random_sukien)
        print(random_sk)


        # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
        mycursor.execute(f"SELECT thongtin FROM {random_sk} where id={index_sk}")
        result2 = mycursor.fetchall()
        print('result2', result2[0])
        print("***")
        my_string = ', '.join(result2[0])
        print('mystring',my_string)
        loaded["thongtin"]=my_string
        mycursor.execute(f"SELECT nam FROM {random_sk} where id={index_sk}")
        result3 = mycursor.fetchall()
        print('result3', result3[0])
        print("***")
        my_string1 = ', '.join(result3[0])
        print('mystring', my_string1)

        mycursor.execute(f"SELECT nu FROM {random_sk} where id={index_sk}")
        result4 = mycursor.fetchall()
        print('result4', result4[0])
        print("***")
        my_string2 = ', '.join(result4[0])
        print('mystring', my_string2)
        # download_image(my_string1, filename3)
        # download_image(my_string2, filename4)
        download_image(my_string1, filename3)
        download_image(my_string2, filename4)
        if (my_string1==""):
            print("hello 1")
        if (my_string2==""):
            print("hello 2")
        sql = "INSERT INTO datademo(img_husband , img_wife, img_root1, img_root2 , thongtin_sk) VALUES (%s, %s , %s ,%s ,%s )"
        val = (link_full1, link_full2, my_string1, my_string2 , my_string)
        mycursor.execute(sql, val)
        result1 = mycursor.fetchall()
        # Lưu các thay đổi vào database
        connection.commit()
        # mycursor.execute("SELECT thongtin from skhanhphuc")
        print(mycursor.rowcount, "record inserted.")
        # mycursor1.execute("Select thongtin from skhanhphuc")x
        # connection.commit()

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL database: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

    # mycursor = connection.cursor()
    # # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
    # sql = "INSERT INTO swapcouple (id, img_husband ,img_wife , img_root1 ,img_root2) VALUES (%s, %s , %s ,%s ,%s)"
    # val = (1, link_full1 , link_full2 ,link_full3 ,link_full4)
    # mycursor.execute(sql, val)
    # # Lưu các thay đổi vào database
    # connection.commit()
    #
    # print(mycursor.rowcount, "record inserted.")

    # print("https://github.com/ngahuynh1/ctanh/blob/main/wi6.jpg")
    # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
    # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
    # print("download thanh cong")
    # download_image(link_full3 , filename3)
    # rescale image

    # img_scale = Image.open("imgs/anhtam1.jpg")
    # print("hihia")
    # img_scale = Image.open(BytesIO(response.content))

    # new_image = img_scale.resize((500, 700))
    # new_image.save('imgs/example_resized1.jpg')
    #
    #
    # img_scale1 = Image.open("imgs/anhtam2.jpg")
    # new_image1 = img_scale1.resize((500, 700))
    # new_image1.save('imgs/example_resized2.jpg')
    progress_bar.update(5)
    loaded["loaddata5"] = f'{progress_bar}'
    # return f"{progress_bar}"
    # # Get the uploaded files
    # src_file = request.files['src']

    # dst_file = request.files['dst']
    # from_file=request.files['from']
    # my_list=[src_file , dst_file]
    # val=random.choice(my_list)
    # print(val)
    # Save the uploaded files to disk
    # src_path =  'imgs/src_img1.jpg'
    # dst_path =  'imgs/src_img2.jpg'
    # from_path=  'imgs/couple.jpg'
    # val.save(src_path)
    # src_file.save(src_path)
    # dst_file.save(dst_path)
    # from_file.save(from_path)

    # open image
    # index=0
    # img = Image.open("imgs/anhtam3.jpg")
    # # new_image = img.resize((500, 500))
    # # new_image.save('example_resized.jpg')
    # # lấy kích thước ảnh
    # width, height = img.size
    #
    # # cắt lấy nửa ảnh đầu trên
    # img_cropped1 = img.crop((0, 0, width//2 -40, height))
    # # lưu ảnh đã cắt
    # img_cropped1.save("imgs/img_1.jpg")
    # # cắt lấy nửa ảnh đầu trên
    # img_cropped2 = img.crop((width//2-40, 0, width, height))
    # # lưu ảnh đã cắt
    # img_cropped2.save("imgs/img_2.jpg")

    # Swap faces
    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg', warp_2d=False,
                              correct_color=False, no_debug_window=True)
    src_img = cv2.imread(args.src)
    dst_img = cv2.imread(args.dst)
    src_points, src_shape, src_face = select_face(src_img)
    dst_faceBoxes = select_all_faces(dst_img)

    args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False,
                               correct_color=False, no_debug_window=True)
    src_img2 = cv2.imread(args1.src)
    dst_img2 = cv2.imread(args1.dst)
    src_points2, src_shape2, src_face2 = select_face(src_img2)
    dst_faceBoxes2 = select_all_faces(dst_img2)
    # progress_bar.update(6)
    progress_bar.update(6)
    loaded["loaddata6"] = f'{progress_bar}'
    print("process6 ", progress_bar)
    if dst_faceBoxes is None:
        print('Detect 0 Face !!!')
        exit(-1)
    output = dst_img

    if dst_faceBoxes2 is None:
        print('Detect 0 Face !!!')
        exit(-1)
    output2 = dst_img2
    progress_bar.update(7)
    loaded["loaddata7"] = f'{progress_bar}'
    print("process7 ", progress_bar)
    for k, dst_face in dst_faceBoxes.items():
        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"], output, args)
    output_path = 'results/output1.jpg'
    cv2.imwrite(output_path, output)

    for k, dst_face2 in dst_faceBoxes2.items():
        output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2,
                            args1)
    output_path2 = 'results/output2.jpg'
    cv2.imwrite(output_path2, output2)
    progress_bar.update(8)
    loaded["loaddata8"] = f'{progress_bar}'
    # print("thanh cong ")
    # image = cv2.imread('results/output1.jpg')
    # print()
    image_1 = cv2.imread('results/output1.jpg')
    image_2 = cv2.imread('results/output2.jpg')
    progress_bar.update(9)
    loaded["loaddata9"] = f'{progress_bar}'
    # print("image1",image_1.shape)
    # print("image2",image_2.shape)

    print("hoanhthanh")
    # ghép hai ảnh lại với nhau theo chiều ngang
    combined_img = cv2.hconcat([image_1, image_2])
    result_img = 'results/output.jpg'
    # hiển thị ảnh đã ghép
    # cv2.imshow('Combined Image', combined_img)
    cv2.imwrite(result_img, combined_img)
    # Return the output image
    # return send_file(result_img, mimetype='image/jpeg')
    random_api_key=["9011a7cfd693ed788a0a98814fc7a118"]
    api_key = "0648864ce249f9b501bb3ff7735eb1cd"
    click_random_api = random.choice(random_api_key)

    direct_link = upload_image_to_imgbb(result_img,click_random_api)
    # loaded.append(direct_link)
    loaded["Link_img"] = direct_link
    progress_bar.update(10)
    loaded["loaddata91=finish"] = f'{progress_bar}'
    # print("process10 ", progress_bar)
    progress_bar.close()
    list_data.append(loaded)
    index_demo+=1

    print("index_demo" , index_demo)
    return list_data

@app.route('/hometh1', methods=['GET', 'POST'])
def index3():
    list_data = []
    index_demo = 0
    while (True):
        loaded = {}
        link_full1 = request.headers.get('Link_img1')
        link_full2 = request.headers.get('Link_img2')
        # link_full3 = request.headers.get('Link_img3')
        # link_full4 = request.headers.get('Link_img4')
        # khởi tạo thanh tiến trình
        progress_bar = tqdm(total=55, unit="records")
        if (link_full1[0:19] == 'https://github.com/'):
            link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
            if "blob/" in link_full1:
                link_full1 = link_full1.replace("blob/", '')
            if "/main" in link_full1:
                link_full1 = link_full1.replace("/raw/", "/")
        progress_bar.update(1)
        # print("process1 ",progress_bar)
        loaded["loaddata1"] = f'{progress_bar}'
        if (link_full2[0:19] == 'https://github.com/'):
            link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
            if "blob/" in link_full2:
                link_full2 = link_full2.replace("blob/", '')
            if "/main" in link_full2:
                link_full2 = link_full2.replace("/raw/", "/")
        progress_bar.update(2)
        loaded["loaddata2"] = f'{progress_bar}'
        # if (link_full3[0:19] == 'https://github.com/'):
        #     link_full3 = link_full3.replace("github.com/", "raw.githubusercontent.com/")
        #     if "blob/" in link_full3:
        #         link_full3 = link_full3.replace("blob/", '')
        #     if "/main" in link_full3:
        #         link_full3 = link_full3.replace("/raw/", "/")
        # progress_bar.update(3)
        # loaded["loaddata3"] = f'{progress_bar}'
        # if (link_full4[0:19] == 'https://github.com/'):
        #     link_full4 = link_full4.replace("github.com/", "raw.githubusercontent.com/")
        #     if "blob/" in link_full4:
        #         link_full4 = link_full4.replace("blob/", '')
        #     if "/main" in link_full4:
        #         link_full4 = link_full4.replace("/raw/", "/")

        progress_bar.update(4)
        loaded["loaddata4"] = f'{progress_bar}'
        filename1 = 'imgs/anhtam1.jpg'
        filename2 = 'imgs/anhtam2.jpg'
        filename3 = 'imgs/anhtam3.jpg'
        filename4 = 'imgs/anhtam4.jpg'
        download_image(link_full1, filename1)
        download_image(link_full2, filename2)
        # download_image(link_full3, filename3)
        # download_image(link_full4, filename4)
        config = {
            'user': 'root',
            'password': 'BAdong14102001!',
            'host': 'localhost',
            'port': 3306,
            'database': 'swapcouple'
        }

        def make_counter(start, step):
            count = start

            def counter():
                nonlocal count
                result = count
                count += step
                return result

            return counter

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print("Connected to MySQL database")
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                print(f"You are connected to database: {db_name}")
            mycursor  = connection.cursor()
            random_index = random.randint(1,1)
            index_sk = random.randint(1, 12)

            # mycursor.execute(sql, val)
            random_sukien =['skchiatay','sknym','dotuoi','skhanhphuc','skkethon', 'skmuasam']
            random_sk=random.choice(random_sukien)
            print(random_sk)


            # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
            mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk}")
            result2 = mycursor.fetchall()
            print('result2', result2[0])
            print("***")
            my_string = ', '.join(result2[0])
            print('mystring',my_string)
            loaded["thongtin"]=my_string
            mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk}")
            result3 = mycursor.fetchall()
            print('result3', result3[0])
            print("***")
            my_string1 = ', '.join(result3[0])
            print('mystring', my_string1)

            mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk}")
            result4 = mycursor.fetchall()
            print('result4', result4[0])
            print("***")
            my_string2 = ', '.join(result4[0])
            print('mystring', my_string2)
            # download_image(my_string1, filename3)
            # download_image(my_string2, filename4)
            download_image(my_string1, filename3)
            download_image(my_string2, filename4)
            if (my_string1==""):
                print("hello 1")
            if (my_string2==""):
                print("hello 2")
            sql = "INSERT INTO datademo(img_husband , img_wife, img_root1, img_root2 , thongtin_sk) VALUES (%s, %s , %s ,%s ,%s )"
            val = (link_full1, link_full2, my_string1, my_string2 , my_string)
            mycursor.execute(sql, val)
            result1 = mycursor.fetchall()
            # Lưu các thay đổi vào database
            connection.commit()
            # mycursor.execute("SELECT thongtin from skhanhphuc")
            print(mycursor.rowcount, "record inserted.")
            # mycursor1.execute("Select thongtin from skhanhphuc")x
            # connection.commit()

        except mysql.connector.Error as error:
            print(f"Failed to connect to MySQL database: {error}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed")

        # mycursor = connection.cursor()
        # # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
        # sql = "INSERT INTO swapcouple (id, img_husband ,img_wife , img_root1 ,img_root2) VALUES (%s, %s , %s ,%s ,%s)"
        # val = (1, link_full1 , link_full2 ,link_full3 ,link_full4)
        # mycursor.execute(sql, val)
        # # Lưu các thay đổi vào database
        # connection.commit()
        #
        # print(mycursor.rowcount, "record inserted.")

        # print("https://github.com/ngahuynh1/ctanh/blob/main/wi6.jpg")
        # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
        # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
        # print("download thanh cong")
        # download_image(link_full3 , filename3)
        # rescale image

        # img_scale = Image.open("imgs/anhtam1.jpg")
        # print("hihia")
        # img_scale = Image.open(BytesIO(response.content))

        # new_image = img_scale.resize((500, 700))
        # new_image.save('imgs/example_resized1.jpg')
        #
        #
        # img_scale1 = Image.open("imgs/anhtam2.jpg")
        # new_image1 = img_scale1.resize((500, 700))
        # new_image1.save('imgs/example_resized2.jpg')
        progress_bar.update(5)
        loaded["loaddata5"] = f'{progress_bar}'
        # return f"{progress_bar}"
        # # Get the uploaded files
        # src_file = request.files['src']

        # dst_file = request.files['dst']
        # from_file=request.files['from']
        # my_list=[src_file , dst_file]
        # val=random.choice(my_list)
        # print(val)
        # Save the uploaded files to disk
        # src_path =  'imgs/src_img1.jpg'
        # dst_path =  'imgs/src_img2.jpg'
        # from_path=  'imgs/couple.jpg'
        # val.save(src_path)
        # src_file.save(src_path)
        # dst_file.save(dst_path)
        # from_file.save(from_path)

        # open image
        # index=0
        # img = Image.open("imgs/anhtam3.jpg")
        # # new_image = img.resize((500, 500))
        # # new_image.save('example_resized.jpg')
        # # lấy kích thước ảnh
        # width, height = img.size
        #
        # # cắt lấy nửa ảnh đầu trên
        # img_cropped1 = img.crop((0, 0, width//2 -40, height))
        # # lưu ảnh đã cắt
        # img_cropped1.save("imgs/img_1.jpg")
        # # cắt lấy nửa ảnh đầu trên
        # img_cropped2 = img.crop((width//2-40, 0, width, height))
        # # lưu ảnh đã cắt
        # img_cropped2.save("imgs/img_2.jpg")

        # Swap faces
        args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg', warp_2d=False,
                                  correct_color=False, no_debug_window=True)
        src_img = cv2.imread(args.src)
        dst_img = cv2.imread(args.dst)
        src_points, src_shape, src_face = select_face(src_img)
        dst_faceBoxes = select_all_faces(dst_img)

        args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False,
                                   correct_color=False, no_debug_window=True)
        src_img2 = cv2.imread(args1.src)
        dst_img2 = cv2.imread(args1.dst)
        src_points2, src_shape2, src_face2 = select_face(src_img2)
        dst_faceBoxes2 = select_all_faces(dst_img2)
        # progress_bar.update(6)
        progress_bar.update(6)
        loaded["loaddata6"] = f'{progress_bar}'
        print("process6 ", progress_bar)
        if dst_faceBoxes is None:
            print('Detect 0 Face !!!')
            exit(-1)
        output = dst_img

        if dst_faceBoxes2 is None:
            print('Detect 0 Face !!!')
            exit(-1)
        output2 = dst_img2
        progress_bar.update(7)
        loaded["loaddata7"] = f'{progress_bar}'
        print("process7 ", progress_bar)
        for k, dst_face in dst_faceBoxes.items():
            output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"], output, args)
        output_path = 'results/output1.jpg'
        cv2.imwrite(output_path, output)

        for k, dst_face2 in dst_faceBoxes2.items():
            output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2,
                                args1)
        output_path2 = 'results/output2.jpg'
        cv2.imwrite(output_path2, output2)
        progress_bar.update(8)
        loaded["loaddata8"] = f'{progress_bar}'
        # print("thanh cong ")
        # image = cv2.imread('results/output1.jpg')
        # print()
        image1 = Image.open('results/output1.jpg')
        image2 = Image.open('results/output2.jpg')
        image_1 = cv2.imread('results/output1.jpg')
        image_2 = cv2.imread('results/output2.jpg')

        progress_bar.update(9)
        width1, height1 = image1.size
        width2, height2 = image2.size
        max_width = max(width1, width2)
        max_height = max(height1, height2)
        new_image = Image.new('RGB', (max_width * 2, max_height))
        # chuyen anh dau vao vi tri (0,0)

        new_image.paste(image1, (0, 0))
        # chuyen anh dau vao vi tri (max_width,0)
        new_image.paste(image2, (max_width, 0))
        new_image.save('results/output.jpg')
        loaded["loaddata9"] = f'{progress_bar}'
        # height ,width , depth =image_1.shape
        # print("heigh" , height,width, depth)
        # image2= image2.resize((height, width) )
        #
        # print("image1",image_1.shape)
        # print("image2",image_2.shape)
        #
        # print("hoanhthanh")
        # # ghép hai ảnh lại với nhau theo chiều ngang
        # combined_img = cv2.hconcat([image1, image2])
        # result_img = 'results/output.jpg'
        # hiển thị ảnh đã ghép
        # cv2.imshow('Combined Image', combined_img)
        # cv2.imwrite(result_img, combined_img)
        # Return the output image
        # return send_file(result_img, mimetype='image/jpeg')
        random_api_key=["408faa95f5bd226c370fd41cb62b4614","ddc51a8c2a1ed5ef16a9faf321c6821a","ddc51a8c2a1ed5ef16a9faf321c6821a","9011a7cfd693ed788a0a98814fc7a118","ef1cb4ba4157f0abf53fa17447f10fe7","31aef57415d034fdb2489d3bedf5d6a4","1c590c3d10c9b92fbfbb1c9eef1cea06","6374d7c9cfa9f0cb372098bdf76d806e","21778d638b0d33c5d855729746deba81","0cb8df6d364699a53973c9a6ce3c4466","7f9fc33be9d03f6775f31d9af2af3858","e3a75062a4e22018ad8c3ab8f24eee5c","7239a119b60707f567ebd17c097f5696","92cd47cbd5c08f5465d6f5d465bf4f8d","e54c198b082708db094ad5b6663b4df8"]
        api_key = "0648864ce249f9b501bb3ff7735eb1cd"
        click_random_api = random.choice(random_api_key)
        print("random_api",click_random_api)
        direct_link = upload_image_to_imgbb('results/output.jpg',click_random_api)
        # loaded.append(direct_link)
        loaded["Link_img"] = direct_link
        progress_bar.update(10)
        loaded["loaddata91=finish"] = f'{progress_bar}'
        # print("process10 ", progress_bar)
        progress_bar.close()
        list_data.append(loaded)
        index_demo+=1
        if index_demo ==5:
            break
    print("index_demo" , index_demo)
    return list_data

@app.route('/hometh2', methods=['GET', 'POST'])
def index4():
    list_data = []
    index_demo = 0
    random_case =random.randint(1,3)
    print("random_case", random_case)
    if random_case==1:
        while (True):
            loaded = {}
            choose_case = 0
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')
            # link_full3 = request.headers.get('Link_img3')
            # link_full4 = request.headers.get('Link_img4')
            # khởi tạo thanh tiến trình
            progress_bar = tqdm(total=55, unit="records")
            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")
            progress_bar.update(1)
            # print("process1 ",progress_bar)
            loaded["loaddata1"] = f'{progress_bar}'
            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")
            progress_bar.update(2)
            loaded["loaddata2"] = f'{progress_bar}'
            # if (link_full3[0:19] == 'https://github.com/'):
            #     link_full3 = link_full3.replace("github.com/", "raw.githubusercontent.com/")
            #     if "blob/" in link_full3:
            #         link_full3 = link_full3.replace("blob/", '')
            #     if "/main" in link_full3:
            #         link_full3 = link_full3.replace("/raw/", "/")
            # progress_bar.update(3)
            # loaded["loaddata3"] = f'{progress_bar}'
            # if (link_full4[0:19] == 'https://github.com/'):
            #     link_full4 = link_full4.replace("github.com/", "raw.githubusercontent.com/")
            #     if "blob/" in link_full4:
            #         link_full4 = link_full4.replace("blob/", '')
            #     if "/main" in link_full4:
            #         link_full4 = link_full4.replace("/raw/", "/")

            progress_bar.update(4)
            loaded["loaddata4"] = f'{progress_bar}'
            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            # download_image(link_full3, filename3)
            # download_image(link_full4, filename4)

            config = {
                'user': 'root',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'swapcouple'
            }

            def make_counter(start, step):
                count = start

                def counter():
                    nonlocal count
                    result = count
                    count += step
                    return result

                return counter

            try:
                connection = mysql.connector.connect(**config)
                if connection.is_connected():
                    print("Connected to MySQL database")
                    cursor = connection.cursor()
                    cursor.execute("SELECT DATABASE();")
                    db_name = cursor.fetchone()[0]
                    print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor()
                mycursor1 = connection.cursor()
                # mycursor1.execute("Select * from skhanhphuc")
                # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
                # print('maek', make_counter(8, 1))
                # date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                # val = (link_full1, link_full2, link_full3, link_full4 )
                # sql = f"INSERT INTO dataset2(id,img_husband, img_wife, img_root1, img_root2,update_time) VALUES     {val}"

                # mycursor.execute(sql, val)
                random_sukien = ['skchiatay', 'sknym', 'skhanhphuc', 'skkethon', 'skmuasam']
                random_sk = random.choice(random_sukien)
                print(random_sk)
                index_sk = random.randint(1, 12)

                # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
                mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk}")
                result2 = mycursor.fetchall()
                print('result2', result2[0])
                my_string = ', '.join(result2[0])
                print('mystring', my_string)

                mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]}  where id={index_sk}")
                result5 = mycursor.fetchall()
                print('result5', result5[0])
                my_string12 = ', '.join(result5[0])
                print('mystring', my_string12)

                mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk}")
                result6 = mycursor.fetchall()
                print('result6', result6[0])
                my_string13 = ', '.join(result6[0])
                print('mystring', my_string13)

                mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk}")
                result3 = mycursor.fetchall()
                print('result3', result3[0])
                print("***")
                my_string1 = ', '.join(result3[0])
                print('mystring', my_string1)

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0":
                    choose_case = 2
                    download_image(my_string1, filename3)

                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                loaded["thongtin"] = my_string
                sql = "INSERT INTO datademo (img_husband ,img_wife , img_root1 ,img_root2 , thongtin_sk) VALUES (%s, %s , %s ,%s ,%s )"
                val = (link_full1, link_full2, my_string1, my_string2, my_string)
                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()

                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")
                # mycursor1.execute("Select thongtin from skhanhphuc")x
                # connection.commit()

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            # mycursor = connection.cursor()
            # # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
            # sql = "INSERT INTO swapcouple (id, img_husband ,img_wife , img_root1 ,img_root2) VALUES (%s, %s , %s ,%s ,%s)"
            # val = (1, link_full1 , link_full2 ,link_full3 ,link_full4)
            # mycursor.execute(sql, val)
            # # Lưu các thay đổi vào database
            # connection.commit()
            #
            # print(mycursor.rowcount, "record inserted.")

            # print("https://github.com/ngahuynh1/ctanh/blob/main/wi6.jpg")
            # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
            # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
            # print("download thanh cong")
            # download_image(link_full3 , filename3)
            # rescale image

            # img_scale = Image.open("imgs/anhtam1.jpg")
            # print("hihia")
            # img_scale = Image.open(BytesIO(response.content))

            # new_image = img_scale.resize((500, 700))
            # new_image.save('imgs/example_resized1.jpg')
            #
            #
            # img_scale1 = Image.open("imgs/anhtam2.jpg")
            # new_image1 = img_scale1.resize((500, 700))
            # new_image1.save('imgs/example_resized2.jpg')
            progress_bar.update(5)
            loaded["loaddata5"] = f'{progress_bar}'
            # return f"{progress_bar}"
            # # Get the uploaded files
            # src_file = request.files['src']

            # dst_file = request.files['dst']
            # from_file=request.files['from']
            # my_list=[src_file , dst_file]
            # val=random.choice(my_list)
            # print(val)
            # Save the uploaded files to disk
            # src_path =  'imgs/src_img1.jpg'
            # dst_path =  'imgs/src_img2.jpg'
            # from_path=  'imgs/couple.jpg'
            # val.save(src_path)
            # src_file.save(src_path)
            # dst_file.save(dst_path)
            # from_file.save(from_path)

            # open image
            # index=0
            # img = Image.open("imgs/anhtam3.jpg")
            # # new_image = img.resize((500, 500))
            # # new_image.save('example_resized.jpg')
            # # lấy kích thước ảnh
            # width, height = img.size
            #
            # # cắt lấy nửa ảnh đầu trên
            # img_cropped1 = img.crop((0, 0, width//2 -40, height))
            # # lưu ảnh đã cắt
            # img_cropped1.save("imgs/img_1.jpg")
            # # cắt lấy nửa ảnh đầu trên
            # img_cropped2 = img.crop((width//2-40, 0, width, height))
            # # lưu ảnh đã cắt
            # img_cropped2.save("imgs/img_2.jpg")
            print("choose case", choose_case)
            if choose_case == 1:

                # Swap faces
                args = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output1.jpg',
                                          warp_2d=False,
                                          correct_color=False, no_debug_window=True)
                src_img = cv2.imread(args.src)
                dst_img = cv2.imread(args.dst)
                src_points, src_shape, src_face = select_face(src_img)
                dst_faceBoxes = select_all_faces(dst_img)
                #
                # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False,
                #                            correct_color=False, no_debug_window=True)
                # src_img2 = cv2.imread(args1.src)
                # dst_img2 = cv2.imread(args1.dst)
                # src_points2, src_shape2, src_face2 = select_face(src_img2)
                # dst_faceBoxes2 = select_all_faces(dst_img2)
                # progress_bar.update(6)
                progress_bar.update(6)
                loaded["loaddata6"] = f'{progress_bar}'
                print("process6 ", progress_bar)
                if dst_faceBoxes is None:
                    print('Detect 0 Face !!!')
                output = dst_img

                # if dst_faceBoxes2 is None:
                #     print('Detect 0 Face !!!')
                #     exit(-1)
                # output2 = dst_img2
                progress_bar.update(7)
                loaded["loaddata7"] = f'{progress_bar}'
                print("process7 ", progress_bar)
                for k, dst_face in dst_faceBoxes.items():
                    output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"],
                                       output, args)
                output_path = 'results/output1.jpg'
                cv2.imwrite(output_path, output)

                # for k, dst_face2 in dst_faceBoxes2.items():
                #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2,
                #                         args1)
                # output_path2 = 'results/output2.jpg'
                # cv2.imwrite(output_path2, output2)
                progress_bar.update(8)
                loaded["loaddata8"] = f'{progress_bar}'
                # print("thanh cong ")
                # image = cv2.imread('results/output1.jpg')
                # # print()
                # image1 = Image.open('results/output1.jpg')
                # image2 = Image.open('results/output2.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                #
                # progress_bar.update(9)
                # width1, height1 = image1.size
                # width2, height2 = image2.size
                # max_width = max(width1, width2)
                # max_height = max(height1, height2)
                # new_image = Image.new('RGB', (max_width * 2, max_height))
                # new_image.paste(image1, (0, 0))
                # # chuyen anh dau vao vi tri (max_width,0)
                # new_image.paste(image2, (max_width, 0))
                # new_image.save('results/output.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                progress_bar.update(9)
                loaded["loaddata9"] = f'{progress_bar}'
                # print("image1",image_1.shape)
                # print("image2",image_2.shape)

                # ghép hai ảnh lại với nhau theo chiều ngang
                # combined_img = cv2.hconcat([image_1, image_2])
                # result_img = 'results/output.jpg'
                # hiển thị ảnh đã ghép
                # cv2.imshow('Combined Image', combined_img)
                # cv2.imwrite(result_img, new_image)
                # Return the output image
                # return send_file(result_img, mimetype='image/jpeg')
                api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                direct_link = upload_image_to_imgbb(output_path, api_key)
                # loaded.append(direct_link)
                loaded["Link_img"] = direct_link
                progress_bar.update(10)
                loaded["loaddata91=finish"] = f'{progress_bar}'
                # print("process10 ", progress_bar)
                progress_bar.close()
                list_data.append(loaded)
                # index_demo += 1
                # if index_demo == 5:
                #     break
                # print("index_demo", index_demo)
                # return list_data
            if choose_case == 2:

                args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                          warp_2d=False,
                                          correct_color=False, no_debug_window=True)
                src_img = cv2.imread(args.src)
                dst_img = cv2.imread(args.dst)
                src_points, src_shape, src_face = select_face(src_img)
                dst_faceBoxes = select_all_faces(dst_img)
                #
                # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False,
                #                            correct_color=False, no_debug_window=True)
                # src_img2 = cv2.imread(args1.src)
                # dst_img2 = cv2.imread(args1.dst)
                # src_points2, src_shape2, src_face2 = select_face(src_img2)
                # dst_faceBoxes2 = select_all_faces(dst_img2)
                # progress_bar.update(6)
                progress_bar.update(6)
                loaded["loaddata6"] = f'{progress_bar}'
                print("process6 ", progress_bar)
                if dst_faceBoxes is None:
                    print('Detect 0 Face !!!')
                output = dst_img

                # if dst_faceBoxes2 is None:
                #     print('Detect 0 Face !!!')
                #     exit(-1)
                # output2 = dst_img2
                progress_bar.update(7)
                loaded["loaddata7"] = f'{progress_bar}'
                print("process7 ", progress_bar)
                for k, dst_face in dst_faceBoxes.items():
                    output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"],
                                       output,
                                       args)
                output_path = 'results/output1.jpg'
                cv2.imwrite(output_path, output)

                # for k, dst_face2 in dst_faceBoxes2.items():
                #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2,
                #                         args1)
                # output_path2 = 'results/output2.jpg'
                # cv2.imwrite(output_path2, output2)
                progress_bar.update(8)
                loaded["loaddata8"] = f'{progress_bar}'
                # print("thanh cong ")
                # image = cv2.imread('results/output1.jpg')
                # # print()
                # image1 = Image.open('results/output1.jpg')
                # image2 = Image.open('results/output2.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                #
                # progress_bar.update(9)
                # width1, height1 = image1.size
                # width2, height2 = image2.size
                # max_width = max(width1, width2)
                # max_height = max(height1, height2)
                # new_image = Image.new('RGB', (max_width * 2, max_height))
                # new_image.paste(image1, (0, 0))
                # # chuyen anh dau vao vi tri (max_width,0)
                # new_image.paste(image2, (max_width, 0))
                # new_image.save('results/output.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                progress_bar.update(9)
                loaded["loaddata9"] = f'{progress_bar}'
                # print("image1",image_1.shape)
                # print("image2",image_2.shape)

                # ghép hai ảnh lại với nhau theo chiều ngang
                # combined_img = cv2.hconcat([image_1, image_2])
                # result_img = 'results/output.jpg'
                # hiển thị ảnh đã ghép
                # cv2.imshow('Combined Image', combined_img)
                # cv2.imwrite(result_img, new_image)
                # Return the output image
                # return send_file(result_img, mimetype='image/jpeg')
                api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                direct_link = upload_image_to_imgbb(output_path, api_key)
                # loaded.append(direct_link)
                loaded["Link_img"] = direct_link
                progress_bar.update(10)
                loaded["loaddata91=finish"] = f'{progress_bar}'
                # print("process10 ", progress_bar)
                progress_bar.close()
                list_data.append(loaded)
                # index_demo += 1
                # if index_demo == 5:
                #     break
                # print("index_demo", index_demo)
                # return list_data
            if choose_case == 3:
                if my_string13 == "namsau":
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                               out='results/output2.jpg',
                                               warp_2d=False,
                                               correct_color=False, no_debug_window=True)
                    src_img2 = cv2.imread(args1.src)
                    dst_img2 = cv2.imread(args1.dst)
                    src_points2, src_shape2, src_face2 = select_face(src_img2)
                    dst_faceBoxes2 = select_all_faces(dst_img2)
                    # progress_bar.update(6)
                    progress_bar.update(6)
                    loaded["loaddata6"] = f'{progress_bar}'
                    print("process6 ", progress_bar)
                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    if dst_faceBoxes2 is None:
                        print('Detect 0 Face !!!')
                        exit(-1)
                    output2 = dst_img2
                    progress_bar.update(7)
                    loaded["loaddata7"] = f'{progress_bar}'
                    print("process7 ", progress_bar)
                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"], output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)

                    for k, dst_face2 in dst_faceBoxes2.items():
                        output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                            dst_face2["shape"],
                                            output2,
                                            args1)
                    output_path2 = 'results/output2.jpg'
                    cv2.imwrite(output_path2, output2)
                    progress_bar.update(8)
                    loaded["loaddata8"] = f'{progress_bar}'
                    # print("thanh cong ")
                    # image = cv2.imread('results/output1.jpg')
                    # print()
                    image1 = Image.open('results/output1.jpg')
                    image2 = Image.open('results/output2.jpg')

                    image_1 = cv2.imread('results/output1.jpg')
                    image_2 = cv2.imread('results/output2.jpg')

                    progress_bar.update(9)
                    width1, height1 = image1.size
                    width2, height2 = image2.size
                    max_width = max(width1, width2)
                    max_height = max(height1, height2)
                    new_image = Image.new('RGB', (max_width * 2, max_height))
                    new_image.paste(image2, (0, 0))
                    # chuyen anh dau vao vi tri (max_width,0)
                    new_image.paste(image1, (max_width, 0))
                    new_image.save('results/output.jpg')
                    # image_1 = cv2.imread('results/output1.jpg')
                    # image_2 = cv2.imread('results/output2.jpg')
                    progress_bar.update(9)
                    loaded["loaddata9"] = f'{progress_bar}'
                    # print("image1",image_1.shape)
                    # print("image2",image_2.shape)

                    # ghép hai ảnh lại với nhau theo chiều ngang
                    # combined_img = cv2.hconcat([image_1, image_2])
                    result_img = 'results/output.jpg'
                    # hiển thị ảnh đã ghép
                    # cv2.imshow('Combined Image', combined_img)
                    # cv2.imwrite(result_img, new_image)
                    # Return the output image
                    # return send_file(result_img, mimetype='image/jpeg')
                    api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    # loaded.append(direct_link)
                    loaded["Link_img"] = direct_link
                    progress_bar.update(10)
                    loaded["loaddata91=finish"] = f'{progress_bar}'
                    # print("process10 ", progress_bar)
                    progress_bar.close()
                    list_data.append(loaded)
                    # index_demo += 1
                    # if index_demo == 5:
                    #     break
                    # print("index_demo", index_demo)
                    # return list_data
                else:
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                               out='results/output2.jpg',
                                               warp_2d=False,
                                               correct_color=False, no_debug_window=True)
                    src_img2 = cv2.imread(args1.src)
                    dst_img2 = cv2.imread(args1.dst)
                    src_points2, src_shape2, src_face2 = select_face(src_img2)
                    dst_faceBoxes2 = select_all_faces(dst_img2)
                    # progress_bar.update(6)
                    progress_bar.update(6)
                    loaded["loaddata6"] = f'{progress_bar}'
                    print("process6 ", progress_bar)
                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    if dst_faceBoxes2 is None:
                        print('Detect 0 Face !!!')
                        exit(-1)
                    output2 = dst_img2
                    progress_bar.update(7)
                    loaded["loaddata7"] = f'{progress_bar}'
                    print("process7 ", progress_bar)
                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)

                    for k, dst_face2 in dst_faceBoxes2.items():
                        output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                            dst_face2["shape"],
                                            output2,
                                            args1)
                    output_path2 = 'results/output2.jpg'
                    cv2.imwrite(output_path2, output2)
                    progress_bar.update(8)
                    loaded["loaddata8"] = f'{progress_bar}'
                    # print("thanh cong ")
                    # image = cv2.imread('results/output1.jpg')
                    # print()
                    image1 = Image.open('results/output1.jpg')
                    image2 = Image.open('results/output2.jpg')

                    image_1 = cv2.imread('results/output1.jpg')
                    image_2 = cv2.imread('results/output2.jpg')

                    progress_bar.update(9)
                    width1, height1 = image1.size
                    width2, height2 = image2.size
                    max_width = max(width1, width2)
                    max_height = max(height1, height2)
                    new_image = Image.new('RGB', (max_width * 2, max_height))
                    new_image.paste(image1, (0, 0))
                    # chuyen anh dau vao vi tri (max_width,0)
                    new_image.paste(image2, (max_width, 0))
                    new_image.save('results/output.jpg')
                    # image_1 = cv2.imread('results/output1.jpg')
                    # image_2 = cv2.imread('results/output2.jpg')
                    progress_bar.update(9)
                    loaded["loaddata9"] = f'{progress_bar}'
                    # print("image1",image_1.shape)
                    # print("image2",image_2.shape)

                    # ghép hai ảnh lại với nhau theo chiều ngang
                    # combined_img = cv2.hconcat([image_1, image_2])
                    result_img = 'results/output.jpg'
                    # hiển thị ảnh đã ghép
                    # cv2.imshow('Combined Image', combined_img)
                    # cv2.imwrite(result_img, new_image)
                    # Return the output image
                    # return send_file(result_img, mimetype='image/jpeg')
                    api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    # loaded.append(direct_link)
                    loaded["Link_img"] = direct_link
                    progress_bar.update(10)
                    loaded["loaddata91=finish"] = f'{progress_bar}'
                    # print("process10 ", progress_bar)
                    progress_bar.close()
                    list_data.append(loaded)
                    # index_demo += 1
                    # if index_demo == 5:
                    #     break
                    # print("index_demo", index_demo)
                    # return list_data
            if choose_case == 4:
                # Swap faces
                # args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                #                           warp_2d=False,
                #                           correct_color=False, no_debug_window=True)
                # src_img = cv2.imread(args.src)
                # dst_img = cv2.imread(args.dst)
                # src_points, src_shape, src_face = select_face(src_img)
                # dst_faceBoxes = select_all_faces(dst_img)
                #
                # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg',
                #                            warp_2d=False,
                #                            correct_color=False, no_debug_window=True)
                # src_img2 = cv2.imread(args1.src)
                # dst_img2 = cv2.imread(args1.dst)
                # src_points2, src_shape2, src_face2 = select_face(src_img2)
                # dst_faceBoxes2 = select_all_faces(dst_img2)
                # # progress_bar.update(6)
                progress_bar.update(6)
                loaded["loaddata6"] = f'{progress_bar}'
                # print("process6 ", progress_bar)
                # if dst_faceBoxes is None:
                #     print('Detect 0 Face !!!')
                # output = dst_img
                #
                # if dst_faceBoxes2 is None:
                #     print('Detect 0 Face !!!')
                #     exit(-1)
                # output2 = dst_img2
                # progress_bar.update(7)
                loaded["loaddata7"] = f'{progress_bar}'
                print("process7 ", progress_bar)
                # for k, dst_face in dst_faceBoxes.items():
                #     output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"], output,
                #                        args)
                # output_path = 'results/output1.jpg'
                # cv2.imwrite(output_path, output)
                #
                # for k, dst_face2 in dst_faceBoxes2.items():
                #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"],
                #                         output2,
                #                         args1)
                # output_path2 = 'results/output2.jpg'
                # cv2.imwrite(output_path2, output2)
                progress_bar.update(8)
                loaded["loaddata8"] = f'{progress_bar}'
                # # print("thanh cong ")
                # # image = cv2.imread('results/output1.jpg')
                # # print()
                # image1 = Image.open('results/output1.jpg')
                # image2 = Image.open('results/output2.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                #
                # progress_bar.update(9)
                # width1, height1 = image1.size
                # width2, height2 = image2.size
                # max_width = max(width1, width2)
                # max_height = max(height1, height2)
                # new_image = Image.new('RGB', (max_width * 2, max_height))
                # new_image.paste(image1, (0, 0))
                # # chuyen anh dau vao vi tri (max_width,0)
                # new_image.paste(image2, (max_width, 0))
                # new_image.save('results/output.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                progress_bar.update(9)
                loaded["loaddata9"] = f'{progress_bar}'
                # print("image1",image_1.shape)
                # print("image2",image_2.shape)

                # ghép hai ảnh lại với nhau theo chiều ngang
                # combined_img = cv2.hconcat([image_1, image_2])
                result_img = 'results/output.jpg'
                # hiển thị ảnh đã ghép
                # cv2.imshow('Combined Image', combined_img)
                # cv2.imwrite(result_img, new_image)
                # Return the output image
                # return send_file(result_img, mimetype='image/jpeg')
                api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                direct_link = upload_image_to_imgbb(result_img, api_key)
                # loaded.append(direct_link)
                loaded["Link_img"] = direct_link
                progress_bar.update(10)
                loaded["loaddata91=finish"] = f'{progress_bar}'
                # print("process10 ", progress_bar)
                progress_bar.close()
                list_data.append(loaded)
                # return loaded

            index_demo += 1
            if index_demo == 4:
                break
            print("index_demo", index_demo)
        return list_data
    if random_case==2:
        while (True):
            loaded = {}
            choose_case = 0
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')
            # link_full3 = request.headers.get('Link_img3')
            # link_full4 = request.headers.get('Link_img4')
            # khởi tạo thanh tiến trình
            progress_bar = tqdm(total=55, unit="records")
            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")
            progress_bar.update(1)
            # print("process1 ",progress_bar)
            loaded["loaddata1"] = f'{progress_bar}'
            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")
            progress_bar.update(2)
            loaded["loaddata2"] = f'{progress_bar}'
            # if (link_full3[0:19] == 'https://github.com/'):
            #     link_full3 = link_full3.replace("github.com/", "raw.githubusercontent.com/")
            #     if "blob/" in link_full3:
            #         link_full3 = link_full3.replace("blob/", '')
            #     if "/main" in link_full3:
            #         link_full3 = link_full3.replace("/raw/", "/")
            # progress_bar.update(3)
            # loaded["loaddata3"] = f'{progress_bar}'
            # if (link_full4[0:19] == 'https://github.com/'):
            #     link_full4 = link_full4.replace("github.com/", "raw.githubusercontent.com/")
            #     if "blob/" in link_full4:
            #         link_full4 = link_full4.replace("blob/", '')
            #     if "/main" in link_full4:
            #         link_full4 = link_full4.replace("/raw/", "/")

            progress_bar.update(4)
            loaded["loaddata4"] = f'{progress_bar}'
            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            # download_image(link_full3, filename3)
            # download_image(link_full4, filename4)

            config = {
                'user': 'root',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'swapcouple'
            }

            def make_counter(start, step):
                count = start

                def counter():
                    nonlocal count
                    result = count
                    count += step
                    return result

                return counter

            try:
                connection = mysql.connector.connect(**config)
                if connection.is_connected():
                    print("Connected to MySQL database")
                    cursor = connection.cursor()
                    cursor.execute("SELECT DATABASE();")
                    db_name = cursor.fetchone()[0]
                    print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor()
                mycursor1 = connection.cursor()
                # mycursor1.execute("Select * from skhanhphuc")
                # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
                # print('maek', make_counter(8, 1))
                # date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                # val = (link_full1, link_full2, link_full3, link_full4 )
                # sql = f"INSERT INTO dataset2(id,img_husband, img_wife, img_root1, img_root2,update_time) VALUES     {val}"

                # mycursor.execute(sql, val)
                random_sukien = ['skchiatay', 'sknym', 'skhanhphuc', 'skkethon', 'skmuasam', 'sklyhon']
                random_sk = random.choice(random_sukien)
                print(random_sk)
                index_sk = random.randint(1, 12)

                # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
                mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk}")
                result2 = mycursor.fetchall()
                print('result2', result2[0])
                my_string = ', '.join(result2[0])
                print('mystring', my_string)

                mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]}  where id={index_sk}")
                result5 = mycursor.fetchall()
                print('result5', result5[0])
                my_string12 = ', '.join(result5[0])
                print('mystring', my_string12)

                mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk}")
                result6 = mycursor.fetchall()
                print('result6', result6[0])
                my_string13 = ', '.join(result6[0])
                print('mystring', my_string13)

                mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk}")
                result3 = mycursor.fetchall()
                print('result3', result3[0])
                print("***")
                my_string1 = ', '.join(result3[0])
                print('mystring', my_string1)

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0":
                    choose_case = 2
                    download_image(my_string1, filename3)

                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                loaded["thongtin"] = my_string
                sql = "INSERT INTO datademo (img_husband ,img_wife , img_root1 ,img_root2 , thongtin_sk) VALUES (%s, %s , %s ,%s ,%s )"
                val = (link_full1, link_full2, my_string1, my_string2, my_string)
                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()

                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")
                # mycursor1.execute("Select thongtin from skhanhphuc")x
                # connection.commit()

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            # mycursor = connection.cursor()
            # # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
            # sql = "INSERT INTO swapcouple (id, img_husband ,img_wife , img_root1 ,img_root2) VALUES (%s, %s , %s ,%s ,%s)"
            # val = (1, link_full1 , link_full2 ,link_full3 ,link_full4)
            # mycursor.execute(sql, val)
            # # Lưu các thay đổi vào database
            # connection.commit()
            #
            # print(mycursor.rowcount, "record inserted.")

            # print("https://github.com/ngahuynh1/ctanh/blob/main/wi6.jpg")
            # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
            # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
            # print("download thanh cong")
            # download_image(link_full3 , filename3)
            # rescale image

            # img_scale = Image.open("imgs/anhtam1.jpg")
            # print("hihia")
            # img_scale = Image.open(BytesIO(response.content))

            # new_image = img_scale.resize((500, 700))
            # new_image.save('imgs/example_resized1.jpg')
            #
            #
            # img_scale1 = Image.open("imgs/anhtam2.jpg")
            # new_image1 = img_scale1.resize((500, 700))
            # new_image1.save('imgs/example_resized2.jpg')
            progress_bar.update(5)
            loaded["loaddata5"] = f'{progress_bar}'
            # return f"{progress_bar}"
            # # Get the uploaded files
            # src_file = request.files['src']

            # dst_file = request.files['dst']
            # from_file=request.files['from']
            # my_list=[src_file , dst_file]
            # val=random.choice(my_list)
            # print(val)
            # Save the uploaded files to disk
            # src_path =  'imgs/src_img1.jpg'
            # dst_path =  'imgs/src_img2.jpg'
            # from_path=  'imgs/couple.jpg'
            # val.save(src_path)
            # src_file.save(src_path)
            # dst_file.save(dst_path)
            # from_file.save(from_path)

            # open image
            # index=0
            # img = Image.open("imgs/anhtam3.jpg")
            # # new_image = img.resize((500, 500))
            # # new_image.save('example_resized.jpg')
            # # lấy kích thước ảnh
            # width, height = img.size
            #
            # # cắt lấy nửa ảnh đầu trên
            # img_cropped1 = img.crop((0, 0, width//2 -40, height))
            # # lưu ảnh đã cắt
            # img_cropped1.save("imgs/img_1.jpg")
            # # cắt lấy nửa ảnh đầu trên
            # img_cropped2 = img.crop((width//2-40, 0, width, height))
            # # lưu ảnh đã cắt
            # img_cropped2.save("imgs/img_2.jpg")
            print("choose case", choose_case)
            if choose_case == 1:

                # Swap faces
                args = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output1.jpg',
                                          warp_2d=False,
                                          correct_color=False, no_debug_window=True)
                src_img = cv2.imread(args.src)
                dst_img = cv2.imread(args.dst)
                src_points, src_shape, src_face = select_face(src_img)
                dst_faceBoxes = select_all_faces(dst_img)
                #
                # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False,
                #                            correct_color=False, no_debug_window=True)
                # src_img2 = cv2.imread(args1.src)
                # dst_img2 = cv2.imread(args1.dst)
                # src_points2, src_shape2, src_face2 = select_face(src_img2)
                # dst_faceBoxes2 = select_all_faces(dst_img2)
                # progress_bar.update(6)
                progress_bar.update(6)
                loaded["loaddata6"] = f'{progress_bar}'
                print("process6 ", progress_bar)
                if dst_faceBoxes is None:
                    print('Detect 0 Face !!!')
                output = dst_img

                # if dst_faceBoxes2 is None:
                #     print('Detect 0 Face !!!')
                #     exit(-1)
                # output2 = dst_img2
                progress_bar.update(7)
                loaded["loaddata7"] = f'{progress_bar}'
                print("process7 ", progress_bar)
                for k, dst_face in dst_faceBoxes.items():
                    output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"],
                                       output, args)
                output_path = 'results/output1.jpg'
                cv2.imwrite(output_path, output)

                # for k, dst_face2 in dst_faceBoxes2.items():
                #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2,
                #                         args1)
                # output_path2 = 'results/output2.jpg'
                # cv2.imwrite(output_path2, output2)
                progress_bar.update(8)
                loaded["loaddata8"] = f'{progress_bar}'
                # print("thanh cong ")
                # image = cv2.imread('results/output1.jpg')
                # # print()
                # image1 = Image.open('results/output1.jpg')
                # image2 = Image.open('results/output2.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                #
                # progress_bar.update(9)
                # width1, height1 = image1.size
                # width2, height2 = image2.size
                # max_width = max(width1, width2)
                # max_height = max(height1, height2)
                # new_image = Image.new('RGB', (max_width * 2, max_height))
                # new_image.paste(image1, (0, 0))
                # # chuyen anh dau vao vi tri (max_width,0)
                # new_image.paste(image2, (max_width, 0))
                # new_image.save('results/output.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                progress_bar.update(9)
                loaded["loaddata9"] = f'{progress_bar}'
                # print("image1",image_1.shape)
                # print("image2",image_2.shape)

                # ghép hai ảnh lại với nhau theo chiều ngang
                # combined_img = cv2.hconcat([image_1, image_2])
                # result_img = 'results/output.jpg'
                # hiển thị ảnh đã ghép
                # cv2.imshow('Combined Image', combined_img)
                # cv2.imwrite(result_img, new_image)
                # Return the output image
                # return send_file(result_img, mimetype='image/jpeg')
                api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                direct_link = upload_image_to_imgbb(output_path, api_key)
                # loaded.append(direct_link)
                loaded["Link_img"] = direct_link
                progress_bar.update(10)
                loaded["loaddata91=finish"] = f'{progress_bar}'
                # print("process10 ", progress_bar)
                progress_bar.close()
                list_data.append(loaded)
                # index_demo += 1
                # if index_demo == 5:
                #     break
                # print("index_demo", index_demo)
                # return list_data
            if choose_case == 2:

                args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                          warp_2d=False,
                                          correct_color=False, no_debug_window=True)
                src_img = cv2.imread(args.src)
                dst_img = cv2.imread(args.dst)
                src_points, src_shape, src_face = select_face(src_img)
                dst_faceBoxes = select_all_faces(dst_img)
                #
                # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False,
                #                            correct_color=False, no_debug_window=True)
                # src_img2 = cv2.imread(args1.src)
                # dst_img2 = cv2.imread(args1.dst)
                # src_points2, src_shape2, src_face2 = select_face(src_img2)
                # dst_faceBoxes2 = select_all_faces(dst_img2)
                # progress_bar.update(6)
                progress_bar.update(6)
                loaded["loaddata6"] = f'{progress_bar}'
                print("process6 ", progress_bar)
                if dst_faceBoxes is None:
                    print('Detect 0 Face !!!')
                output = dst_img

                # if dst_faceBoxes2 is None:
                #     print('Detect 0 Face !!!')
                #     exit(-1)
                # output2 = dst_img2
                progress_bar.update(7)
                loaded["loaddata7"] = f'{progress_bar}'
                print("process7 ", progress_bar)
                for k, dst_face in dst_faceBoxes.items():
                    output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"],
                                       output,
                                       args)
                output_path = 'results/output1.jpg'
                cv2.imwrite(output_path, output)

                # for k, dst_face2 in dst_faceBoxes2.items():
                #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2,
                #                         args1)
                # output_path2 = 'results/output2.jpg'
                # cv2.imwrite(output_path2, output2)
                progress_bar.update(8)
                loaded["loaddata8"] = f'{progress_bar}'
                # print("thanh cong ")
                # image = cv2.imread('results/output1.jpg')
                # # print()
                # image1 = Image.open('results/output1.jpg')
                # image2 = Image.open('results/output2.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                #
                # progress_bar.update(9)
                # width1, height1 = image1.size
                # width2, height2 = image2.size
                # max_width = max(width1, width2)
                # max_height = max(height1, height2)
                # new_image = Image.new('RGB', (max_width * 2, max_height))
                # new_image.paste(image1, (0, 0))
                # # chuyen anh dau vao vi tri (max_width,0)
                # new_image.paste(image2, (max_width, 0))
                # new_image.save('results/output.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                progress_bar.update(9)
                loaded["loaddata9"] = f'{progress_bar}'
                # print("image1",image_1.shape)
                # print("image2",image_2.shape)

                # ghép hai ảnh lại với nhau theo chiều ngang
                # combined_img = cv2.hconcat([image_1, image_2])
                # result_img = 'results/output.jpg'
                # hiển thị ảnh đã ghép
                # cv2.imshow('Combined Image', combined_img)
                # cv2.imwrite(result_img, new_image)
                # Return the output image
                # return send_file(result_img, mimetype='image/jpeg')
                api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                direct_link = upload_image_to_imgbb(output_path, api_key)
                # loaded.append(direct_link)
                loaded["Link_img"] = direct_link
                progress_bar.update(10)
                loaded["loaddata91=finish"] = f'{progress_bar}'
                # print("process10 ", progress_bar)
                progress_bar.close()
                list_data.append(loaded)
                # index_demo += 1
                # if index_demo == 5:
                #     break
                # print("index_demo", index_demo)
                # return list_data
            if choose_case == 3:
                if my_string13 == "namsau":
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                               out='results/output2.jpg',
                                               warp_2d=False,
                                               correct_color=False, no_debug_window=True)
                    src_img2 = cv2.imread(args1.src)
                    dst_img2 = cv2.imread(args1.dst)
                    src_points2, src_shape2, src_face2 = select_face(src_img2)
                    dst_faceBoxes2 = select_all_faces(dst_img2)
                    # progress_bar.update(6)
                    progress_bar.update(6)
                    loaded["loaddata6"] = f'{progress_bar}'
                    print("process6 ", progress_bar)
                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    if dst_faceBoxes2 is None:
                        print('Detect 0 Face !!!')
                        exit(-1)
                    output2 = dst_img2
                    progress_bar.update(7)
                    loaded["loaddata7"] = f'{progress_bar}'
                    print("process7 ", progress_bar)
                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"], output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)

                    for k, dst_face2 in dst_faceBoxes2.items():
                        output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                            dst_face2["shape"],
                                            output2,
                                            args1)
                    output_path2 = 'results/output2.jpg'
                    cv2.imwrite(output_path2, output2)
                    progress_bar.update(8)
                    loaded["loaddata8"] = f'{progress_bar}'
                    # print("thanh cong ")
                    # image = cv2.imread('results/output1.jpg')
                    # print()
                    image1 = Image.open('results/output1.jpg')
                    image2 = Image.open('results/output2.jpg')

                    image_1 = cv2.imread('results/output1.jpg')
                    image_2 = cv2.imread('results/output2.jpg')

                    progress_bar.update(9)
                    width1, height1 = image1.size
                    width2, height2 = image2.size
                    max_width = max(width1, width2)
                    max_height = max(height1, height2)
                    new_image = Image.new('RGB', (max_width * 2, max_height))
                    new_image.paste(image2, (0, 0))
                    # chuyen anh dau vao vi tri (max_width,0)
                    new_image.paste(image1, (max_width, 0))
                    new_image.save('results/output.jpg')
                    # image_1 = cv2.imread('results/output1.jpg')
                    # image_2 = cv2.imread('results/output2.jpg')
                    progress_bar.update(9)
                    loaded["loaddata9"] = f'{progress_bar}'
                    # print("image1",image_1.shape)
                    # print("image2",image_2.shape)

                    # ghép hai ảnh lại với nhau theo chiều ngang
                    # combined_img = cv2.hconcat([image_1, image_2])
                    result_img = 'results/output.jpg'
                    # hiển thị ảnh đã ghép
                    # cv2.imshow('Combined Image', combined_img)
                    # cv2.imwrite(result_img, new_image)
                    # Return the output image
                    # return send_file(result_img, mimetype='image/jpeg')
                    api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    # loaded.append(direct_link)
                    loaded["Link_img"] = direct_link
                    progress_bar.update(10)
                    loaded["loaddata91=finish"] = f'{progress_bar}'
                    # print("process10 ", progress_bar)
                    progress_bar.close()
                    list_data.append(loaded)
                    # index_demo += 1
                    # if index_demo == 5:
                    #     break
                    # print("index_demo", index_demo)
                    # return list_data
                else:
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                               out='results/output2.jpg',
                                               warp_2d=False,
                                               correct_color=False, no_debug_window=True)
                    src_img2 = cv2.imread(args1.src)
                    dst_img2 = cv2.imread(args1.dst)
                    src_points2, src_shape2, src_face2 = select_face(src_img2)
                    dst_faceBoxes2 = select_all_faces(dst_img2)
                    # progress_bar.update(6)
                    progress_bar.update(6)
                    loaded["loaddata6"] = f'{progress_bar}'
                    print("process6 ", progress_bar)
                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    if dst_faceBoxes2 is None:
                        print('Detect 0 Face !!!')
                        exit(-1)
                    output2 = dst_img2
                    progress_bar.update(7)
                    loaded["loaddata7"] = f'{progress_bar}'
                    print("process7 ", progress_bar)
                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)

                    for k, dst_face2 in dst_faceBoxes2.items():
                        output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                            dst_face2["shape"],
                                            output2,
                                            args1)
                    output_path2 = 'results/output2.jpg'
                    cv2.imwrite(output_path2, output2)
                    progress_bar.update(8)
                    loaded["loaddata8"] = f'{progress_bar}'
                    # print("thanh cong ")
                    # image = cv2.imread('results/output1.jpg')
                    # print()
                    image1 = Image.open('results/output1.jpg')
                    image2 = Image.open('results/output2.jpg')

                    image_1 = cv2.imread('results/output1.jpg')
                    image_2 = cv2.imread('results/output2.jpg')

                    progress_bar.update(9)
                    width1, height1 = image1.size
                    width2, height2 = image2.size
                    max_width = max(width1, width2)
                    max_height = max(height1, height2)
                    new_image = Image.new('RGB', (max_width * 2, max_height))
                    new_image.paste(image1, (0, 0))
                    # chuyen anh dau vao vi tri (max_width,0)
                    new_image.paste(image2, (max_width, 0))
                    new_image.save('results/output.jpg')
                    # image_1 = cv2.imread('results/output1.jpg')
                    # image_2 = cv2.imread('results/output2.jpg')
                    progress_bar.update(9)
                    loaded["loaddata9"] = f'{progress_bar}'
                    # print("image1",image_1.shape)
                    # print("image2",image_2.shape)

                    # ghép hai ảnh lại với nhau theo chiều ngang
                    # combined_img = cv2.hconcat([image_1, image_2])
                    result_img = 'results/output.jpg'
                    # hiển thị ảnh đã ghép
                    # cv2.imshow('Combined Image', combined_img)
                    # cv2.imwrite(result_img, new_image)
                    # Return the output image
                    # return send_file(result_img, mimetype='image/jpeg')
                    api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    # loaded.append(direct_link)
                    loaded["Link_img"] = direct_link
                    progress_bar.update(10)
                    loaded["loaddata91=finish"] = f'{progress_bar}'
                    # print("process10 ", progress_bar)
                    progress_bar.close()
                    list_data.append(loaded)
                    # index_demo += 1
                    # if index_demo == 5:
                    #     break
                    # print("index_demo", index_demo)
                    # return list_data
            if choose_case == 4:
                # Swap faces
                # args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                #                           warp_2d=False,
                #                           correct_color=False, no_debug_window=True)
                # src_img = cv2.imread(args.src)
                # dst_img = cv2.imread(args.dst)
                # src_points, src_shape, src_face = select_face(src_img)
                # dst_faceBoxes = select_all_faces(dst_img)
                #
                # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg',
                #                            warp_2d=False,
                #                            correct_color=False, no_debug_window=True)
                # src_img2 = cv2.imread(args1.src)
                # dst_img2 = cv2.imread(args1.dst)
                # src_points2, src_shape2, src_face2 = select_face(src_img2)
                # dst_faceBoxes2 = select_all_faces(dst_img2)
                # # progress_bar.update(6)
                progress_bar.update(6)
                loaded["loaddata6"] = f'{progress_bar}'
                # print("process6 ", progress_bar)
                # if dst_faceBoxes is None:
                #     print('Detect 0 Face !!!')
                # output = dst_img
                #
                # if dst_faceBoxes2 is None:
                #     print('Detect 0 Face !!!')
                #     exit(-1)
                # output2 = dst_img2
                # progress_bar.update(7)
                loaded["loaddata7"] = f'{progress_bar}'
                print("process7 ", progress_bar)
                # for k, dst_face in dst_faceBoxes.items():
                #     output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"], output,
                #                        args)
                # output_path = 'results/output1.jpg'
                # cv2.imwrite(output_path, output)
                #
                # for k, dst_face2 in dst_faceBoxes2.items():
                #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"],
                #                         output2,
                #                         args1)
                # output_path2 = 'results/output2.jpg'
                # cv2.imwrite(output_path2, output2)
                progress_bar.update(8)
                loaded["loaddata8"] = f'{progress_bar}'
                # # print("thanh cong ")
                # # image = cv2.imread('results/output1.jpg')
                # # print()
                # image1 = Image.open('results/output1.jpg')
                # image2 = Image.open('results/output2.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                #
                # progress_bar.update(9)
                # width1, height1 = image1.size
                # width2, height2 = image2.size
                # max_width = max(width1, width2)
                # max_height = max(height1, height2)
                # new_image = Image.new('RGB', (max_width * 2, max_height))
                # new_image.paste(image1, (0, 0))
                # # chuyen anh dau vao vi tri (max_width,0)
                # new_image.paste(image2, (max_width, 0))
                # new_image.save('results/output.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                progress_bar.update(9)
                loaded["loaddata9"] = f'{progress_bar}'
                # print("image1",image_1.shape)
                # print("image2",image_2.shape)

                # ghép hai ảnh lại với nhau theo chiều ngang
                # combined_img = cv2.hconcat([image_1, image_2])
                result_img = 'results/output.jpg'
                # hiển thị ảnh đã ghép
                # cv2.imshow('Combined Image', combined_img)
                # cv2.imwrite(result_img, new_image)
                # Return the output image
                # return send_file(result_img, mimetype='image/jpeg')
                api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                direct_link = upload_image_to_imgbb(result_img, api_key)
                # loaded.append(direct_link)
                loaded["Link_img"] = direct_link
                progress_bar.update(10)
                loaded["loaddata91=finish"] = f'{progress_bar}'
                # print("process10 ", progress_bar)
                progress_bar.close()
                list_data.append(loaded)
                # return loaded

            index_demo += 1
            if index_demo == 5:
                break
            print("index_demo", index_demo)
        return list_data
    if random_case==3:

        while (True):
            loaded = {}
            choose_case = 0
            link_full1 = request.headers.get('Link_img1')
            link_full2 = request.headers.get('Link_img2')
            # link_full3 = request.headers.get('Link_img3')
            # link_full4 = request.headers.get('Link_img4')
            # khởi tạo thanh tiến trình
            progress_bar = tqdm(total=55, unit="records")
            if (link_full1[0:19] == 'https://github.com/'):
                link_full1 = link_full1.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full1:
                    link_full1 = link_full1.replace("blob/", '')
                if "/main" in link_full1:
                    link_full1 = link_full1.replace("/raw/", "/")
            progress_bar.update(1)
            # print("process1 ",progress_bar)
            loaded["loaddata1"] = f'{progress_bar}'
            if (link_full2[0:19] == 'https://github.com/'):
                link_full2 = link_full2.replace("github.com/", "raw.githubusercontent.com/")
                if "blob/" in link_full2:
                    link_full2 = link_full2.replace("blob/", '')
                if "/main" in link_full2:
                    link_full2 = link_full2.replace("/raw/", "/")
            progress_bar.update(2)
            loaded["loaddata2"] = f'{progress_bar}'
            # if (link_full3[0:19] == 'https://github.com/'):
            #     link_full3 = link_full3.replace("github.com/", "raw.githubusercontent.com/")
            #     if "blob/" in link_full3:
            #         link_full3 = link_full3.replace("blob/", '')
            #     if "/main" in link_full3:
            #         link_full3 = link_full3.replace("/raw/", "/")
            # progress_bar.update(3)
            # loaded["loaddata3"] = f'{progress_bar}'
            # if (link_full4[0:19] == 'https://github.com/'):
            #     link_full4 = link_full4.replace("github.com/", "raw.githubusercontent.com/")
            #     if "blob/" in link_full4:
            #         link_full4 = link_full4.replace("blob/", '')
            #     if "/main" in link_full4:
            #         link_full4 = link_full4.replace("/raw/", "/")

            progress_bar.update(4)
            loaded["loaddata4"] = f'{progress_bar}'
            filename1 = 'imgs/anhtam1.jpg'
            filename2 = 'imgs/anhtam2.jpg'
            filename3 = 'imgs/anhtam3.jpg'
            filename4 = 'imgs/anhtam4.jpg'
            download_image(link_full1, filename1)
            download_image(link_full2, filename2)
            # download_image(link_full3, filename3)
            # download_image(link_full4, filename4)

            config = {
                'user': 'root',
                'password': 'BAdong14102001!',
                'host': 'localhost',
                'port': 3306,
                'database': 'swapcouple'
            }

            def make_counter(start, step):
                count = start

                def counter():
                    nonlocal count
                    result = count
                    count += step
                    return result

                return counter

            try:
                connection = mysql.connector.connect(**config)
                if connection.is_connected():
                    print("Connected to MySQL database")
                    cursor = connection.cursor()
                    cursor.execute("SELECT DATABASE();")
                    db_name = cursor.fetchone()[0]
                    print(f"You are connected to database: {db_name}")
                mycursor = connection.cursor()
                mycursor1 = connection.cursor()
                # mycursor1.execute("Select * from skhanhphuc")
                # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
                # print('maek', make_counter(8, 1))
                # date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                # val = (link_full1, link_full2, link_full3, link_full4 )
                # sql = f"INSERT INTO dataset2(id,img_husband, img_wife, img_root1, img_root2,update_time) VALUES     {val}"

                # mycursor.execute(sql, val)
                random_sukien = ['skhanhphuc', 'skkethon', 'skmuasam']
                random_sk = random.choice(random_sukien)
                print(random_sk)
                index_sk = random.randint(1, 12)

                # Thực hiện truy vấn SQL để lấy dữ liệu từ bảng
                mycursor.execute(f"SELECT thongtin FROM {random_sukien[index_demo]} where id={index_sk}")
                result2 = mycursor.fetchall()
                print('result2', result2[0])
                my_string = ', '.join(result2[0])
                print('mystring', my_string)

                mycursor.execute(f"SELECT image FROM {random_sukien[index_demo]}  where id={index_sk}")
                result5 = mycursor.fetchall()
                print('result5', result5[0])
                my_string12 = ', '.join(result5[0])
                print('mystring', my_string12)

                mycursor.execute(f"SELECT vtrinam FROM {random_sukien[index_demo]} where id={index_sk}")
                result6 = mycursor.fetchall()
                print('result6', result6[0])
                my_string13 = ', '.join(result6[0])
                print('mystring', my_string13)

                mycursor.execute(f"SELECT nam FROM {random_sukien[index_demo]} where id={index_sk}")
                result3 = mycursor.fetchall()
                print('result3', result3[0])
                print("***")
                my_string1 = ', '.join(result3[0])
                print('mystring', my_string1)

                mycursor.execute(f"SELECT nu FROM {random_sukien[index_demo]} where id={index_sk}")
                result4 = mycursor.fetchall()
                print('result4', result4[0])
                print("***")
                my_string2 = ', '.join(result4[0])
                print('mystring', my_string2)
                if my_string1 == "0" and my_string2 == "0":
                    choose_case = 4
                    download_image(my_string12, "results/output.jpg")
                elif my_string1 == "0":
                    choose_case = 1
                    download_image(my_string2, filename4)
                elif my_string2 == "0":
                    choose_case = 2
                    download_image(my_string1, filename3)

                else:
                    choose_case = 3
                    download_image(my_string1, filename3)
                    download_image(my_string2, filename4)
                print("choose_Case ", choose_case)

                loaded["thongtin"] = my_string
                sql = "INSERT INTO datademo (img_husband ,img_wife , img_root1 ,img_root2 , thongtin_sk) VALUES (%s, %s , %s ,%s ,%s )"
                val = (link_full1, link_full2, my_string1, my_string2, my_string)
                mycursor.execute(sql, val)
                result1 = mycursor.fetchall()

                # Lưu các thay đổi vào database
                connection.commit()
                # mycursor.execute("SELECT thongtin from skhanhphuc")
                print(mycursor.rowcount, "record inserted.")
                # mycursor1.execute("Select thongtin from skhanhphuc")x
                # connection.commit()

            except mysql.connector.Error as error:
                print(f"Failed to connect to MySQL database: {error}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")
            # mycursor = connection.cursor()
            # # Thực hiện truy vấn INSERT để insert dữ liệu vào bảng
            # sql = "INSERT INTO swapcouple (id, img_husband ,img_wife , img_root1 ,img_root2) VALUES (%s, %s , %s ,%s ,%s)"
            # val = (1, link_full1 , link_full2 ,link_full3 ,link_full4)
            # mycursor.execute(sql, val)
            # # Lưu các thay đổi vào database
            # connection.commit()
            #
            # print(mycursor.rowcount, "record inserted.")

            # print("https://github.com/ngahuynh1/ctanh/blob/main/wi6.jpg")
            # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
            # print("https://raw.githubusercontent.com/ngahuynh1/ctanh/main/wi6.jpg")
            # print("download thanh cong")
            # download_image(link_full3 , filename3)
            # rescale image

            # img_scale = Image.open("imgs/anhtam1.jpg")
            # print("hihia")
            # img_scale = Image.open(BytesIO(response.content))

            # new_image = img_scale.resize((500, 700))
            # new_image.save('imgs/example_resized1.jpg')
            #
            #
            # img_scale1 = Image.open("imgs/anhtam2.jpg")
            # new_image1 = img_scale1.resize((500, 700))
            # new_image1.save('imgs/example_resized2.jpg')
            progress_bar.update(5)
            loaded["loaddata5"] = f'{progress_bar}'
            # return f"{progress_bar}"
            # # Get the uploaded files
            # src_file = request.files['src']

            # dst_file = request.files['dst']
            # from_file=request.files['from']
            # my_list=[src_file , dst_file]
            # val=random.choice(my_list)
            # print(val)
            # Save the uploaded files to disk
            # src_path =  'imgs/src_img1.jpg'
            # dst_path =  'imgs/src_img2.jpg'
            # from_path=  'imgs/couple.jpg'
            # val.save(src_path)
            # src_file.save(src_path)
            # dst_file.save(dst_path)
            # from_file.save(from_path)

            # open image
            # index=0
            # img = Image.open("imgs/anhtam3.jpg")
            # # new_image = img.resize((500, 500))
            # # new_image.save('example_resized.jpg')
            # # lấy kích thước ảnh
            # width, height = img.size
            #
            # # cắt lấy nửa ảnh đầu trên
            # img_cropped1 = img.crop((0, 0, width//2 -40, height))
            # # lưu ảnh đã cắt
            # img_cropped1.save("imgs/img_1.jpg")
            # # cắt lấy nửa ảnh đầu trên
            # img_cropped2 = img.crop((width//2-40, 0, width, height))
            # # lưu ảnh đã cắt
            # img_cropped2.save("imgs/img_2.jpg")
            print("choose case", choose_case)
            if choose_case == 1:

                # Swap faces
                args = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output1.jpg',
                                          warp_2d=False,
                                          correct_color=False, no_debug_window=True)
                src_img = cv2.imread(args.src)
                dst_img = cv2.imread(args.dst)
                src_points, src_shape, src_face = select_face(src_img)
                dst_faceBoxes = select_all_faces(dst_img)
                #
                # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False,
                #                            correct_color=False, no_debug_window=True)
                # src_img2 = cv2.imread(args1.src)
                # dst_img2 = cv2.imread(args1.dst)
                # src_points2, src_shape2, src_face2 = select_face(src_img2)
                # dst_faceBoxes2 = select_all_faces(dst_img2)
                # progress_bar.update(6)
                progress_bar.update(6)
                loaded["loaddata6"] = f'{progress_bar}'
                print("process6 ", progress_bar)
                if dst_faceBoxes is None:
                    print('Detect 0 Face !!!')
                output = dst_img

                # if dst_faceBoxes2 is None:
                #     print('Detect 0 Face !!!')
                #     exit(-1)
                # output2 = dst_img2
                progress_bar.update(7)
                loaded["loaddata7"] = f'{progress_bar}'
                print("process7 ", progress_bar)
                for k, dst_face in dst_faceBoxes.items():
                    output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"],
                                       output, args)
                output_path = 'results/output1.jpg'
                cv2.imwrite(output_path, output)

                # for k, dst_face2 in dst_faceBoxes2.items():
                #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2,
                #                         args1)
                # output_path2 = 'results/output2.jpg'
                # cv2.imwrite(output_path2, output2)
                progress_bar.update(8)
                loaded["loaddata8"] = f'{progress_bar}'
                # print("thanh cong ")
                # image = cv2.imread('results/output1.jpg')
                # # print()
                # image1 = Image.open('results/output1.jpg')
                # image2 = Image.open('results/output2.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                #
                # progress_bar.update(9)
                # width1, height1 = image1.size
                # width2, height2 = image2.size
                # max_width = max(width1, width2)
                # max_height = max(height1, height2)
                # new_image = Image.new('RGB', (max_width * 2, max_height))
                # new_image.paste(image1, (0, 0))
                # # chuyen anh dau vao vi tri (max_width,0)
                # new_image.paste(image2, (max_width, 0))
                # new_image.save('results/output.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                progress_bar.update(9)
                loaded["loaddata9"] = f'{progress_bar}'
                # print("image1",image_1.shape)
                # print("image2",image_2.shape)

                # ghép hai ảnh lại với nhau theo chiều ngang
                # combined_img = cv2.hconcat([image_1, image_2])
                # result_img = 'results/output.jpg'
                # hiển thị ảnh đã ghép
                # cv2.imshow('Combined Image', combined_img)
                # cv2.imwrite(result_img, new_image)
                # Return the output image
                # return send_file(result_img, mimetype='image/jpeg')
                api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                direct_link = upload_image_to_imgbb(output_path, api_key)
                # loaded.append(direct_link)
                loaded["Link_img"] = direct_link
                progress_bar.update(10)
                loaded["loaddata91=finish"] = f'{progress_bar}'
                # print("process10 ", progress_bar)
                progress_bar.close()
                list_data.append(loaded)
                # index_demo += 1
                # if index_demo == 5:
                #     break
                # print("index_demo", index_demo)
                # return list_data
            if choose_case == 2:

                args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                          warp_2d=False,
                                          correct_color=False, no_debug_window=True)
                src_img = cv2.imread(args.src)
                dst_img = cv2.imread(args.dst)
                src_points, src_shape, src_face = select_face(src_img)
                dst_faceBoxes = select_all_faces(dst_img)
                #
                # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg', warp_2d=False,
                #                            correct_color=False, no_debug_window=True)
                # src_img2 = cv2.imread(args1.src)
                # dst_img2 = cv2.imread(args1.dst)
                # src_points2, src_shape2, src_face2 = select_face(src_img2)
                # dst_faceBoxes2 = select_all_faces(dst_img2)
                # progress_bar.update(6)
                progress_bar.update(6)
                loaded["loaddata6"] = f'{progress_bar}'
                print("process6 ", progress_bar)
                if dst_faceBoxes is None:
                    print('Detect 0 Face !!!')
                output = dst_img

                # if dst_faceBoxes2 is None:
                #     print('Detect 0 Face !!!')
                #     exit(-1)
                # output2 = dst_img2
                progress_bar.update(7)
                loaded["loaddata7"] = f'{progress_bar}'
                print("process7 ", progress_bar)
                for k, dst_face in dst_faceBoxes.items():
                    output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"],
                                       output,
                                       args)
                output_path = 'results/output1.jpg'
                cv2.imwrite(output_path, output)

                # for k, dst_face2 in dst_faceBoxes2.items():
                #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"], output2,
                #                         args1)
                # output_path2 = 'results/output2.jpg'
                # cv2.imwrite(output_path2, output2)
                progress_bar.update(8)
                loaded["loaddata8"] = f'{progress_bar}'
                # print("thanh cong ")
                # image = cv2.imread('results/output1.jpg')
                # # print()
                # image1 = Image.open('results/output1.jpg')
                # image2 = Image.open('results/output2.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                #
                # progress_bar.update(9)
                # width1, height1 = image1.size
                # width2, height2 = image2.size
                # max_width = max(width1, width2)
                # max_height = max(height1, height2)
                # new_image = Image.new('RGB', (max_width * 2, max_height))
                # new_image.paste(image1, (0, 0))
                # # chuyen anh dau vao vi tri (max_width,0)
                # new_image.paste(image2, (max_width, 0))
                # new_image.save('results/output.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                progress_bar.update(9)
                loaded["loaddata9"] = f'{progress_bar}'
                # print("image1",image_1.shape)
                # print("image2",image_2.shape)

                # ghép hai ảnh lại với nhau theo chiều ngang
                # combined_img = cv2.hconcat([image_1, image_2])
                # result_img = 'results/output.jpg'
                # hiển thị ảnh đã ghép
                # cv2.imshow('Combined Image', combined_img)
                # cv2.imwrite(result_img, new_image)
                # Return the output image
                # return send_file(result_img, mimetype='image/jpeg')
                api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                direct_link = upload_image_to_imgbb(output_path, api_key)
                # loaded.append(direct_link)
                loaded["Link_img"] = direct_link
                progress_bar.update(10)
                loaded["loaddata91=finish"] = f'{progress_bar}'
                # print("process10 ", progress_bar)
                progress_bar.close()
                list_data.append(loaded)
                # index_demo += 1
                # if index_demo == 5:
                #     break
                # print("index_demo", index_demo)
                # return list_data
            if choose_case == 3:
                if my_string13 == "namsau":
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                               out='results/output2.jpg',
                                               warp_2d=False,
                                               correct_color=False, no_debug_window=True)
                    src_img2 = cv2.imread(args1.src)
                    dst_img2 = cv2.imread(args1.dst)
                    src_points2, src_shape2, src_face2 = select_face(src_img2)
                    dst_faceBoxes2 = select_all_faces(dst_img2)
                    # progress_bar.update(6)
                    progress_bar.update(6)
                    loaded["loaddata6"] = f'{progress_bar}'
                    print("process6 ", progress_bar)
                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    if dst_faceBoxes2 is None:
                        print('Detect 0 Face !!!')
                        exit(-1)
                    output2 = dst_img2
                    progress_bar.update(7)
                    loaded["loaddata7"] = f'{progress_bar}'
                    print("process7 ", progress_bar)
                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"], output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)

                    for k, dst_face2 in dst_faceBoxes2.items():
                        output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                            dst_face2["shape"],
                                            output2,
                                            args1)
                    output_path2 = 'results/output2.jpg'
                    cv2.imwrite(output_path2, output2)
                    progress_bar.update(8)
                    loaded["loaddata8"] = f'{progress_bar}'
                    # print("thanh cong ")
                    # image = cv2.imread('results/output1.jpg')
                    # print()
                    image1 = Image.open('results/output1.jpg')
                    image2 = Image.open('results/output2.jpg')

                    image_1 = cv2.imread('results/output1.jpg')
                    image_2 = cv2.imread('results/output2.jpg')

                    progress_bar.update(9)
                    width1, height1 = image1.size
                    width2, height2 = image2.size
                    max_width = max(width1, width2)
                    max_height = max(height1, height2)
                    new_image = Image.new('RGB', (max_width * 2, max_height))
                    new_image.paste(image2, (0, 0))
                    # chuyen anh dau vao vi tri (max_width,0)
                    new_image.paste(image1, (max_width, 0))
                    new_image.save('results/output.jpg')
                    # image_1 = cv2.imread('results/output1.jpg')
                    # image_2 = cv2.imread('results/output2.jpg')
                    progress_bar.update(9)
                    loaded["loaddata9"] = f'{progress_bar}'
                    # print("image1",image_1.shape)
                    # print("image2",image_2.shape)

                    # ghép hai ảnh lại với nhau theo chiều ngang
                    # combined_img = cv2.hconcat([image_1, image_2])
                    result_img = 'results/output.jpg'
                    # hiển thị ảnh đã ghép
                    # cv2.imshow('Combined Image', combined_img)
                    # cv2.imwrite(result_img, new_image)
                    # Return the output image
                    # return send_file(result_img, mimetype='image/jpeg')
                    api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    # loaded.append(direct_link)
                    loaded["Link_img"] = direct_link
                    progress_bar.update(10)
                    loaded["loaddata91=finish"] = f'{progress_bar}'
                    # print("process10 ", progress_bar)
                    progress_bar.close()
                    list_data.append(loaded)
                    # index_demo += 1
                    # if index_demo == 5:
                    #     break
                    # print("index_demo", index_demo)
                    # return list_data
                else:
                    # Swap faces
                    args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                                              warp_2d=False,
                                              correct_color=False, no_debug_window=True)
                    src_img = cv2.imread(args.src)
                    dst_img = cv2.imread(args.dst)
                    src_points, src_shape, src_face = select_face(src_img)
                    dst_faceBoxes = select_all_faces(dst_img)

                    args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg',
                                               out='results/output2.jpg',
                                               warp_2d=False,
                                               correct_color=False, no_debug_window=True)
                    src_img2 = cv2.imread(args1.src)
                    dst_img2 = cv2.imread(args1.dst)
                    src_points2, src_shape2, src_face2 = select_face(src_img2)
                    dst_faceBoxes2 = select_all_faces(dst_img2)
                    # progress_bar.update(6)
                    progress_bar.update(6)
                    loaded["loaddata6"] = f'{progress_bar}'
                    print("process6 ", progress_bar)
                    if dst_faceBoxes is None:
                        print('Detect 0 Face !!!')
                    output = dst_img

                    if dst_faceBoxes2 is None:
                        print('Detect 0 Face !!!')
                        exit(-1)
                    output2 = dst_img2
                    progress_bar.update(7)
                    loaded["loaddata7"] = f'{progress_bar}'
                    print("process7 ", progress_bar)
                    for k, dst_face in dst_faceBoxes.items():
                        output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"],
                                           dst_face["shape"],
                                           output, args)
                    output_path = 'results/output1.jpg'
                    cv2.imwrite(output_path, output)

                    for k, dst_face2 in dst_faceBoxes2.items():
                        output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"],
                                            dst_face2["shape"],
                                            output2,
                                            args1)
                    output_path2 = 'results/output2.jpg'
                    cv2.imwrite(output_path2, output2)
                    progress_bar.update(8)
                    loaded["loaddata8"] = f'{progress_bar}'
                    # print("thanh cong ")
                    # image = cv2.imread('results/output1.jpg')
                    # print()
                    image1 = Image.open('results/output1.jpg')
                    image2 = Image.open('results/output2.jpg')

                    image_1 = cv2.imread('results/output1.jpg')
                    image_2 = cv2.imread('results/output2.jpg')

                    progress_bar.update(9)
                    width1, height1 = image1.size
                    width2, height2 = image2.size
                    max_width = max(width1, width2)
                    max_height = max(height1, height2)
                    new_image = Image.new('RGB', (max_width * 2, max_height))
                    new_image.paste(image1, (0, 0))
                    # chuyen anh dau vao vi tri (max_width,0)
                    new_image.paste(image2, (max_width, 0))
                    new_image.save('results/output.jpg')
                    # image_1 = cv2.imread('results/output1.jpg')
                    # image_2 = cv2.imread('results/output2.jpg')
                    progress_bar.update(9)
                    loaded["loaddata9"] = f'{progress_bar}'
                    # print("image1",image_1.shape)
                    # print("image2",image_2.shape)

                    # ghép hai ảnh lại với nhau theo chiều ngang
                    # combined_img = cv2.hconcat([image_1, image_2])
                    result_img = 'results/output.jpg'
                    # hiển thị ảnh đã ghép
                    # cv2.imshow('Combined Image', combined_img)
                    # cv2.imwrite(result_img, new_image)
                    # Return the output image
                    # return send_file(result_img, mimetype='image/jpeg')
                    api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                    direct_link = upload_image_to_imgbb(result_img, api_key)
                    # loaded.append(direct_link)
                    loaded["Link_img"] = direct_link
                    progress_bar.update(10)
                    loaded["loaddata91=finish"] = f'{progress_bar}'
                    # print("process10 ", progress_bar)
                    progress_bar.close()
                    list_data.append(loaded)
                    # index_demo += 1
                    # if index_demo == 5:
                    #     break
                    # print("index_demo", index_demo)
                    # return list_data
            if choose_case == 4:
                # Swap faces
                # args = argparse.Namespace(src='imgs/anhtam1.jpg', dst='imgs/anhtam3.jpg', out='results/output1.jpg',
                #                           warp_2d=False,
                #                           correct_color=False, no_debug_window=True)
                # src_img = cv2.imread(args.src)
                # dst_img = cv2.imread(args.dst)
                # src_points, src_shape, src_face = select_face(src_img)
                # dst_faceBoxes = select_all_faces(dst_img)
                #
                # args1 = argparse.Namespace(src='imgs/anhtam2.jpg', dst='imgs/anhtam4.jpg', out='results/output2.jpg',
                #                            warp_2d=False,
                #                            correct_color=False, no_debug_window=True)
                # src_img2 = cv2.imread(args1.src)
                # dst_img2 = cv2.imread(args1.dst)
                # src_points2, src_shape2, src_face2 = select_face(src_img2)
                # dst_faceBoxes2 = select_all_faces(dst_img2)
                # # progress_bar.update(6)
                progress_bar.update(6)
                loaded["loaddata6"] = f'{progress_bar}'
                # print("process6 ", progress_bar)
                # if dst_faceBoxes is None:
                #     print('Detect 0 Face !!!')
                # output = dst_img
                #
                # if dst_faceBoxes2 is None:
                #     print('Detect 0 Face !!!')
                #     exit(-1)
                # output2 = dst_img2
                # progress_bar.update(7)
                loaded["loaddata7"] = f'{progress_bar}'
                print("process7 ", progress_bar)
                # for k, dst_face in dst_faceBoxes.items():
                #     output = face_swap(src_face, dst_face["face"], src_points, dst_face["points"], dst_face["shape"], output,
                #                        args)
                # output_path = 'results/output1.jpg'
                # cv2.imwrite(output_path, output)
                #
                # for k, dst_face2 in dst_faceBoxes2.items():
                #     output2 = face_swap(src_face2, dst_face2["face"], src_points2, dst_face2["points"], dst_face2["shape"],
                #                         output2,
                #                         args1)
                # output_path2 = 'results/output2.jpg'
                # cv2.imwrite(output_path2, output2)
                progress_bar.update(8)
                loaded["loaddata8"] = f'{progress_bar}'
                # # print("thanh cong ")
                # # image = cv2.imread('results/output1.jpg')
                # # print()
                # image1 = Image.open('results/output1.jpg')
                # image2 = Image.open('results/output2.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                #
                # progress_bar.update(9)
                # width1, height1 = image1.size
                # width2, height2 = image2.size
                # max_width = max(width1, width2)
                # max_height = max(height1, height2)
                # new_image = Image.new('RGB', (max_width * 2, max_height))
                # new_image.paste(image1, (0, 0))
                # # chuyen anh dau vao vi tri (max_width,0)
                # new_image.paste(image2, (max_width, 0))
                # new_image.save('results/output.jpg')
                # image_1 = cv2.imread('results/output1.jpg')
                # image_2 = cv2.imread('results/output2.jpg')
                progress_bar.update(9)
                loaded["loaddata9"] = f'{progress_bar}'
                # print("image1",image_1.shape)
                # print("image2",image_2.shape)

                # ghép hai ảnh lại với nhau theo chiều ngang
                # combined_img = cv2.hconcat([image_1, image_2])
                result_img = 'results/output.jpg'
                # hiển thị ảnh đã ghép
                # cv2.imshow('Combined Image', combined_img)
                # cv2.imwrite(result_img, new_image)
                # Return the output image
                # return send_file(result_img, mimetype='image/jpeg')
                api_key = "1c590c3d10c9b92fbfbb1c9eef1cea06"
                direct_link = upload_image_to_imgbb(result_img, api_key)
                # loaded.append(direct_link)
                loaded["Link_img"] = direct_link
                progress_bar.update(10)
                loaded["loaddata91=finish"] = f'{progress_bar}'
                # print("process10 ", progress_bar)
                progress_bar.close()
                list_data.append(loaded)
                # return loaded

            index_demo += 1
            if index_demo == 2:
                break
            print("index_demo", index_demo)
        return list_data



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)
