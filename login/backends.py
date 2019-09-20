from .models import Users
import logging

class AuthBackend(object):
    def authenticate(self,name,institution_id,password):
        try:
            user = Users.objects.get(name=name,institution_id=institution_id,password=password)
            if user.check_password(password):
                return user
            else:
                return None

        except Users.DoesNotExist:
            return logging.getLogger("error_logger").error("user with login %s does not exists " % login)

        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def get_user(self,name):
        try:
            user = Users.objects.get(name=name)
            if user.is_active:
                return user
            else:
                return None
        except Users.DoesNotExist:
            logging.getLogger("error_logger").error("user with username %s does not exist" % name)

