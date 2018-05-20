## IPCIS_Malicious_Detection

 IPCIS下属的恶意域名检测系统

A malicious domains detection system included by IPCIS (IP Comprehensive Information System)

#### 目录结构

```sh
./malicious_detection
│   ├── data_analysis			# 域名检测所需raw data数据库设计
│   │   ├── data
│   │   ├── domain_feat			# 域名基本信息和whois信息获取
│   │   └── ip_act				# 域名ip活动获取
│   └── detection_system		# 恶意域名检测系统
│       ├── domain_collection	# 基于编码的同形异义域名收集
│       ├── client				# 检测系统前端(Vue.js)
│       └── server				# 检测系统后端(tornado)
```

#### 分工

- 检测系统前端：[@Silence-Rain](https://github.com/Silence-Rain)
- 检测系统后端：[@Silence-Rain](https://github.com/Silence-Rain)，[@xudongh123](https://github.com/xudongh123)
- 检测系统运维：[@hhinamoy](https://github.com/hhinamoy)
- 恶意域名特征测度分析：[@hhinamoy](https://github.com/hhinamoy)，[@Mindbooom](https://github.com/Mindbooom)
- 基于编码的同形异义域名收集：[@wtharry](https://github.com/wtharry)