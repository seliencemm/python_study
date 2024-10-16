################################################################
############## 文本翻译自动识别语种接口 正向用例集成测试 ##############
################################################################

# 邮箱登录
POST {{live_translator_login_host}}/lvtrans/user/auth/loginByEmail
{
    "email": "{{email}}",
    "password": "{{password}}"
}
HTTP 200
[Asserts]
header "Authorization" not isEmpty
header "Refreshtoken" not isEmpty
jsonpath "$.code" == 200
jsonpath "$.data.email" == "{{email}}"
[Captures]
token: header "Authorization"

# 文本翻译自动识别语种接口，指定源语言 传所有参数
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "hello world",
    "from": "en-US",
    "to": "zh-CN"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" isEmpty
jsonpath "$.data.translate_text" == "你好，世界"

# 文本翻译自动识别语种接口 Request Headers: X-Platform传timekettle
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: timekettle
{
    "content": "hello world",
    "from": "en-US",
    "to": "zh-CN"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" isEmpty
jsonpath "$.data.translate_text" == "你好，世界"

# 文本翻译自动识别语种接口，自动检测源语言 Request Body: 不传from
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "hello world",
    "to": "zh-CN"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" matches /en-/
jsonpath "$.data.translate_text" == "你好，世界"

# 文本翻译自动识别语种接口，自动检测源语言 Request Body: content传短文本
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "你",
    "to": "en-US"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" matches /zh-/
jsonpath "$.data.translate_text" == "You"

# 文本翻译自动识别语种接口，自动检测源语言 Request Body: content传长文本
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "{{content_long}}",
    "to": "en-US"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" == "zh-CN"
jsonpath "$.data.translate_text" matches /ShenZhen|hometown/

# 文本翻译自动识别语种接口，自动检测源语言 Request Body: content传纯特殊符号
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "$#%^&<@!*",
    "to": "en-US"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"

# 文本翻译自动识别语种接口，自动检测源语言 Request Body: content传emoji表情符号
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "😊😊😊😊😊😊",
    "to": "en-US"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"

# 文本翻译自动识别语种接口，自动检测源语言 Request Body: content传正常字符、特殊字符、emoji的组合文本
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "@#&你好，@#￥%&*我喜欢吃鱼😊😊😊😊😊😊",
    "to": "en-US"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" == "zh-CN"
jsonpath "$.data.translate_text" matches /hello|like|eat|fish/

# 文本翻译自动识别语种接口，指定源语言 Request Body: content传与from不一致的语言文本
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "こんにちは、初めまして、どうぞよろしくお願いします。",
    "from": "en-US",
    "to": "zh-CN"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" isEmpty
jsonpath "$.data.translate_text" matches /你好|关照|认识|初次见面/

# 文本翻译自动识别语种接口 自动检测语种， Request Body: content传与to一致的语言文本
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "你好，我喜欢吃鱼。",
    "to": "zh-CN"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" == "zh-CN"
jsonpath "$.data.translate_text" == "你好，我喜欢吃鱼。"

# 文本翻译自动识别语种接口 指定源语言， Request Body: content传与to一致的语言文本
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "你好，我喜欢吃鱼。",
    "from": "en-US",
    "to": "zh-CN"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" isEmpty
jsonpath "$.data.translate_text" == "你好，我喜欢吃鱼。"

# 文本翻译自动识别语种接口 Request Body: from传空值
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "你好，我喜欢吃鱼。",
    "from": "",
    "to": "en-US"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" == "zh-CN"
jsonpath "$.data.translate_text" matches /hello|like|eat|fish/

# 文本翻译自动识别语种接口 Request Body: from传null
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "你好，我喜欢吃鱼。",
    "from": null,
    "to": "en-US"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" == "zh-CN"
jsonpath "$.data.translate_text" matches /hello|like|eat|fish/

# 文本翻译自动识别语种接口 Request Body: to传非法的语言code
POST {{live_translator_host}}/livetranslator/translate/text
Authorization: Bearer {{token}}
X-Platform: livetranslator
{
    "content": "你好，我喜欢吃鱼。",
    "to": "ab-CD"
}
HTTP 200
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" == "zh-CN"
jsonpath "$.data.translate_text" not isEmpty
