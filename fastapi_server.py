from fastapi import FastAPI, Request, File, UploadFile, HTTPException

import json
import os
import time
import random
import string
import numpy as np
from PIL import Image


import grpc_client

import base64

MAX_WIDTH = 102400
MAX_HEIGHT = 102400
RAW_IMG_PATH = "api_data/"
CUT_IMG_PATH = "results/sub_picture/"
CROP_SIZE = 1024
GPU_LIST = [0]

MAX_REQUEST = 5
global REQUEST_COUNT
REQUEST_COUNT = 0

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "Hello World!"


def getByte(path):
    with open(path, "rb") as f:
        img_byte = base64.b64encode(f.read())
    img_str = img_byte.decode("ascii")
    return img_str


# api 2 done
@app.get("/get_cls_picture")
async def get_cls_picture(request: Request, id: str):
    if request.method == "GET":
        if id:
            file_path = id + "_result.png"
            if os.path.exists(file_path):
                img_str = getByte(file_path)
                return {
                    "status": "BS.200",
                    "message": "return cls img str",
                    "img": img_str,
                }
            else:
                return {"status": "BS.104", "message": "please wait a few seconds."}

        else:
            return {"status": "BS.102", "message": "please check param."}
    else:
        return {"status": "BS.101", "message": "GET required"}


def getRandomStr():
    return "".join(random.sample(string.ascii_letters + string.digits, 8))


def generateName(isPre):
    date = time.strftime("%Y%m%d", time.localtime())
    extension = ".png"
    p = isPre and "pre" or "post"
    return date + "_" + getRandomStr() + "_" + p + extension


# api 3 done
@app.post("/upload")
async def upload(
    request: Request,
    myFile: UploadFile = File(...),
    type: str = "pre",
    fileName: str = None,
):
    if request.method == "POST":
        if not myFile:
            return {"status": "BS.102", "message": "no file for upload."}

        existName = fileName

        if not existName:
            fileName = generateName(type == "pre")
        elif type == "pre":
            fileName = existName + "_pre.png"
        elif type == "post":
            fileName = existName + "_post.png"

        print(fileName)
        contents = await myFile.read()
        with open(os.path.join(fileName), "wb+") as destination:
            destination.write(contents)

        return {"success": "true", "fileName": fileName}
    else:
        return {"status": "BS.101", "message": "POST required"}


# api 4 done
@app.get("/download")
async def download(request: Request, file_name: str = None):
    if request.method != "GET":
        return {"status": "BS.101", "message": "POST required"}

    if not file_name:
        return {"status": "BS.102", "message": "please enter filename."}

    if not os.path.exists(file_name):
        return {"status": "BS.103", "message": "File not exist!"}

    img = getByte(file_name)

    return {"img": img}


def _read_image_as_array(path, dtype):
    f = Image.open(path)
    try:
        image = np.asarray(f, dtype=dtype)
    finally:
        # Only pillow >= 3.0 has 'close' method
        if hasattr(f, "close"):
            f.close()
    return image


ABS_PATH = "/data1/su/pdd/afastapi/"


def sizefix(img_path_pre: str, img_path_post: str):

    img_pre = Image.open(img_path_pre)
    img_post = Image.open(img_path_post)

    base_img_pre = Image.new("RGB", (1024, 1024), (0, 0, 0))
    base_img_post = Image.new("RGB", (1024, 1024), (0, 0, 0))
    base_img_pre.paste(img_pre, (0, 0) + img_pre.size)
    base_img_post.paste(img_post, (0, 0) + img_post.size)
    base_img_pre.save(img_path_pre.replace("pre", "pre_fixed"))
    base_img_post.save(img_path_post.replace("post", "post_fixed"))
    return img_pre.size[0],img_pre.size[1]


# api 5 done
@app.get("/cls_for_upload")
async def cls_for_upload(pre_file_name: str, post_file_name: str, request: Request):
    global REQUEST_COUNT
    if request.method == "GET":
        key_flag = pre_file_name and post_file_name
        if key_flag:
            if (
                os.path.exists(pre_file_name)
                and os.path.exists(post_file_name)
                and pre_file_name.split(".")[-1] in ["png", "jpg"]
                and post_file_name.split(".")[-1] in ["png", "jpg"]
            ):
                # fixed_size
                height,width = sizefix(pre_file_name, post_file_name)
                img_pre = _read_image_as_array(
                    pre_file_name.replace("pre", "pre_fixed"), np.float32
                )
                img_post = _read_image_as_array(
                    post_file_name.replace("post", "post_fixed"), np.float32
                )

                if (
                    img_pre.shape[0] == img_post.shape[0]
                    and img_pre.shape[1] == img_post.shape[1]
                    and img_pre.shape[2] == img_post.shape[2]
                    and pre_file_name.split(".")[-1] == post_file_name.split(".")[-1]
                ):

                    grpc_client.run2(
                        pre_file_name.replace("pre", "pre_fixed"),
                        post_file_name.replace("post", "post_fixed"), height = height, width = width
                    )
                    if os.path.exists(
                        pre_file_name.replace("pre", "pre_fixed")
                        .split(".")[0]
                        .replace("_pre", "_result")
                        + ".png"
                    ):
                        img = getByte(
                            pre_file_name.replace("pre", "pre_fixed")
                            .split(".")[0]
                            .replace("_pre", "_result")
                            + ".png"
                        )
                        return {
                            "success": "true",
                            "fileName": pre_file_name.replace(
                                "pre", "pre_fixed"
                            ).replace("pre", "result"),
                            "img": img,
                        }
                    else:
                        raise HTTPException(
                            status_code=518,
                            detail="fail to generate result.",
                        )
                else:
                    raise HTTPException(
                        status_code=218,
                        detail="pre_img and post_img's width or height or channel or picture format are not the same.",
                    )
            else:
                raise HTTPException(
                    status_code=103,
                    detail="files not found or picture format is not png or jpg",
                )
        else:
            raise HTTPException(status_code=102, detail="please check param.")
    else:
        raise HTTPException(status_code=101, detail="POST required")


# api 6 done
@app.get("/check_download_result")
async def check_download_result(request: Request, file_name: str):
    if request.method == "GET":
        if file_name:
            if os.path.exists(file_name):
                return {"success": "true", "isFinish": "true"}
            else:
                return {"success": "true", "isFinish": "false"}
        else:
            return {"status": "BS.102", "message": "please check param."}
    else:
        return {"status": "BS.101", "message": "GET required"}
