from django.db import models

# Create your models here.
# 테이블명 : Post
# 컬럼 :
    # title char max_length 30
    # content  textfield
    # created_at  datetime

class Post(models.Model):
    title = models. CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    def __str__(self): # 객체 자체를 출력하면 호출되는 클래스
        return f"{self.pk} : {self.title}"