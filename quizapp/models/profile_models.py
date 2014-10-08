from django.db import models
from django.contrib.auth.models import User
from quizapp.models import CommonModel


class UserProfile(models.Model):
    # Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    # The additional attributes.
    website = models.URLField(blank=True)
    # picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username


class Organization(CommonModel):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        app_label = 'quizapp'

    def __unicode__(self):
        return self.name


class Classroom(CommonModel):
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=150)
    teachers = models.ManyToManyField(User, through='ClassroomTeacher',
                                      related_name='classroom_teachers')
    students = models.ManyToManyField(User, through='ClassroomStudent',
                                      related_name='classroom_students')

    class Meta:
        app_label = 'quizapp'
        unique_together = ("organization", "name")

    def __unicode__(self):
        return self.name


class ClassroomTeacher(CommonModel):
    user = models.ForeignKey(User)
    classroom = models.ForeignKey(Classroom)

    class Meta:
        app_label = 'quizapp'


class ClassroomStudent(CommonModel):
    user = models.ForeignKey(User)
    classroom = models.ForeignKey(Classroom)

    class Meta:
        app_label = 'quizapp'


__all__ = ['UserProfile',
           'Organization',
           'Classroom',
           'ClassroomTeacher',
           'ClassroomStudent',
           ]