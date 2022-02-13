import configparser


def load_settings():
    

    CONFIG_PATH = "settings.ini"  
    config= configparser.ConfigParser()
    config.read(CONFIG_PATH)

    upload_quality = config['image']['upload_quality']
    ip_info = config['layout']['ip_info']


    return upload_quality, ip_info


def save_settings(value):

    CONFIG_PATH = "settings.ini"  
    config= configparser.ConfigParser()
    config.read(CONFIG_PATH)
    config.set("image", "upload_quality", f"{value}")
    cfgfile = open(CONFIG_PATH, 'w')
    config.write(cfgfile)
    cfgfile.close()

