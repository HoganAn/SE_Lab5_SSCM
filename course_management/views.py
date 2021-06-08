from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, FileResponse
from django.utils.http import urlquote
from django.shortcuts import render
from django.conf import settings
from course_management.models import Course, CourseRegistration, CourseFiles
from login.models import Student
import os


def cs_view(request):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')

        uid = request.session.get('uid')
        usr_type = request.session.get('usr_type')
        usr_name = request.session.get('name')
        return render(request, "course_select.html", locals())


def get_selectable_courses(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        courses = Course.objects.exclude(reg_stat__uid=uid)
        total = courses.count()
        course_info = []
        for c in courses:
            data = {
                'cid': c.course_id,
                'cname': c.course_name,
                'fname': c.faculty,
                'tname': c.lecturer.name,
                'cinfo': c.info
            }
            course_info.append(data)

        data = {
            'code': 0,
            'count': total,
            'data': course_info
        }
        return JsonResponse(data)
    else:
        return HttpResponse(status=405)


def get_select_stat(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        courses = Course.objects.filter(reg_stat__uid=uid)
        course_list = []
        for c in courses:
            stat = CourseRegistration.objects.get(course__course_id=c.course_id).is_joined
            data = {
                'cid': c.course_id,
                'cname': c.course_name,
                'fname': c.faculty,
                'tname': c.lecturer.name,
                'cstat': stat
            }
            course_list.append(data)
        data = {
            'code': 0,
            'data': course_list
        }
        return JsonResponse(data)
    else:
        return HttpResponse(status=405)


def course_selected(request):
    if request.method == 'POST':
        cid = request.POST.get('cid')
        uid = request.session.get('uid')
        course = Course.objects.get(course_id=cid)
        stu = Student.objects.get(uid=uid)
        pre_courses = course.prerequisite.all()
        for pc in pre_courses:
            stat = Course.objects.filter(course_id=pc.pre_course_id,
                                         reg_stat__uid=uid,
                                         courseregistration__is_joined='1')
            if len(stat) == 0:
                return HttpResponse('UnmetRequirement')

        course.reg_stat.add(stu, through_defaults={'is_joined': '0'})
        return HttpResponse('Success')
    else:
        return HttpResponse(status=405)


def my_course_view(request):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
        uid = request.session.get('uid')
        usr_type = request.session.get('usr_type')
        usr_name = request.session.get('name')
        return render(request, "my_course.html", locals())


def course_index_view(request, course_id):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    cname = Course.objects.get(course_id=course_id)
    cid = course_id
    return render(request, "course_info.html", locals())


def course_intro_view(request, course_id):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    course = Course.objects.get(course_id=course_id)
    cname = course.course_name
    cid = course_id
    course_intro = course.info
    return render(request, "course_intro.html", locals())


def course_files_view(request, course_id):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    course = Course.objects.get(course_id=course_id)
    cname = course.course_name
    cid = course_id
    return render(request, "s_course_files.html", locals())


def my_score_view(request):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    return render(request, "my_score.html", locals())


def t_course_manage_view(request):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    return render(request, "t_my_course.html", locals())


def t_course_index_view(request, course_id):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    cname = Course.objects.get(course_id=course_id)
    return render(request, "t_course_index.html", locals())


def t_course_file_view(request, course_id):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    cname = Course.objects.get(course_id=course_id)
    return render(request, "t_course_file_manage.html", locals())


def get_my_course_list(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        courses = Course.objects.filter(reg_stat__uid=uid, courseregistration__is_joined='1')
        total = courses.count()
        course_info = []
        for c in courses:
            data = {
                'cid': c.course_id,
                'cname': c.course_name,
                'fname': c.faculty,
                'tname': c.lecturer.name,
                'cinfo': c.info
            }
            course_info.append(data)

        data = {
            'code': 0,
            'count': total,
            'data': course_info
        }
        return JsonResponse(data)
    else:
        return HttpResponse(status=403)


def get_t_my_course_list(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        courses = Course.objects.filter(lecturer__uid=uid)
        total = courses.count()
        course_info = []
        for c in courses:
            data = {
                'cid': c.course_id,
                'cname': c.course_name,
                'fname': c.faculty,
            }
            course_info.append(data)

        data = {
            'code': 0,
            'count': total,
            'data': course_info
        }
        return JsonResponse(data)
    else:
        return HttpResponse(status=403)


def get_course_file_list(request):
    if request.method == 'GET':
        cid = request.GET.get('cid')
        files = CourseFiles.objects.filter(course__course_id=cid)
        file_list = []
        for file in files:
            data = {
                "fname": file.file.name.split('/')[-1],
                "uptime": file.add_date.strftime("%Y年%m月%d日 %H:%M:%S")
            }
            file_list.append(data)
        data = {
            "code": 0,
            "data": file_list
        }
        return JsonResponse(data)


def upload(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        cid = request.POST.get('cid')
        course = Course.objects.get(course_id=cid)
        CourseFiles.objects.create(course=course, file=file)
        data = {
            "code": 0
        }
        return JsonResponse(data)
    else:
        return HttpResponse(status=403)


def download(request):
    if request.method == 'GET':
        cid = request.GET.get('cid')
        fname = request.GET.get('fname')
        file_path = os.path.join(settings.MEDIA_ROOT, 'course_files', cid, fname)
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename={0}'.format(urlquote(fname))
        return response
    else:
        return HttpResponse(status=403)
