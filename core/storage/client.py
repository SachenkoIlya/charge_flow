from botocore.config import Config
from io import BytesIO
import aioboto3
import aiohttp
import pandas as pd
from core.logger.logger import logger
from core.security.settings import settings


class S3Client:
    def __init__(self):
        self.access_key = settings.S3_ACCESS_KEY
        self.secret_key = settings.S3_SECRET_KEY
        self.bucket_name = settings.S3_BUCKET
        self.endpoint_url = settings.S3_ENDPOINT
        self.config = Config(signature_version="s3v4")
    
    
    # @BaseDB.with_retries(retries=5, delay=1.5, msg_prefix="[s3 upload]")
    async def upload_parquet_and_get_url(
        self,
        user_id: int,
        type_method: str,
        run_id: str,
        df: pd.DataFrame,
        expire: int = 3600
    ) -> str:
        """
        Преобразует DataFrame в Parquet, заливает в S3 и возвращает presigned URL.
        """
        size_df = df.memory_usage(deep=True).sum() / 1024**2
        
        if df.shape[0] == 0 or df.shape[1] == 0:
            return None, None, None, None
        
        # 1. Преобразуем DataFrame в Parquet (в память)
        buffer = BytesIO()
        df.to_parquet(buffer, index=False, engine="pyarrow")
        buffer.seek(0)

        size_parquet = len(buffer.getvalue()) / 1024

        if size_parquet == 0 or size_df == 0:
            compression = 0
        else:
            compression = (1 - size_parquet/float(size_df)/1024)*100
        
        # 2. Формируем ключ
        key = f"charge_flow/{type_method}/{user_id}/{run_id}.parquet"

        # 3. Загружаем в S3
        session = aioboto3.Session()
        async with session.client(
            "s3",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.endpoint_url,
            config=self.config,
        ) as s3:
            await s3.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=buffer.getvalue()
            )

        return key, compression, size_parquet
    
    


    async def download_parquet_from_s3(self, url:str):
        """
        Загружает parquet-файл из S3 по URL и возвращает pandas.DataFrame.
        """
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as resp:
                data = await resp.read()
            return pd.read_parquet(BytesIO(data))
        

    
    async def download_parquet_s3_from_key(self, bucket:str, key:str):
        sess = aioboto3.Session()
        try:
            async with sess.client(
                "s3",
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                endpoint_url=self.endpoint_url,
                config=self.config,
            ) as s3:
                obj = await s3.get_object(Bucket=bucket, Key=key)
                data = await obj['Body'].read()
                df = pd.read_parquet(BytesIO(data))
                logger.info(f"✅ Успешно загружен parquet строк({df.shape[0]}), столбцов({df.shape[1]})")
                return df
        except Exception as e:
            logger.error(f"❌ Ошибка при чтении parquet из S3 по ключу {key}: {e}")
            return None