################################################################
############## 文本翻译自动识别语种接口 正向用例集成测试 ##############
################################################################

# 邮箱登录
POST http://47.245.55.239:30013/lvtrans/user/auth/loginByEmail
{
    "email": "1219118137@qq.com",
    "password": "123456"
}
HTTP 200
[Asserts]
header "Authorization" not isEmpty
header "Refreshtoken" not isEmpty
jsonpath "$.code" == 200
jsonpath "$.data.email" == "1219118137@qq.com"
[Captures]
token: header "Authorization"
