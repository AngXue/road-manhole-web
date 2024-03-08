from django.shortcuts import render
from .models import YolovModel


def get_available_names(request):
    # 从数据库中查询所有模型名
    model_names = YolovModel.objects.all().values_list('name', flat=True)
    return render(request, 'index.html', {'models': list(model_names)})


def select_model(request):
    # 获取模型名
    model_name = request.POST.get('modelName')
    if not model_name:
        return render(request, 'index.html', {'result': False, 'msg': '模型名不能为空'})

    # 检查模型是否存在
    try:
        YolovModel.objects.get(name=model_name)
    except YolovModel.DoesNotExist:
        return render(request, 'index.html', {'result': False, 'msg': '模型不存在'})

    return render(request, 'index.html', {'result': True})


def get_model_overview(request):
    # 获取模型名
    model_name = request.POST.get('modelName')
    if not model_name:
        return render(request, 'index.html', {'result': False, 'msg': '模型名不能为空'})

    # 从数据库中查询模型信息
    model = YolovModel.objects.get(name=model_name)

    # 返回模型信息
    return render(request, 'index.html', {'model': model})


def get_model_perfor(request):
    # 获取模型名
    model_name = request.POST.get('modelName')
    if not model_name:
        return render(request, 'index.html', {'result': False, 'msg': '模型名不能为空'})

    # 从数据库中查询模型信息
    model = YolovModel.objects.get(name=model_name)

    # 返回模型信息
    return render(request, 'index.html', {'model': model})


def select_data_path(request):
    """
    选择数据集
    """
    return render(request, 'index.html', {'result': True})


def pre_analysis(request):
    """
    统计需预测数据集
    """
    return render(request, 'index.html', {'result': True})


def start_detect(request):
    """
    开始预测
    """
    return render(request, 'index.html', {'result': True})


def get_detect_status(request):
    """
    获取预测状态
    """
    return render(request, 'index.html', {'result': True})


def get_detect_result(request):
    """
    获取预测结果统计
    """
    return render(request, 'index.html', {'result': True})


def get_samples_path(request):
    """
    获取样本图路径
    """
    return render(request, 'index.html', {'result': True})


def get_detect_model_perfor(request):
    """
    获取模型预测性能图
    """
    return render(request, 'index.html', {'result': True})
