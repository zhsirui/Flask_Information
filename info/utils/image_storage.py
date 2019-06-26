from qiniu import Auth, put_data

access_key = "5z6nqNjTuE18BOsd9pi7ojZzcNVkZeWdEZ6CVddy"
secret_key = "TZVkycG5_UbPAqVLB2uGZFRll35YA4eDwDdU9Gxl"
bucket_name = "home"

def storage(data):

    try:
        q = Auth(access_key, secret_key)
        token = q.upload_token(bucket_name)
        ret, info = put_data(token, None, data)
        print(ret, info)
    except Exception as e:
        raise e

    if info.status_code != 200:
        raise Exception("上传失败")

    return ret["key"]