import cgi
import prediction

form = cgi.FieldStorage()
review = form.getvalue('msg')
pred = prediction.testReview(review)

print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Your prediction is : {}</h1>
</body>
</html>
""".format(pred[0]))
