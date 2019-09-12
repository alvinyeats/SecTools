# 敏感文件检索器

查找记录用户名密码的文件

## 需求点

- 支持排除目录，不收集目标目录下的文件（常见的windows系统文件）
- 支持指定目录，只收集指定目录下的文件
- 支持windows域登录，远程检索
- 支持linux登录，远程检索
- 为了不影响服务器性能，扫描的目录层级限制在三层以内

## Refer

```code
本地登录
net use \\{ip} /user:{username} {password}

域登录
net use \\{ip} /user:{domain}\{username} {password}

列可使用的连接
net use

连接成功后即可操作远程目录，如：
dir \\{ip}\C$\

删除指定连接
net use \\{ip}\IPC$ /delete

删除所有连接
net use * /delete
```

