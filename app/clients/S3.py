from app import application
from app.settings import AWS_BUCKET


class S3Client:
    async def send_file(self, b_file, file_name):
        async with application.botocore_client as client:
            esp = await client.put_object(Body=b_file,
                                          Bucket=AWS_BUCKET,
                                          Key=file_name)
        return esp
