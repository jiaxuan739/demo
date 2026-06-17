# 车间管理系统（Workshop Management System） — 规格说明书
## 1. 目标（目标）
      做什么
      一个集成人员管理 + 任务管理的车间管理系统，包含：
    
    后端 API：FastAPI + MySQL
    微信小程序前端：学生扫码查看自己的数据
    二维码：每个用户独立二维码，扫码进入小程序查看
    预留接口：ERP、MES、WMS 系统对接
    谁用
    角色	权限
    管理员（管理员）	增删改查所有数据（人员、任务）
    普通用户（用户）	只能查看自己的数据
    成功标准
    管理员能通过 API 管理所有人员和任务
    用户扫码后只能看到自己的信息
    预留了 ERP/MES/WMS 三套系统的标准接口
    代码结构支持二次开发（模块化、分层清晰）

## 项目结构
d:\student\workshop\
├── SPEC.md                          # 本规格说明书
├── tasks/
│   └── plan.md                      # 任务分解
├── backend/                         # FastAPI 后端
│   ├── main.py                      # 应用入口
│   ├── config.py                    # 数据库配置
│   ├── init_db.sql                  # 建库建表 SQL
│   ├── requirements.txt             # Python 依赖
│   ├── models/                      # 数据模型
│   │   ├── __init__.py
│   │   ├── admin.py                 # 管理员模型
│   │   └── user.py                  # 用户模型
│   ├── routes/                      # API 路由
│   │   ├── __init__.py
│   │   ├── auth.py                  # 登录认证
│   │   ├── users.py                 # 人员管理 CRUD
│   │   ├── tasks.py                 # 任务管理 CRUD
│   │   └── qrcode.py                # 二维码生成
│   ├── services/                    # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── task_service.py
│   ├── integrations/                # 外部系统接口（预留）
│   │   ├── __init__.py
│   │   ├── erp_interface.py         # ERP 接口
│   │   ├── mes_interface.py         # MES 接口
│   │   └── wms_interface.py         # WMS 接口
│   └── tests/                       # 测试
│       ├── __init__.py
│       ├── test_auth.py
│       ├── test_users.py
│       └── test_tasks.py
└── miniprogram/                     # 微信小程序
    ├── app.js                       # 小程序入口
    ├── app.json                     # 全局配置
    ├── app.wxss                     # 全局样式
    └── pages/
        ├── index/                   # 首页（扫码入口）
        ├── login/                   # 登录页
        ├── my-data/                 # 我的数据（用户端）
        ├── admin-users/             # 人员管理（管理员）
        └── admin-tasks/             # 任务管理（管理员）
