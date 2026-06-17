# 车间管理系统 (Workshop Management System) — 规格说明书

## 1. Objective（目标）

### 做什么
一个集成**人员管理 + 任务管理**的车间管理系统，包含：
- **后端 API**：FastAPI + MySQL
- **微信小程序前端**：学生扫码查看自己的数据
- **二维码**：每个用户独立二维码，扫码进入小程序查看
- **预留接口**：ERP、MES、WMS 系统对接

### 谁用
| 角色 | 权限 |
|------|------|
| **管理员 (admin)** | 增删改查所有数据（人员、任务） |
| **普通用户 (user)** | 只能查看自己的数据 |

### 成功标准
- [ ] 管理员能通过 API 管理所有人员和任务
- [ ] 用户扫码后只能看到自己的信息
- [ ] 预留了 ERP/MES/WMS 三套系统的标准接口
- [ ] 代码结构支持二次开发（模块化、分层清晰）

---

## 2. Commands（命令）

```bash
# 数据库初始化
mysql -u root -proot123456 < backend/init_db.sql

# 安装后端依赖
pip install -r backend/requirements.txt

# 启动后端服务
D:/python3.7.6/python.exe -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 运行测试
D:/python3.7.6/python.exe -m pytest backend/tests/

# API 文档（启动后访问）
http://localhost:8000/docs
```

---

## 3. Project Structure（项目结构）

```
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
```

---

## 4. Code Style（代码风格）

```python
# 路由示例
from fastapi import APIRouter, HTTPException
from backend.models.user import User
from backend.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["人员管理"])

@router.get("/{user_id}")
async def get_user(user_id: int):
    """查询单个用户"""
    user = UserService.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user
```

**规范：**
- 命名：snake_case（Python）、kebab-case（小程序文件）
- 路由格式：`/api/{资源名}/{动作}`
- 错误统一返回 `{ "error": "message" }` 格式
- API 文档用 FastAPI 自带的 `/docs`

---

## 5. Testing Strategy（测试策略）

| 层级 | 框架 | 位置 | 覆盖 |
|------|------|------|------|
| 单元测试 | pytest | `backend/tests/` | 业务逻辑层 |
| API 测试 | pytest + httpx | `backend/tests/` | 所有路由 |
| 小程序 | 手动测试 | 微信开发者工具 | 页面功能 |

- **测试金字塔**：80% 单元测试, 15% API 测试, 5% 手动测试
- TDD 流程：先写测试 → 红 → 绿 → 重构

---

## 6. Database Schema（数据库设计）

**数据库名：`wms_db`**

### admins 表（管理员）
```sql
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(50),
    role ENUM('super_admin', 'admin') DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### users 表（普通用户/学生）
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL UNIQUE COMMENT '学号',
    name VARCHAR(50) NOT NULL,
    class_name VARCHAR(50) COMMENT '班级',
    phone VARCHAR(20),
    qrcode_token VARCHAR(64) UNIQUE COMMENT '二维码唯一标识',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### tasks 表（任务/工单）
```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '所属用户',
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
    quantity INT DEFAULT 0 COMMENT '产量',
    deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 7. API Design（接口设计）

### 认证
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/admin/login` | 管理员登录 |
| POST | `/api/auth/user/login` | 用户扫码登录（用 qrcode_token） |

### 人员管理（管理员）
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/users` | 查询所有用户 |
| GET | `/api/users/{id}` | 查询单个用户 |
| POST | `/api/users` | 新增用户（自动生成二维码） |
| PUT | `/api/users/{id}` | 修改用户信息 |
| DELETE | `/api/users/{id}` | 删除用户 |

### 任务管理（管理员）
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/tasks` | 查询所有任务 |
| GET | `/api/tasks/{id}` | 查询单个任务 |
| POST | `/api/tasks` | 新增任务 |
| PUT | `/api/tasks/{id}` | 修改任务 |
| DELETE | `/api/tasks/{id}` | 删除任务 |

### 用户端
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/my/data` | 查看自己的信息和任务 |

### 二维码
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/qrcode/{token}` | 返回用户信息（扫码后调用） |
| GET | `/api/qrcode/{user_id}/image` | 生成二维码图片 |

### 预留接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/integration/erp/orders` | ERP 工单同步 |
| POST | `/api/integration/mes/progress` | MES 生产进度上报 |
| POST | `/api/integration/wms/inventory` | WMS 库存同步 |

---

## 8. Boundaries（边界）

### 始终
- 运行测试后再提交
- 验证所有用户输入
- 返回明确的错误信息

### 先问
- 修改数据库表结构前
- 添加新依赖前
- 修改 API 路径前

### 绝不
- 提交密码和密钥
- 删除失败的测试（应该修复代码）
- 跳过输入验证
