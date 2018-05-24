## IPCIS_Malicious_Detection

 IPCIS下属的恶意域名检测系统

A malicious domains detection system included by IPCIS (IP Comprehensive Information System)

#### 目录结构

```sh
./IPCIS_Malicious_Detection
│   ├── data_analysis			# 域名检测所需raw data数据库设计
│   │   ├── data
│   │   ├── domain_feat			# 域名基本信息和whois信息获取
│   │   └── ip_act				# 域名ip活动获取
│   └── detection_system		# 恶意域名检测系统
│       ├── domain_collection	# 基于编码的同形异义域名，已知恶意域名收集
│       ├── client				# 检测系统前端(Vue.js)
│       └── server				# 检测系统后端(tornado)
```

#### 分工

- 检测系统前端：[@Silence-Rain](https://github.com/Silence-Rain)
- 检测系统后端：[@Silence-Rain](https://github.com/Silence-Rain)
- 检测系统数据库：[@xudongh123](https://github.com/xudongh123)
- 恶意域名特征测度分析：[@hhinamoy](https://github.com/hhinamoy)，[@Mindbooom](https://github.com/Mindbooom)
- 基于编码的同形异义域名收集：[@wtharry](https://github.com/wtharry)

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

####实现功能

- 获取域名基本信息，解析IP信息，whois归属信息
- 获取域名解析IP通信活动的稳定&最大拓扑结构
- 获取域名解析IP活动的地理位置分布
- 计算并获取域名活跃度
- 计算并预测域名服务类型

