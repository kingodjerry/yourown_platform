# flask_login에서 제공하는 사용자 클래스 객체
from flask_login import UserMixin

# DB 연결 정보가 저장되어 있는 config
from app.config import DB

# 쿼리문 실행 함수
from app.model.common.model_db_connect import select, insert, update, delete


# UserMixin 상속하여 flask_login에서 제공하는 기본 함수들 사용
class User(UserMixin):

    # User 객체에 저장할 사용자 정보
    # 그 외의 정보가 필요할 경우 추가한다. (ex. email 등)
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return str(self.user_id)

    # User객체를 생성하지 않아도 사용할 수 있도록 staticmethod로 설정
    # 사용자가 작성한 계정 정보가 맞는지 확인하거나
    # flask_login의 user_loader에서 사용자 정보를 조회할 때 사용한다.
    @staticmethod
    def get_user_info(user_id, user_pw=None):
        result = dict()

        try:
            sql = ""
            sql += f"SELECT USER_ID, USER_NAME, `PASSWORD`, COMPANY_CODE, DEPARTMENT_CODE, POSITION_CODE, AUTH_CODE, "
            sql += f"REGISTER_DATETIME, LOGIN_DATETIME, LASTWEEK_REPORT_ID, THISWEEK_REPORT_ID, "
            sql += f"INSERT_USER_ID, INSERT_DATETIME, UPDATE_USER_ID, UPDATE_DATETIME "
            sql += f"FROM tn_user_info "
            if user_pw:
                sql += f"WHERE USER_ID = '{user_id}' AND `PASSWORD` = '{user_pw}'; "
            else:
                sql += f"WHERE USER_ID = '{user_id}'; "

            result = select(sql)

        except ex:
            result['result'] = 'fail'
            result['data'] = ex
        finally:
            return result