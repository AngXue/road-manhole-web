# 智能识别路面井盖隐患

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
  - `/models/getAvailableNames`
  - 无需参数
  - 返回可用模型名列表 `List(<model_name>)`
- 选择模型：
  - `/models/selectModel`
  - 传递模型名 `model_name`
  - 返回 `Dict({'result': True/False})`

### 模型参数预览
- 查询模型概览：
  - `/models/getModelOverview`
  - 传递模型名 `model_name`
  - 返回 `Dict({'model_acid': value, 'model_parameter': value, 'model_size': value})`
- 获取模型性能图：
  - `/models/getModelPerfor`
  - 传递模型名 `model_name`
  - 返回 `Dict({'labels_correlogram': model_path/labels_correlogram', ...})`

### 数据预测
- 选择数据集：
  - `/data/selectDataPath`
  - 无需参数
  - 返回 `Dict({'dataPath': value, 'samplePath': value})`
- 统计需预测数据集：（在获得数据集目录后立即调用）
  - `/data/preAnalysis`
  - 传递数据集路径 `Dict({'dataPath': value})`
  - 返回 `Dict({'picNums': value, 'hasLabel': True/False})`
- 开始预测：（需要在统计需预测数据集之后才能调用）
  - `/data/startDetect`
  - 无需参数
  - 返回 `Dict({'result': True/False})`

### 预测结果分析
- 获取预测状态：
  - `/detect/status`
  - 无需参数
  - 返回 `Dict({'result': True/False})`
- 获取预测结果统计：（必须在预测结果返回True之后调用）
  - `/dectect/result`
  - 无需参数
  - 返回 `Dict({'good': value, 'circle': value, 'uncover': value, 'broke': value, 'lose': value, 'P': value, 'R': value, 'map50': value, 'map50-95': value})`
- 获取样本图路径：（必须在预测结果返回True之后调用）
  - `/dectect/samplesPath`
  - 无需参数
  - 返回 `List(<Str samplePath>)`
- 获取模型预测性能图：（当用户选择的数据集是带标注的验证集才能调用->`hasLabel: True`）
  - `/dectect/getModelPerfor`
  - 无需参数
  - 返回 `Dict({'labels_correlogram': path', ...})`