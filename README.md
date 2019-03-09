## 各文件夹内容
#### 1. kdnet/ v2ex 
- 为了wenda网站的前期数据扩充，用pyspider写了凯迪社区的爬虫，共爬取约5w条数据,包括问题，评论和用户信息等。
- 知乎和v2ex爬不下来,代码不可用，v2ex的爬虫被重定向

#### 2. 11thlesson

牛客网高级项目课第11课和12课python学习代码;
  - requests
  - pymysql
  - pyquery
  - pyspider
  


#### 3. mysql / redis

本机写项目时的mysql、redis的数据备份在这两个文件夹，为了便于向阿里云服务器迁移
迁移流程：
  - 本机的sql和redis数据备份于此
  - linux服务器中git fetch下来
  - mysql\redis中执行恢复备份命令
  

