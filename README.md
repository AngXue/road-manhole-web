# 智能识别路面井盖隐患

## TODO
- [ ] 用户管理
  - [x] 后端接口
  - [ ] 前端页面
  - [ ] 单元测试
  - [ ] 功能测试
- [ ] 数据管理
  - [ ] 后端接口
  - [ ] 前端页面
  - [ ] 单元测试
  - [ ] 功能测试
- [ ] 模型训练任务管理
  - [ ] 后端接口
  - [ ] 前端页面
  - [ ] 单元测试
  - [ ] 功能测试
- [ ] 模型管理
  - [ ] 后端接口
  - [ ] 前端页面
  - [ ] 单元测试
  - [ ] 功能测试
- [ ] 集成测试与部署

## 实体模型

1. **User**: Django自带的用户模型，主要字段包括：
    - `username`: 用户名，字符串类型，用于唯一标识用户。
    - `password`: 密码，字符串类型，用户登录验证所用。

2. **UserProfile**: 用户扩展信息模型，主要字段包括：
    - `user`: 与User模型一对一关联的字段，用于关联Django自带的用户模型。
    - `role`: 用户角色，字符串类型，用于区分不同的用户类型（如普通用户、管理员等）。

## 接口文档

### 用户注册

- **URL**: `/api/user/`
- **方法**: `POST`
- **参数**:
    - `action`: 必须，值为 "register"。
    - `username`: 必须，用户的用户名。
    - `password`: 必须，用户的密码。
- **返回**:
    - 成功: 返回状态码201和注册的用户信息。
    - 失败: 返回状态码400和错误信息。
- **实例**:
    > 向 http://127.0.0.1:8000/api/user/ 发送POST请求（本地测试且端口为8000）
    ```json
    {
      "action": "register",
      "username": "test",
      "password": "123456"
    }
    ```
    > 成功返回
    ```json
    {
      "message": "用户注册成功",
      "user": {
          "username": "test"
      }
    }
    ```
    > 失败返回
    ```json
    {
      "username": [
          "A user with that username already exists."
      ]
    }
    ```

### 用户登录

- **URL**: `/api-token-auth/`
- **方法**: `POST`
- **参数**:
    - `username`: 必须，用户的用户名。
    - `password`: 必须，用户的密码。
- **返回**:
    - 成功: 返回状态码200和用户的Token。
    - 失败: 返回状态码400和错误信息。
- **实例**:
    >   /api-token-auth/ 发送POST请求
    ```json
    {
      "username": "test",
      "password": "123456"
    }
    ```
    >   成功返回
    ```json
    {
      "token": "8d0f788d7e3d9d5575348ef9606c3979a1679245"
    }
    ```
    >   失败返回
    ```json
    {
      "non_field_errors": [
          "Unable to log in with provided credentials."
      ]
    }
    ```

### 更新用户信息

- **URL**: `/api/user/`
- **方法**: `POST`
- **参数**:
    - `action`: 必须，值为 "update"。
    - `username`: 可选，要更新信息的用户的用户名。**注意**：仅管理员可指定用户名更新其他用户的信息。
    - `password`: 必须，用户的新密码。
- **权限**:
    - 普通用户：只能更新自己的密码，不能指定`username`参数。
    - 管理员：可以指定`username`参数来更新指定用户的密码。
- **返回**:
    - 成功: 返回状态码200和更新后的用户信息。
    - 失败: 返回状态码403表示没有权限更新其他用户的信息，状态码400表示请求参数错误或其他请求错误。
- **实例**:
    > /api/user/ 发送POST请求，header中携带Token
    例如：Key: Authorization, Value: Token 8d0f788d7e3d9d5575348ef9606c3979a1679245
    ```json
    {
      "action": "update",
      "password": "newpassword123"
    }
    ```
    > 成功返回
    ```json
    {
      "message": "密码更新成功。"
    }
    ```
- **实例**:
    ```json
    {
      "action": "update",
      "username": "otheruser",
      "password": "newpassword123"
    }
    ```
    > 成功返回
    ```json
    {
      "message": "密码更新成功。"
    }
    ```
    > 失败返回
    ```json
    {
      "detail": "没有权限更新其他用户的信息。"
    }
    ```

### 注意

- 需要认证的接口，如果请求没有携带Token或Token无效，都会返回如下信息：
    ```json
    {
      "detail": "Invalid token."
    }
    ```

### 删除用户

- **URL**: `/api/user/`
- **方法**: `POST`
- **参数**:
    - `action`: 必须，值为 "delete"。
    - `username`: 必须，要删除的用户username。
    - 需要在请求头中携带Token进行认证。
- **返回**:
    - 成功: 返回状态码204。
    - 失败: 返回状态码400和错误信息。
- **实例**:
    > /api/user/ 发送POST请求，header中携带Token
    ```json
    {
      "action": "delete",
      "username": "test"
    }
    ```
    > 成功返回
    ```json
    {
      "message": "用户删除成功。"
    }
    ```
    > 失败返回
    ```json
    {
      "detail": "没有权限删除其他用户。"
    }
    ```
    > 失败返回
    ```json
    {
      "detail": "用户不存在。"
    }
    ```

### 获取用户信息

- **URL**: `/api/user/`
- **方法**: `POST`
- **参数**:
    - `action`: 必须，值为 "get"。
    - 需要在请求头中携带Token进行认证。
- **返回**:
    - 成功: 返回状态码200和用户信息。
    - 失败: 返回状态码400和错误信息。
- **实例**:
    > /api/user/ 发送POST请求，header中携带Token
    ```json
    {
      "action": "get"
    }
    ```
    > 成功返回
    ```json
    {
      "User": {
          "id": 9,
          "username": "test",
          "role": "普通用户"
      }
    }
    ```
    > 失败返回
    ```json
    {
      "detail": "未认证的用户。"
    }
    ```

### 查询用户

- **URL**: `/api/user/`
- **方法**: `POST`
- **参数**:
    - `action`: 必须，值为 "query"。
    - `username`: 必须，要查询的用户名（支持模糊查询）,若为空则查询所有用户。
    - 需要在请求头中携带Token进行认证。
- **返回**:
    - 成功: 返回状态码200和符合条件的用户列表。
    - 失败: 返回状态码400和错误信息。
- **实例**:
    > /api/user/ 发送POST请求，header中携带Token
    ```json
    {
      "action": "query",
      "username": "test"
    }
    ```
    > 成功返回
    ```json
    [
        {
            "id": 12,
            "username": "test",
            "role": "普通用户"
        },
        {
            "id": 15,
            "username": "test2",
            "role": "普通用户"
        },
        {
            "id": 16,
            "username": "2test",
            "role": "普通用户"
        }
    ]
    ```
    > 失败返回
    ```json
    {
      "detail": "只有管理员可以查询用户。"
    }
    ```

## 注意事项

- 对于需要认证的接口（如更新、删除、获取、查询用户信息），必须在请求头中携带有效的Token，格式为`Authorization: Token <Your-Token>`。
- 用户注册和登录接口无需认证即可访问。
- 只有管理员用户可以查询其他用户、更新其他用户信息或删除其他用户。普通用户仅能更新或获取自己的信息。