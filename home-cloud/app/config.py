import configparser

def set_settings():
    CONFIG_PATH = "settings.ini"
    section = ['image', 'layout']
    setting = ['upload_quality', 'ip_info', '']
    value = ['50']


    config= configparser.ConfigParser()
    config.read(CONFIG_PATH)
    config.set(f"{section}", f"{setting}", f"{value}")
    cfgfile = open(CONFIG_PATH, 'w')
    config.write(cfgfile)
    cfgfile.close()


def load_settings():
    

    CONFIG_PATH = "settings.ini"  
    config= configparser.ConfigParser()
    config.read(CONFIG_PATH)
    upload_quality = config['image']['upload_quality']
    ip_info = config['layout']['ip_info']
    show_folders = config['layout']['show_folders']

    if upload_quality == '100':
        upload_quality_str = 'Original'
    elif upload_quality == '80':
        upload_quality_str = 'High'
    elif upload_quality == '50':
        upload_quality_str = 'Medium'
    else:
        upload_quality_str = 'Low'


    return upload_quality_str, upload_quality, ip_info, show_folders


def save_settings(section, setting ,value):

    CONFIG_PATH = "settings.ini"  
    config= configparser.ConfigParser()
    config.read(CONFIG_PATH)
    config.set(f"{section}", f"{setting}", f"{value}")
    cfgfile = open(CONFIG_PATH, 'w')
    config.write(cfgfile)
    cfgfile.close()

