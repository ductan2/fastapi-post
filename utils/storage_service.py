from fastapi import UploadFile, File
from fastapi import APIRouter
import boto3
from decouple import config
import uuid

router = APIRouter()

ACCESS_KEY_ID = config('ACCESS_KEY_ID')
ACCESS_SECRET_KEY = config('ACCESS_SECRET_KEY')
BUCKET_NAME = config('BUCKET_NAME')
s3 = boto3.client('s3',
                  aws_access_key_id=ACCESS_KEY_ID,
                  aws_secret_access_key=ACCESS_SECRET_KEY,
                  region_name='ap-southeast-1'
                  )


async def getAllFile():
    res = s3.list_objects_v2(Bucket=BUCKET_NAME)
    print(res)
    return res


def get_link_file(file_key):
    print(file_key)
    return s3.generate_presigned_url('get_object',
                                     Params={'Bucket': BUCKET_NAME, 'Key': file_key}, ExpiresIn=3600)


def delete_file(file_key):
    s3.delete_object(Bucket=BUCKET_NAME, Key=file_key)


async def get_link_all_file():
    res = s3.list_objects_v2(Bucket=BUCKET_NAME)
    url = []

    for i in res['Contents']:
        print(i['Key'])
        url.append(
            s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': i['Key']}, ExpiresIn=3600))
    return url


# Cách tạo presignUrl trên s3
# # Tên của tệp trên Amazon S3
# file_key = 'Google - Original.png'
#
# # Tạo URL có thời hạn cho tệp
# url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_key}, ExpiresIn=3600)
#
# print("URL của tệp là:", url)
def upload_file(file: UploadFile = File(...)) -> str:
    print(file.filename)
    # Tạo một UUID duy nhất cho tên tệp
    unique_filename = f"{file.filename}-{uuid.uuid4()}"
    # Đọc dữ liệu của file và gửi nó lên S3
    print(unique_filename)
    s3.upload_fileobj(file.file, BUCKET_NAME, unique_filename)

    return unique_filename
