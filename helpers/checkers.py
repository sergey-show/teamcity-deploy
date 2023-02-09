from datetime import datetime,timedelta

class ProdTime(object):

    def __init__(self, env = "DEV"):
        """Constructor"""
        self.env = env

    def timeValidate(self,valid=False):
        """
        Checker for allow time for running build on production 
        This checker get time in UTC and make timedelta +3 hours to current time, then check maintenance window for deploy of 20.00-23.00
        If time allow in production maintenance window, method return True if not allowed return False
        For another env`s method return True
        """
        now = datetime.utcnow()
        start_time = now.replace(hour=20, minute=0, second=0, microsecond=0)
        end_time = now.replace(hour=23, minute=0, second=0, microsecond=0)
        Msk = now + timedelta(hours=3)
        if self.env in ("PROD"):
            if (Msk > start_time) and ( Msk < end_time):
                valid = True
        else:
            valid = True
        return valid
