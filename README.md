# IPCIS_DNS

 对IPCIS系统DNS解析数据的分析处理

### 目录结构

```
./Malicious_Domain_Detect
│   ├── data_analysis		# 进行数据分析的handler
│   │   ├── data			# 收集到的所有数据 
│   │   ├── domain_feat		# 域名的特征测度
│   │   │   └── utils		# 通用模块
│   │   ├── ip_act			# ip活动分析
│   │   │   └── utils
│   │   └── whois			# whois信息分析
│   │       └── utils
│   └── malicious_track		# 可疑域名监测追踪系统
│       ├── Domain_Collect	# 可疑域名收集
│       ├── Client			# 系统前端(Vue.js)
│       └── Server			# 系统后端(tornado)
│           ├── MySQL		# 数据库连接
│           ├── doc			# 文档
│           ├── handler		# 各个模块具体处理程序
```

### 分工

监测系统前端：[@Silence-Rain](https://github.com/Silence-Rain)

监测系统后端服务器：[@Silence-Rain](https://github.com/Silence-Rain)，[@Mindbooom](https://github.com/Mindbooom)

域名特征测度数据分析：[@xudongh123](https://github.com/xudongh123)

域名特征测度数据库运维：[@hhinamoy](https://github.com/hhinamoy)

同形异义域名及其他恶意域名的收集：[@wtharry](https://github.com/wtharry)