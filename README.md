# fastapi for abd

## quick start

```
cd /data1/su/haoyu/building_damage_kd
python grpc_server.py
uvicorn fastapi_server:app --host 0.0.0.0
python fastapi_client.py
```

## 接口规范说明

## AI 图像处理接口

- 1 图像分类接口  
   **名称：** get_sub_picture
  **类型：** post
  **参数：**
  |参数|类型|是否必填|说明|示例|
  |--|--|--|--|--|
  id|number|是|裁剪的图形编号|默认 1
  x|number|是|裁剪图像时的左上角坐标||
  y|number|是|裁剪图像时的左上角坐标||
  width|number|是|裁剪的宽度，单位像素||
  height|number|是|裁剪的宽度，单位像素||
  返回结果：裁剪后的图片地址、id
  ```
  {
     success:true,
     data:{
         id:'xxx'    // 任务id
         pre_cut:'xxx' //裁剪的灾前图片 base64字符串
         post_cut:'xxx'  //裁剪的在后图片 base64字符串
     }
  }
  ```
- 2 获取分类结果接口  
   **名称：** get_cls_picture  
   **类型：** get
  **参数：**  
   |参数|类型|是否必填|说明|示例|
  |--|--|--|--|--|
  id|string|是|任务 id||
  **返回结果：**
  ```
  {
     success:true,
     data:{
         img:'xxx'    // 结果图片
     }
  }
  ```
- 3 上传接口  
   **名称：** upload  
   **类型：** post  
   **参数：**  
   |参数|类型|是否必填|说明|示例|
  |--|--|--|--|--|
  file|string|必填|文件名|
  type|string|可选|pre/post,默认是 pre|
  fileName|string|可选|已上传的文件名|

  **返回结果：**

  ```
  {
      success:true,
      data:{
          fileName,//上传后的文件名
      }
  }
  文件名：灾前  20200823_xxxx_pre.jpg
         在后  20200823_xxxx_post.jpg
  ```

- 4 下载接口  
   **名称：** download  
   **类型：** get  
   **参数：**
  |参数名|类型|是否必填|说明|示例|
  |--|--|--|--|--|
  fileName|string|必填|文件名|20200823_xxxx_result.jpg
  **返回结果：** 文件

- 5 进行灾害图像处理  
   **名称:** cls_for_upload
  **类型:** post  
   **参数:**
  |参数名|类型|是否必填|说明|示例|
  |--|--|--|--|--|
  preName|string|必填|灾前文件名，文件类型为 jpg、png|20200823_xxxx_pre.jpg
  postName|string|必填|在后文件名，文件类型为 jpg、png|20200823_xxxx_post.jpg
  **返回结果:**

  ```
  {
      success:true,
      data:{
          fileName:xxx  //处理完成后的文件名,根据输入的preName生成，文件类型固定为jpg，如： 20200823_xxxx_result.jpg
      }
  }
  ```

- 6 图像处理是否完成  
   **名称:** check_download_result
  **类型:** get  
   **参数:**
  |参数名|类型|是否必填|说明|示例|
  |--|--|--|--|--|
  fileName|string|必填|文件名|20200823_xxxx_result.jpg

  **返回结果:**

  ````
    {
        success:true,
        data:{
            isFinish:false/true
        }
    }
    ```
  ````
