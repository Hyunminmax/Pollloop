import boto3
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import InputFileSerializer
from rest_framework import status
from dotenv import dotenv_values



class InputFile(APIView):
# 파일 입력의 총 3가지 경로
    # 사용자 2
        # 프로필 inputfile/profile/user_uuid*/file*
        # 폼에 넣은 파일 inputfile/form/form_uuid*/question*/option_number*/user_uuid*/file
    # 폼 1
        # 폼의 보기 inputfile/form/form_uuid*/question_order*/option_number*/file
    @extend_schema(
            summary="파일 S3에 저장",
            description="""S3에 파일 저장 후 URL 반환 \n
Multipart/form-data의 경우 예제 선택이 되지 않음. \n
1. 사용자 프로필 수정\n
    inputsorce: profile\n
    user_uuid: feb3e9a66abf4fcfa5a841eed8bca466\n
    file: file\n
2. 폼에 파일 제출\n
    inputsorce: form\n
    form_uuid: 2bd64b2e1364441b9840020039906fe4\n
    question_id: 10\n
    option_number: 1\n
    user_uuid: feb3e9a66abf4fcfa5a841eed8bca466\n
    file: file\n
3. 폼 예제에 이미지 등록\n
    inputsorce: form\n
    form_uuid: 2bd64b2e1364441b9840020039906fe4\n
    question_order: 9\n
    option_number: 1\n
    file: file\n
    """,
            request={
                "multipart/form-data": InputFileSerializer,  # Content-Type 명시
            },
            responses={
                200: OpenApiResponse(
                    response={
                        "uuid": "2bd64b2e1364441b9840020039906fe4",
                        "user": 1,
                    },
                    description="S3 URL이 성공적으로 반환된 경우",
                ),
                400: "잘못된 요청 데이터",
                404: "폼을 찾을 수 없음",
            },
    )

    def post(self, request):
        serializer = InputFileSerializer(data=request.data)

        if serializer.is_valid():
            # 필수 입력값
            input_source = serializer.validated_data['input_source']
            file = serializer.validated_data['file']
            # 조건부 입력값
            # user = serializer.validated_data['user']
            # form = serializer.validated_data['form']
            # question = serializer.validated_data['question']
            # option = serializer.validated_data['option']

            # S3 초기화
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.S3_ACCESS_KEY,
                aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
                region_name=settings.S3_REGION_NAME,
            )

            if input_source == 'profile': # 프로필 저장
                user = serializer.validated_data['user']

                # 버킷에 해당 폴더가 있는지 확인
                if not self.prefix_exists(s3_client, bucket_name, input_source):
                    # 해당 폴더가 없으면 생성
                    s3_client.put_object(Bucket=bucket_name, Key=f"{input_source}/")
                
                # S3에 파일 업로드
                response = s3_client.upload_file(
                    Filename=file.name,  # 로컬 파일 경로
                    Bucket=settings.S3_STORAGE_BUCKET_NAME,      # S3 버킷 이름
                    Key=input_source+'/'+str(user)+'/'+file.name     # S3에 저장될 파일 이름
                )
                
            # # S3 버킷의 파일 목록 가져오기
            response = s3_client.list_objects_v2(Bucket=settings.S3_STORAGE_BUCKET_NAME)

            for obj in response.get('Contents', []):
                print(f"File Name: {obj['Key']} | Size: {obj['Size']} bytes")
            
            
            # 파일 저장 로직 (예: 로컬 저장 또는 S3 업로드)
            file_name = file.name
            file_size = file.size
            # # 저장 후 응답
            return Response({
                "message": "파일 업로드 성공",
                "file_name": file_name,
                "file_size": file_size,
                "input_source": input_source,
            }, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)  # 검증 실패 시 에러 출력
            return Response(serializer.errors, status=400)            

    
    # def post(self, request):
    #     # 이미지 업로드를 호출하는 위치
    #     input_source = request.data.get("input_source")
    #     # 이미지들
    #     file = request.FILES.getlist("images")

    #     # S3 초기화
    #     s3_client = boto3.client(
    #         "s3",
    #         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    #         region_name=settings.AWS_S3_REGION_NAME,
    #     )
    #     # 버킷 이름
    #     bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    #     uploaded_url = []

    #     try:
    #         # 버킷에 해당 폴더가 있는지 확인
    #         if not self.prefix_exists(s3_client, bucket_name, input_source):
    #             # 해당 폴더가 없으면 생성
    #             s3_client.put_object(Bucket=bucket_name, Key=f"{input_source}/")

    #         for image in images:
    #             # 파일 이름, 확장자 분리
    #             image_fullname = image.name
    #             name_parts = image.name.split(".")
    #             if len(name_parts) > 1:
    #                 image_extension = name_parts[-1]
    #                 image_name = ".".join(name_parts[:-1])
    #             else:
    #                 image_extension = ""
    #                 image_name = image_fullname

    #             # 파일명에 특수문자나 공백을 '-'로 변경
    #             if image_extension:
    #                 new_name = slugify(image_name) + "." + image_extension
    #             else:
    #                 new_name = slugify(image_name)

    #             # 이미지 업로드
    #             s3_client.upload_fileobj(
    #                 image, bucket_name, input_source + "/" + new_name
    #             )

    #             # 업로드된 파일 URL 생성
    #             image_url = f"https://s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{bucket_name}/{input_source}/{new_name}"
    #             uploaded_url.append(image_url)

    #         return Response({"images_urls": uploaded_url})

    #     except Exception as e:
    #         return Response({"error": str(e)}, status=500)

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