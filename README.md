# 智能识别路面井盖隐患

## TODO
- 数据增强
- 尝试yolov7
- 是否使用restful风格

## 实体
- YOLOV模型：
  - 模型名 `model_name` 唯一值
  - 模型储存路径 `model_path`
  - 模型算力 `model_acid`
  - 模型参数数量 `model_parameter`
  - 模型大小 `model_size`

## 接口

### 切换模型
- 查询模型：
  - `/models/get_available_names`
  - 无需参数
  - 返回可用模型名列表 `List(<model_name>)`
- 选择模型：
  - `/models/select_model`
  - 传递模型名 `model_name`
  - 返回 `Dict({'result': True/False})`

### 模型参数预览
- 查询模型概览：
  - `/models/get_model_overview`
  - 传递模型名 `model_name`
  - 返回 `Dict({'model_acid': value, 'model_parameter': value, 'model_size': value})`
- 获取模型性能图：
  - `/models/get_model_perfor`
  - 传递模型名 `model_name`
  - 返回 `Dict({'labels_correlogram': model_path/labels_correlogram', ...})`

### 数据预测
- 选择数据集：
  - `/data/select_data_path`
  - 无需参数
  - 返回 `Dict({'data_path': value, 'sample_path': value})`
- 统计需预测数据集：（在获得数据集目录后立即调用）
  - `/data/pre_analysis`
  - 传递数据集路径 `Dict({'data_path': value})`
  - 返回 `Dict({'pic_nums': value, 'has_label': True/False})`
- 开始预测：（需要在统计需预测数据集之后才能调用）
  - `/data/start_detect`
  - 传递路径 `Dict({'model_name': model_name, 'data_path': value, has_label: True/False})`
  - 返回 `Dict({'result': True/False})`

### 预测结果分析
- 获取预测状态：
  - `/detect/get_detect_status`
  - 无需参数
  - 返回 `Dict({'result': True/False})`
- 获取预测结果统计：（必须在预测结果返回True之后调用）
  - `/dectect/get_detect_result`
  - 无需参数
  - 返回 `Dict({'good': value, 'circle': value, 'uncover': value, 'broke': value, 'lose': value, 'P': value, 'R': value, 'map50': value, 'map50-95': value})`
- 获取样本图路径：（必须在预测结果返回True之后调用）
  - `/dectect/get_samples_path`
  - 无需参数
  - 返回 `List(<Str samplePath>)`
- 获取模型预测性能图：（当用户选择的数据集是带标注的验证集才能调用->`hasLabel: True`）
  - `/dectect/get_detect_model_perfor`
  - 无需参数
  - 返回 `Dict({'labels_correlogram': path', ...})`