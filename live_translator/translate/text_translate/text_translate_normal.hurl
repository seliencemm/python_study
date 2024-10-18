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
HTTP 400
[Asserts]
jsonpath "$.code" == 0
jsonpath "$.message" == "Success"
jsonpath "$.data.detect_language" isEmpty
jsonpath "$.data.translate_text" == "你好，世界"
