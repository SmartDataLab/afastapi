import requests
from fastapi_server import getByte

# f = {"myFile": open("/data1/su/pdd/afastapi/3_post.png", "rb")}
req = requests.get("http://127.0.0.1:8000/check_download_result?file_name=3_result.png")
print(req.text)
print("api 6 done")

# test for api 5
req = requests.get(
    "http://127.0.0.1:8000/cls_for_upload?pre_file_name=3_pre.png&post_file_name=3_post.png"
)
print(req.text)
print("api 5 done")

with open("3_pre.png", "rb") as f:
    # f = open(".../file.txt", 'rb')
    files = {"myFile": (f.name, f, "multipart/form-data")}
    req = requests.post(
        "http://127.0.0.1:8000/upload",
        data=files,
    )
print(req.text)
print("api 3 done")
