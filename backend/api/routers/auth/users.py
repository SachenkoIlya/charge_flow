
from core.base_db import Base


class Users:
    def __init__(self, base_db: "Base"):
        self.db = base_db


    @Base.with_retries(retries=3, delay=1.5,  msg_prefix='[UsersDb.create_users]')
    async def create_user(
        self, 
        full_name: str, 
        email:str, 
        hash_password: str, 
        company:str, 
        phone: str, 
        country: str
    ):
        """
        Создаёт нового пользователя в базе данных.

        Выполняет INSERT-запрос в таблицу users_new и возвращает ID
        созданной записи.

        :param full_name: Полное имя пользователя (будет приведено к Title Case)
        :param email: Email пользователя (очищается от пробелов и приводится к нижнему регистру)
        :param hash_password: Хэш пароля пользователя
        :param company: Название компании пользователя
        :param phone: Номер телефона пользователя
        :param country: Страна пользователя

        :return: Запись с полем ID созданного пользователя (Record)
        """
        
        q = """
            INSERT INTO users_new(
                full_name, 
                email, 
                hash_password, 
                company, 
                phone, 
                country
            )
            VALUES(
                $1, $2, $3, $4, $5, $6
            )
            RETURNING ID
            """
        
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
                q,
                full_name.title(), 
                email.strip().lower(), 
                hash_password, 
                company, 
                phone, 
                country
            )

         
    @Base.with_retries(retries=3, delay=1.5,  msg_prefix='[UsersDb.check_login]')
    async def check_login(self, email:str):
        """ 
        Получение пользователя по email из базы данных.

        Выполняет SQL-запрос для поиска пользователя в таблице users_new.
        Используется в процессе аутентификации (логина).

        Args:
            email (str): Email пользователя

        Returns:
            asyncpg.Record | None:
                - Если пользователь найден:
                    {
                        "id": int,
                        "full_name": str,
                        "hash_password": str,
                        "email": str,
                        "role": str
                    }
                - Если пользователь не найден:
                    None
        """
   
        q = """
            SELECT 
                id, full_name, hash_password, email, role 
            FROM users_new
            WHERE email = $1
            """
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
                q,
                email
            )

           