from django.db import models

class Post(models.Model):
    postname = models.CharField(max_length=50)
    # 게시글 Post에 이미지 추가
    contents = models.TextField()
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    # postname이 Post object 대신 나오기
    def __str__(self):
        return self.postname