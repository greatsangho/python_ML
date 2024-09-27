# 모듈에서 제공하고 싶은 함수를 생성
# 상수는 대문자로 나타냄
PI = 3.1415
# 원의 넓이
def getArea(radius):
    return PI*radius*2

# 제공하려는 함수를 검증하기 위해서
if __name__ == '__main__': # 자기 자신이 실행된다면
    radius = 2
    print(f'만지름이 2일 때 원의 넓이 : {getArea(2)}')