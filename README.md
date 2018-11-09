## IPCIS_IDN_Observation_System

 IPCIS下属的国际化域名累计观测系统

An accumulative observation system of international domain names (IDNs) included by IPCIS (IP Comprehensive Information System)

#### 目录结构

```sh
./IPCIS_IDN_Observation_System
├── client              # 系统前端(Vue.js)
└── server              # 系统后端(tornado)
```

#### 实现功能

- 国际化域名收集
- 国际化域名语种分布
- 国际化域名按语种的地理位置&管理归属分布
- 单个域名的 whois 信息&解析 IP 信息
- 单个域名指定时间区间内通信对端的网络拓扑
- 单个域名指定时间区间内通信对端的地理位置&管理归属统计

