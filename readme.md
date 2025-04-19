# 📦 Evaluation 项目环境变量说明

本项目使用 `.env` 文件集中管理数据库连接信息与 JWT 鉴权配置。

---

## 🗂️ `.env` 文件路径

该文件位于项目根目录：
---

## ⚙️ 配置变量说明

| 变量名                      | 示例值                                             | 说明                        |
|---------------------------|-------------------------------------------------|---------------------------|
| `DB_USER`                 | `admin`                                         | 数据库用户名                    |
| `DB_PASSWORD`             | `password`                                      | 数据库密码                     |
| `DB_HOST`                 | `127.0.0.1`                                     | 数据库地址                     |
| `DB_PORT`                 | `3306`                                          | 数据库端口                     |
| `DB_NAME`                 | `evaluation_db`                                 | 使用的数据库名                   |
| `DB_ROOT_URI`             | `mysql+pymysql://admin:password@127.0.0.1:3306` | 不带数据库名的连接 URI，用于自动建库      |
| `ORIGINS`                 | `ORIGINS=http://localhost:80,http://example.com`| 允许的CORS跨域请求（填写前端协议/域名/端口） |

| JWT 鉴权配置项              | 示例值                   | 说明                                  |
|-----------------------------|------------------------|---------------------------------------|
| `SECRET_KEY`                | `secret_key`          | 用于签发 JWT Token 的密钥             |
| `ALGORITHM`                 | `HS256`               | JWT 加密算法（建议固定为 HS256）      |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30`                  | Token 有效时长（单位：分钟）         |

---

## ✅ 示例 `.env` 文件内容

```env
DB_USER=admin
DB_PASSWORD=password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=evaluation_db
DB_ROOT_URI=mysql+pymysql://admin:password@127.0.0.1:3306

SECRET_KEY=zsecret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ORIGINS=http://localhost:80,http://example.com