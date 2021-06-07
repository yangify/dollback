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

# GIT
COMMIT = 'cd resources/code/{filename}; git init; git add .; git commit -m "first commit"'

# SOURCEGRAPH
SOURCEGRAPH_URL = 'http://localhost:7080'
SOURCEGRAPH_API = '/.api/graphql'
SOURCEGRAPH_TOKEN = 'REDACTED'
SOURCEGRAPH_LOCALHOST = 'RXh0ZXJuYWxTZXJ2aWNlOjk='
SOURCEGRAPH_UPDATE_HOST_QUERY = 'mutation UpdateExternalService($input: UpdateExternalServiceInput = {id: \"{' \
                                'host_id}\"}) { updateExternalService(input: $input) { id, displayName } }'
SOURCEGRAPH_SEARCH_URL = 'query { '\
                         '  search ( query: \"repo:^<REPO_NAME>$ (http|ftp|https)://([\\\\w_-]+(?:(?:\\\\.[\\\\w_-]+)+))([\\\\w.,@?^=%&:/~+#-]*[\\\\w@?^=%&/~+#-])? count:all\" patternType: regexp ) { '\
                         '      results { '\
                         '          matchCount '\
                         '          results { ...result } '\
                         '      } '\
                         '  } '\
                         '} '\
                         'fragment result on FileMatch { '\
                         '  file { path name } '\
                         '  lineMatches { offsetAndLengths preview } '\
                         '}'\
