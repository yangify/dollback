# CELERY
CELERY_BROKER_URL = 'amqp://localhost:5672'

# DECOMPILER
DECOMPILERS = ['apktool', 'jadx']

APK_FOLDER_PATH = './resources/apk'
SOURCE_CODE_FOLDER_PATH = './resources/code'
LINK_FOLDER_PATH = './resources/link'

APKTOOL_COMMAND = 'java -jar ./tools/decompiler/apktool/apktool.jar d <INPUT_PATH> -o <OUTPUT_PATH>'
JADX_COMMAND = './tools/decompiler/jadx/bin/jadx -d <OUTPUT_PATH> <INPUT_PATH>'

# DATABASE
MONGO_URI = 'mongodb://localhost:27017/dollback'

# CODECOMMIT
CODECOMMIT_USERNAME = 'admin-at-496345044153'
CODECOMMIT_PASSWORD = 'yPuH144HJh5LZgw401cB4Jt+esb5pSkoTWNnj11NWQw='
CREATE_REPOSITORY_CMD = 'aws codecommit create-repository --repository-name {repository_name}'
CLONE_REPOSITORY_CMD = 'git clone https://{username}:{password}@git-codecommit.ap-southeast-1.amazonaws.com/v1/repOs' \
                       '/{repository_name} '
