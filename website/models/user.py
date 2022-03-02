from website.db import queries
from website.utils import security


class User:
    def __init__(self, user_id):
        user_data = queries.get_user(user_id)

        self.anonymous = not user_data
        self.active = False
        if user_data:
            self.user_id = user_data['user_id']
            self.email = security.decrypt_data(user_data['email'])
            self.password = user_data['password']
            self.email_confirmed = user_data['email_confirmed']
            if self.email_confirmed:
                self.active = True
            self.register_date = user_data['register_date']
            self.deletion_date = user_data['deletion_date']
            self.authenticated = False

    def authenticate(self, password):
        self.authenticated = queries.verify_password(self.user_id, password, security.verify_password)
        return self.authenticated

    def activate(self, address):
        if address == self.email:
            queries.confirm_email(self.user_id)
            return True
        else:
            return False

    @classmethod
    def get_user(cls, user_id):
        return cls(user_id)

    @classmethod
    def from_mail(cls, email):
        cls(queries.get_user_by_mail('token_confirmation', email, security.encrypt_data))

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return self.anonymous

    def get_id(self):
        return self.user_id
