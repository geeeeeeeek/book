# Create your views here.
from django.db import connection
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes

from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Classification
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import ClassificationSerializer
from myapp.utils import dict_fetchall


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        sql_str = 'SELECT x.id AS parentId, x.title AS parentTitle, y.id AS childId ,y.title AS childTitle FROM ' \
                  'b_classification AS x LEFT JOIN b_classification AS y ON y.pid = x.id WHERE x.pid = -1 order by ' \
                  'x.create_time desc '
        data = []
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            join_data = dict_fetchall(cursor)
            # print(join_data)
            for item1 in join_data:
                found = False
                for item2 in data:
                    if item2['key'] == item1['parentId']:
                        found = True
                        if item1['childId']:
                            item2['children'].append({
                                'key': item1['childId'],
                                'name': item1['childTitle'],
                                'isParent': False,
                                # 'children': []
                            })
                        break
                if not found:
                    k = {
                        'key': item1['parentId'],
                        'name': item1['parentTitle'],
                        'isParent': True,
                        'children': []
                    }
                    if item1['childId']:
                        k['children'].append({
                            'key': item1['childId'],
                            'name': item1['childTitle'],
                            'isParent': False,
                            # 'children': []
                        })
                    data.append(k)
        return APIResponse(code=0, msg='????????????', data=data)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='????????????????????????')

    classification = Classification.objects.filter(title=request.data['title'])
    if len(classification) > 0:
        return APIResponse(code=1, msg='??????????????????')

    serializer = ClassificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='????????????', data=serializer.data)

    return APIResponse(code=1, msg='????????????')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='????????????????????????')

    try:
        pk = request.GET.get('id', -1)
        print(pk)
        classification = Classification.objects.get(pk=pk)
    except Classification.DoesNotExist:
        return APIResponse(code=1, msg='???????????????')

    serializer = ClassificationSerializer(classification, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='????????????', data=serializer.data)

    return APIResponse(code=1, msg='????????????')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='????????????????????????')

    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        # ?????????????????????????????????
        Classification.objects.filter(Q(id__in=ids_arr) | Q(pid__in=ids_arr)).delete()
    except Classification.DoesNotExist:
        return APIResponse(code=1, msg='???????????????')
    return APIResponse(code=0, msg='????????????')
