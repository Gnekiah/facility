import json, os, time, subprocess


G_HOME_PATH = os.path.join(os.path.expanduser('~'), ".facility")
G_APP_NAME = "facility"
G_CONFIG_FILE = "facility.json"
G_VERSION = "0.0.1"
G_UPDATE_URL = "http://www.xxiong.me/facility/"


def docopy(src_file, dst_file):
    try:
        with open(src_file, "rb") as fr, open(dst_file, 'wb') as fw:
            while True:
                data = fr.read(4096)
                if not data:
                    break
                fw.write(data)
    except:
        return False
    return True


def main():
    config = dict()
    config_path = os.path.join(G_HOME_PATH, G_CONFIG_FILE)
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        return
    origin_path = config["latest_facility"]["path"]
    target_path = config["facility"]["path"]
    ret = docopy(origin_path, target_path)
    if not ret:
        return
    os.system(target_path)
        
    
if __name__ == '__main__':
    for i in range(10):
        time.sleep(1)
        print(i)
    try:
        pid = os.fork()
        if pid == 0:
            time.sleep(10)
            main()
        else:
            time.sleep(2)
            pass
    except Exception as e:
        print(e)
