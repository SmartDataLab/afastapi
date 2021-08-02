#!usr/bin/env python
# encoding:utf-8
from __future__ import division


import io
import os
import cv2
import json
import time
import grpc
import base64
import numpy as np
from PIL import Image
import data_pb2, data_pb2_grpc


_HOST = "localhost"
_PORT = "8080"


def run(img_path, id):  # img_pre_path, img_post_path

    connection = grpc.insecure_channel(
        _HOST + ":" + _PORT,
        options=[
            ("grpc.max_send_message_length", 50 * 1024 * 1024),
            ("grpc.max_receive_message_length", 50 * 1024 * 1024),
        ],
    )
    print("connection: ", connection)
    client = data_pb2_grpc.FormatDataStub(channel=connection)
    print("client: ", client)

    f1 = open(img_path, "rb")  # img_path
    string1 = base64.b64encode(f1.read())
    f2 = open(img_path.replace("_pre", "_post"), "rb")  # img_path
    # f2 = open("2.png", "rb")
    string2 = base64.b64encode(f2.read())

    res = client.DoFormat(data_pb2.actionrequest(img1=string1, img2=string2))  # 核心代码

    part1 = base64.b64decode(res.part1)
    part1 = Image.open(io.BytesIO(part1))
    part2 = base64.b64decode(res.part2)
    part2 = Image.open(io.BytesIO(part2))

    part1.save(
        os.path.join("{0}.png".format(id + "result_part1")),
    )
    part2.save(
        os.path.join("{0}.png".format(id + "result_part2")),
    )


def run2(img_path_pre, img_path_post):  # img_pre_path, img_post_path

    connection = grpc.insecure_channel(
        _HOST + ":" + _PORT,
        options=[
            ("grpc.max_send_message_length", 50 * 1024 * 1024),
            ("grpc.max_receive_message_length", 50 * 1024 * 1024),
        ],
    )
    print("connection: ", connection)
    client = data_pb2_grpc.FormatDataStub(channel=connection)
    print("client: ", client)

    f1 = open(img_path_pre, "rb")  # img_path
    string1 = base64.b64encode(f1.read())
    f2 = open(img_path_post, "rb")  # img_path
    # f2 = open("2.png", "rb")
    string2 = base64.b64encode(f2.read())

    res = client.DoFormat(data_pb2.actionrequest(img1=string1, img2=string2))  # 核心代码

    part1 = base64.b64decode(res.part1)
    part1 = Image.open(io.BytesIO(part1))
    part2 = base64.b64decode(res.part2)
    part2 = Image.open(io.BytesIO(part2))

    part1.save(
        os.path.join(
            "{0}.png".format(img_path_pre.split(".")[0].replace("_pre", "_result"))
        ),
    )
    part2.save(
        os.path.join(
            "{0}.png".format(
                img_path_pre.split(".")[0].replace("_pre", "_result_part2")
            )
        ),
    )


import time

if __name__ == "__main__":

    t0 = time.time()
    # img = "/data1/pdd/test/img/1_pre_.png"
    # img = "/data1/pdd/test/img/1_post_.png"
    # run(img)
    img = "/data1/su/pdd/afastapi/input/3_pre.png"
    # img = "test/images/socal-fire_00001384_pre_disaster.png"
    for i in range(10):
        run(img)
    t1 = time.time()

    print((t1 - t0) / 10)
