from django.db import models

# Create your models here.
import login.models


class Prerequisite(models.Model):
    pre_course_id = models.CharField(max_length=15, verbose_name='先修课程代码')

    def __str__(self):
        return self.pre_course_id


class Course(models.Model):
    course_name = models.CharField(max_length=50, verbose_name='课程名称')
    course_id = models.CharField(max_length=15, verbose_name='课程代码', unique=True)
    capacity = models.IntegerField(verbose_name='课程容量')
    faculty = models.CharField(max_length=20, verbose_name="开课学院")
    info = models.CharField(max_length=255, verbose_name="课程介绍", blank=True, default="暂无课程介绍")
    lecturer = models.ForeignKey(login.models.Teacher, on_delete=models.CASCADE, verbose_name="授课教师")
    prerequisite = models.ManyToManyField(Prerequisite, blank=True, verbose_name='先修课程')
    reg_stat = models.ManyToManyField(login.models.Student, through='CourseRegistration')
    stu_score = models.ManyToManyField(login.models.Student, through='StuScore',
                                       related_name="cm_%(class)s_related")

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name_plural = '课程'


class CourseRegistration(models.Model):
    status = (
        ('0', "未中签"),
        ('1', "已中签")
    )

    stu = models.ForeignKey(login.models.Student, on_delete=models.CASCADE, verbose_name='学生')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    is_joined = models.CharField(max_length=1, verbose_name="选课状态", choices=status, default='未中签')

    def __str__(self):
        return self.course.course_name + ' --- ' + self.stu.name

    class Meta:
        verbose_name_plural = '学生选课'


class StuScore(models.Model):
    stu = models.ForeignKey(login.models.Student, on_delete=models.CASCADE, verbose_name='学生')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    score = models.IntegerField(verbose_name="课程成绩")

    def __str__(self):
        return self.course.course_name + ' --- ' + self.stu.name

    class Meta:
        verbose_name_plural = '学生成绩'
