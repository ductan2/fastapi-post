from fastapi import UploadFile, File
from fastapi import APIRouter
import boto3
from decouple import config

router = APIRouter()

ACCESS_KEY_ID = config('ACCESS_KEY_ID')
ACCESS_SECRET_KEY = config('ACCESS_SECRET_KEY')
s3 = boto3.client('s3',
                  aws_access_key_id=ACCESS_KEY_ID,
                  aws_secret_access_key=ACCESS_SECRET_KEY,
                  )

BUCKET_NAME = 's3-nguyenductan'


@router.get("/")
def read_root():
    return {"name": "aniket", "age": 24}


@router.get("/getallfiles")
async def hello():
    res = s3.list_objects_v2(Bucket=BUCKET_NAME)
    print(res)
    return res
# Cách tạo presignUrl trên s3
# # Tên của tệp trên Amazon S3
# file_key = 'Google - Original.png'
#
# # Tạo URL có thời hạn cho tệp
# url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_key}, ExpiresIn=3600)
#
# print("URL của tệp là:", url)
@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    if file:
        print(file.filename)
        s3.upload_fileobj(file.file, BUCKET_NAME, file.filename)
        return "file uploaded"
    else:
        return "error in uploading."

