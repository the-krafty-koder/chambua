from djongo import models
from picklefield.fields import PickledObjectField

# Create your models here
class CustomExam(models.Model):
    exam_name = models.CharField(max_length=50)
    results = PickledObjectField(default="Null", null=True)

    def __str__(self):
        return self.exam_name

class Exam(models.Model):
    exam_name = models.CharField(max_length=50)
    results = PickledObjectField(default="Null",null=True)

    def __str__(self):
        return self.exam_name



class Stream(models.Model):
    stream_name = models.CharField(max_length=30)
    classteacher = models.CharField(max_length=40)
    exam = models.ArrayModelField(
        model_container=Exam,
    )

    def __str__(self):
        return  self.stream_name

    def find(self,examname,type=None):
        if type is None:
            return [obj for obj in self.exam if obj.exam_name == examname][0]
        else:
            return [obj for obj in self.exam if obj.exam_name == examname]

    def find_ordinal(self,examname,type=None):
        if type is None:
            return [self.exam.index(obj) for obj in self.exam if obj.exam_name == examname][0]
        else:
            return [self.exam.index(obj) for obj in self.exam if obj.exam_name == examname]

    def app(self,new):
        newexam = [obj for obj in self.exam]
        newexam.append(new)

        return newexam


class Class(models.Model):
    class_name = models.CharField(max_length = 50)
    stream_name = models.ArrayModelField(
        model_container=Stream,
    )

    def __str__(self):
        return  self.class_name

    def find(self,streamname,type=None):
        if type is None:
            return [obj for obj in self.stream_name if obj.stream_name == streamname][0]
        else:
            return [obj for obj in self.stream_name if obj.stream_name == streamname]

    def app(self,new):
        newstream = [obj for obj in self.stream_name]
        newstream.append(new)

        return newstream


class InstitutionManager(models.Manager):
    def find(self,institution_name,type=None):
        if type is None:
            return self.filter(institution_Name = institution_name)[0]
        else:
            return self.filter(institution_Name = institution_name)


class Institution(models.Model):
    institution_Name= models.CharField(max_length=50)
    institution_Number = models.IntegerField(default=0)
    class_name = models.ArrayModelField(model_container=Class, )

    objects = InstitutionManager()

    def __str__(self):
        return self.institution_Name

    def find(self,classname,type=None):
        if type is None:
            return [obj for obj in self.class_name if obj.class_name == classname][0]
        else:
            return [obj for obj in self.class_name if obj.class_name == classname]

    def app(self,new):
        newclass = [obj for obj in self.class_name]
        newclass.append(new)

        return newclass


class Teacher(models.Model):
    stream_name = models.CharField(max_length=30)
    teacher_list = PickledObjectField(default="Null")

    def __str__(self):
        return self.stream_name


def search_existence(user,clas,stream,classteacher,exam,result):

    if Institution.objects.find(user.name,1).count() != 0:

        if Institution.objects.find(user.name).find(clas,1) != []:

            if Institution.objects.find(user.name).find(clas).find(stream,1) != []:
                # create new exam
                newexam = CustomExam.objects.create(exam_name = exam, results = result)
                insert = Institution.objects.find(user.name)
                insert.find(clas).find(stream).exam = insert.find(clas).find(stream).app(newexam)
                insert.save()

                return Institution.objects.find(user.name).find(clas).find(stream).exam
            else:
                # create new stream
                newstream = Stream.objects.create(stream_name=stream,classteacher=classteacher,exam=[Exam(exam_name=exam, results=result)])
                insert_stream = Institution.objects.find(user.name)
                insert_stream.find(clas).stream_name = insert_stream.find(clas).app(newstream)
                insert_stream.save()

                return Institution.objects.find(user.name).find(clas).stream_name

        else:
            #create new class
            newclass = Class.objects.create(class_name=clas,stream_name=[Stream(stream_name=stream,classteacher=classteacher,exam=[Exam(exam_name=exam, results=result)])])
            insert = Institution.objects.find(user.name)
            insert.class_name = insert.app(newclass)
            insert.save()

            return Institution.objects.find(user.name).class_name

    else:
        #create new institution
        newinstitution = Institution.objects.create(institution_Number=user.institution_id, institution_Name=user.name,class_name=[Class(class_name=clas, stream_name=[Stream(stream_name=stream,classteacher=classteacher,exam=[Exam(exam_name=exam, results=result)])])])
        return Institution.objects.find(newinstitution.institution_Name)

