import boto3
from django.conf import settings
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.views import APIView
class InputImage(APIView):

    def post(self, request):
        # 이미지 업로드를 호출하는 위치
        input_source = request.data.get("input_source")
        # 이미지들
        images = request.FILES.getlist("images")

        # S3 초기화
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        # 버킷 이름
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME

        uploaded_url = []

        try:
            # 버킷에 해당 폴더가 있는지 확인
            if not self.prefix_exists(s3_client, bucket_name, input_source):
                # 해당 폴더가 없으면 생성
                s3_client.put_object(Bucket=bucket_name, Key=f"{input_source}/")

            for image in images:
                # 파일 이름, 확장자 분리
                image_fullname = image.name
                name_parts = image.name.split(".")
                if len(name_parts) > 1:
                    image_extension = name_parts[-1]
                    image_name = ".".join(name_parts[:-1])
                else:
                    image_extension = ""
                    image_name = image_fullname

                # 파일명에 특수문자나 공백을 '-'로 변경
                if image_extension:
                    new_name = slugify(image_name) + "." + image_extension
                else:
                    new_name = slugify(image_name)

                # 이미지 업로드
                s3_client.upload_fileobj(
                    image, bucket_name, input_source + "/" + new_name
                )

                # 업로드된 파일 URL 생성
                image_url = f"https://s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{bucket_name}/{input_source}/{new_name}"
                uploaded_url.append(image_url)

            return Response({"images_urls": uploaded_url})

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def prefix_exists(self, s3_client, bucket_name, prefix):
        # 폴더(프리픽스) 존재 여부 확인
        try:
            response = s3_client.list_objects_v2(
                Bucket=bucket_name, Prefix=prefix, MaxKeys=1
            )
            # Contents는 aws에서 사용하는 key값
            if "Contents" in response:
                return True
            else:
                return False
        except Exception as e:
            print(f"오류 발생: {str(e)}")
            return False