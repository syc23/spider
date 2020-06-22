import requests
import json
import base64
import simplejson
image1 = './d.jpg'
image2 = './b.jpg'
image = './c.jpg'
def find_face(image_path):
#     print('finding')
    detect_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {
        'api_key':'CNaFPjsTufgl5JkLRjpVvkbQgl3w2Tej',
        'api_secret':'5c5ZXMVhiIQFpJfv8p9eIocoIJe8F4VO',
        'image_url':image_path,
        'return_landmark':1
    }
    files = {'image_file':open(image_path,'rb')}
    req_content = requests.post(detect_url,data=data,files=files).content.decode()
    json_content = simplejson.loads(req_content)['faces'][0]
    position = json_content['face_rectangle']
    face_rectangle =','.join([str(value).strip() for key,value in position.items()])
    return face_rectangle
def merge_face(image1_path,image2_path,image_path,number):
    f1 = find_face(image1_path)
    f2 = find_face(image2_path)
    print(f1,f2)
    merge_url = 'https://api-cn.faceplusplus.com/imagepp/v1/mergeface'
    ff1 = open(image1_path,'rb')
    f1_64 = base64.b64encode(ff1.read()) # 图片进行编码
    ff1.close()
    ff2 = open(image2_path,'rb')
    f2_64 = base64.b64encode(ff2.read()) # 图片进行编码
    ff2.close()
    data = {
        'api_key':'CNaFPjsTufgl5JkLRjpVvkbQgl3w2Tej',
        'api_secret':'5c5ZXMVhiIQFpJfv8p9eIocoIJe8F4VO',
        'template_base64':f1_64,
        'template_rectangle':f1,
        'merge_base64':f2_64,
        'merge_rectangle':f2,
        'merge_rate':number
    }
    req_content = requests.post(merge_url,data=data).content.decode()
    result = simplejson.loads(req_content)['result']
    data = base64.b64decode(result)
    with open(image,'wb') as fp:
        fp.write(data)
    print('换脸完成！')
    
merge_face(image1,image2,image,100)