import requests

# f = {"myFile": open("/data1/su/pdd/afastapi/3_post.png", "rb")}
req = requests.get("http://127.0.0.1:8000/check_download_result?file_name=3_result.png")
print(req.text)
# TODO(pandi): decode into picture format and save it


# NOTE(pandi): previous api code(django): /data1/su/app/xview2/xviewapi/xviewapi/views.py
