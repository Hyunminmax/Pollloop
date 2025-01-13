from multiprocessing import context
import boto3
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import InputFileSerializer
from rest_framework import status
from dotenv import dotenv_values

def upload_file(s3_client, bucket_name, region_name, input_source, S3_key, file):
    # 버킷에 해당 폴더가 있는지 확인
    if not prefix_exists(s3_client, bucket_name, input_source):
        # 해당 폴더가 없으면 생성
        s3_client.put_object(Bucket=bucket_name, Key=f"{input_source}/")
    
    # S3에 파일 업로드
    s3_client.put_object(
        Bucket=bucket_name,      # S3 버킷 이름
        Key=S3_key,     # S3에 저장될 파일 이름
        Body=file.read(),
    )
    # 반환용 S3 URL 생성
    file_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{S3_key}"

    return file_url

def prefix_exists(s3_client, bucket_name, prefix):
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

class InputFile(APIView):
# 파일 입력의 총 3가지 경로
    # 사용자 2
        # 프로필 inputfile/profile/user_uuid*/file*
        # 폼에 넣은 파일 inputfile/form_answer/form_uuid*/question*/option_number*/user_uuid*/file
    # 폼 1
        # 폼의 보기 inputfile/form/form_uuid*/question_order*/option_number*/file
    @extend_schema(
            summary="파일 S3에 저장",
            description="""S3에 파일 저장 후 URL 반환 \n
Multipart/form-data의 경우 예제 선택이 되지 않음. \n
1. 사용자 프로필 수정\n
    inputsorce: profile\n
    file: file\n
2. 폼에 파일 제출\n
    inputsorce: form_answer\n
    form_uuid: 2bd64b2e1364441b9840020039906fe4\n
    question_id: 10\n
    option_number: 1\n
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
            }
    )

    def post(self, request):
        serializer = InputFileSerializer(data=request.data, context={'request':request})

        if serializer.is_valid():
            # 필수 입력값
            input_source = serializer.validated_data['input_source']
            file = serializer.validated_data['file']
            user = str(request.user.uuid)
            # 조건부 입력값
            # user = serializer.validated_data['user']
            # form = serializer.validated_data['form']
            # question = serializer.validated_data['question']
            # option = serializer.validated_data['option']

            region_name = settings.S3_REGION_NAME
            bucket_name = settings.S3_STORAGE_BUCKET_NAME
            S3_key = ''

            # S3 초기화
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.S3_ACCESS_KEY,
                aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
                region_name=region_name,
            )

            if input_source == 'profile': # 프로필 저장
                S3_key = input_source+'/'+user+'/'+file.name
                file_url = upload_file(s3_client, bucket_name, region_name, input_source, S3_key, file)
                
            elif input_source == 'form_answer': # 폼 파일제출 저장
                form = serializer.validated_data['form']
                question = serializer.validated_data['question']
                option = serializer.validated_data['option']
                S3_key = input_source+'/'+str(form)+'/'+str(question)+'/'+str(option)+'/'+user+'/'+file.name
                file_url = upload_file(s3_client, bucket_name, region_name, input_source, S3_key, file)
            
            elif input_source == 'form': # 폼 보기 저장
                form = serializer.validated_data['form']
                question = serializer.validated_data['question']
                option = serializer.validated_data['option']
                S3_key = input_source+'/'+str(form)+'/'+str(question)+'/'+str(option)+'/'+file.name
                file_url = upload_file(s3_client, bucket_name, region_name, input_source, S3_key, file)

            # # 저장 후 응답
            return Response({
                'message': '파일 업로드 성공',
                'file_name': file.name,
                'file_size': file.size,
                'input_source': input_source,
                'file_url': file_url,
            }, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)  # 검증 실패 시 에러 출력
            return Response(serializer.errors, status=400)            