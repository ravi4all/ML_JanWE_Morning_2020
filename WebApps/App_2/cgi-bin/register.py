import cgi

form = cgi.FieldStorage()

name = form.getvalue('u_name')
email = form.getvalue('u_mail')
pwd = form.getvalue('u_pwd')

print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

    <h1>Hello {}</h1>

</body>
</html>
""".format(name))