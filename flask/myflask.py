from flask import Flask  # 첫글자가 대문자인 단어는 클래스

app = Flask(__name__)

@app.route("/")
def home():
  return "<h1>Hello World</h1>"

@app.route("/list1")
def home2():
    return"<h1>리스트 정보는 .... 다음과 같습니다</h1>"

@app.route("/list2")
def home2():
    return"<h1>리스트 정보는 .... 다음과 같습니다</h1>"

@app.route("/list3")
def home2():
    return"<h1>리스트 정보는 .... 다음과 같습니다</h1>"


if __name__ == "__main__":
  app.run()