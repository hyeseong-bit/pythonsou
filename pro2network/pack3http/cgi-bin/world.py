import sys
sys.stdout.reconfigure(encoding='utf-8')

s1 = "자료1"
s2 = "두번쨰 자료"

print('Content-Type:text/html; charset=utf-8')

print("""
<html lang="kr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>world</title>
</head>
<body>
    <h1>world 페이지</h1>
    자료 출력 : {0}, {1}
</body>
</html>
    """.format(s1, s2))
