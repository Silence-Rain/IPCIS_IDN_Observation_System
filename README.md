## IPCIS_Domains_Information_System

 IPCIS下属的域名信息分析系统

A information analysis system included by IPCIS (IP Comprehensive Information System)

#### 目录结构

```sh
./IPCIS_Domains_Information_System
├── client              # 系统前端(Vue.js)
├── domain_import       # 新域名导入模块
└── server              # 系统后端(tornado)
```

#### 依赖

- 前端
  - Vue.js@2.9.2
  - vue-router@3.0.1
  - iView@2.13.0
  - Echarts@4.0.4
  - inMap@1.5.6
- 后端
  - Python@3.6.3
  - tornado@5.0.2
  - pymysql@0.8.1
  - IPy@0.83
  - apscheduler@3.5.1

#### 实现功能

- 获取域名基本信息，解析IP信息，whois归属信息
- 获取域名解析IP通信活动的稳定&最大拓扑结构
- 获取域名解析IP活动的地理位置分布
- 计算并获取域名活跃度

