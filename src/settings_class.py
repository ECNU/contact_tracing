import settings


class SettingsObject():
    def __init__(self):
        ### 集成配置
        for k in dir(settings):
            v = getattr(settings,k)
            setattr(self,k,v)


settings_obj = SettingsObject()