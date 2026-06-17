-- ============================================
-- 车间管理系统 (WMS) - 数据库初始化脚本
-- ============================================

USE wms_db;

-- 1. 管理员表
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(50),
    role VARCHAR(20) DEFAULT 'admin' COMMENT 'super_admin/admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. 普通用户表（学生/工人）
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL UNIQUE COMMENT '学号',
    name VARCHAR(50) NOT NULL,
    class_name VARCHAR(50) COMMENT '班级',
    phone VARCHAR(20),
    qrcode_token VARCHAR(64) UNIQUE COMMENT '二维码唯一标识',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. 任务表
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '所属用户',
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending' COMMENT 'pending/in_progress/completed',
    quantity INT DEFAULT 0 COMMENT '产量',
    deadline DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. 插入默认管理员（密码: admin123，sha256 哈希）
INSERT INTO admins (username, password_hash, name, role) VALUES
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', '系统管理员', 'super_admin')
ON DUPLICATE KEY UPDATE username=username;

-- 5. 插入测试用户
INSERT INTO users (student_id, name, class_name, qrcode_token) VALUES
('2024001', '张三', '机械工程1班', 'qr_token_zhangsan_2024001'),
('2024002', '李四', '机械工程2班', 'qr_token_lisi_2024002'),
('2024003', '王五', '自动化1班',   'qr_token_wangwu_2024003')
ON DUPLICATE KEY UPDATE student_id=student_id;

-- 6. 插入测试任务
INSERT INTO tasks (user_id, title, description, status, quantity, deadline) VALUES
(1, '加工齿轮A', '按图纸加工齿轮A型号，精度0.01mm', 'in_progress', 50, '2026-06-20'),
(1, '打磨轴套', '对轴套进行表面打磨处理', 'pending', 30, '2026-06-22'),
(2, '装配电机', '将电机组件装配到基座上', 'completed', 10, '2026-06-18'),
(3, '质检工件', '对当日生产工件进行质量检查', 'pending', 100, '2026-06-21')
ON DUPLICATE KEY UPDATE title=title;
