import pymysql


class DatabaseManager:
    def __init__(self, host='localhost', user='root', password='password', database='password_db'):
        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4'
        }
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """连接到MySQL数据库"""
        try:
            self.conn = pymysql.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            self.init_table()
            print("数据库连接成功")
            return True
        except pymysql.Error as e:
            print(f"数据库连接失败: {e}")
            return False

    def init_table(self):
        """初始化密码表"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INT AUTO_INCREMENT PRIMARY KEY,  
                    password VARCHAR(255) NOT NULL,
                    length INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
        except pymysql.Error as e:
            print(f"初始化表失败: {e}")

    def save_password(self, password, length):
        """保存数据库"""
        try:
            self.cursor.execute(
                "INSERT INTO passwords (password, length) VALUES (%s, %s)",
                (password, length)
            )
            self.conn.commit()
        except pymysql.Error as e:
            print(f"❌ 保存密码失败: {e}")


database=DatabaseManager('localhost', 'root', '123456', 'password_db')
