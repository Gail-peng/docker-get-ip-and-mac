# 这是一个通过docker部署（或是本地部署）的网络测试工具

该工具用于扫描指定网络内和宿主机连接的设备的UP和MAC地址


## 配置方法

1. 进入项目文件夹

2. 执行代码

```
docker build -t network-scanner-web .

```

3. 执行代码，使用docker compose 构建容器

```
docker-compose up -d

```

4. 启动后，通过在浏览器中输入

```
http://localhost:5000

```
或是

```
http://host-ip:5000

```
均可访问操作界面，查询中只需要输入指定网络地址即可
