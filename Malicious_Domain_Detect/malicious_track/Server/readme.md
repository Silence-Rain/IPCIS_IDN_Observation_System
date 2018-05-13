## IPCIS恶意域名检测系统 后端文档

#### 依赖

- Python 3.6.3
- Tornado 5.0.2

#### 实现功能

- 获取域名基本信息
- 获取域名解析IP活动的稳定&最大拓扑结构
- 获取域名解析IP活动的地理位置分布
- 计算并获取域名活跃度
- 计算并预测域名服务类型

#### API

##### info - 获取域名基本信息

- url：`/info`

- method：`POST`

- 参数：

  | 字段        | 类型   | 描述         |
  | ----------- | ------ | ------------ |
  | domain_name | String | 要查询的域名 |

- Success 200:

  | 字段   | 类型   | 描述               |
  | ------ | ------ | ------------------ |
  | status | String | "success"          |
  | result | Object | 查询域名的基本信息 |

  ```json
  result: {
      "domain_name": "www.test.com",
      "static": {
          "is_dga": 0,
          "ttl": 86400,
          "credit": 70,
      },
      "whois": {
          "registrar": "注册人",
          "registrant": "注册机构",
          "address": "注册机构地址",
          "email": "test@email.com",
          "register_date": "17-jun-2005",
          "expire_date": "17-jun-2020"
      },
      "ip": {
          "ip": ["118.89.140.118","45.77.86.38"],
          "location": ["中国-上海-上海", "美国-CA-洛杉矶"],
          "count": [100, 50]
      }
  }
  ```

- Error 4xx：

  | 字段   | 类型   | 描述       |
  | ------ | ------ | ---------- |
  | status | String | "err"      |
  | result | String | 错误的原因 |

##### topo - 获取稳定拓扑结构

- url：`/topo/steady`

- method：`GET`

- header：

  | 字段        | 类型   | 描述         |
  | ----------- | ------ | ------------ |
  | domain_name | String | 要查询的域名 |

- Success 200:

  | 字段   | 类型   | 描述                 |
  | ------ | ------ | -------------------- |
  | status | String | "success"            |
  | result | Object | 稳定拓扑结构的图数据 |

  ```json
  result: {
      "node": [
          {
              "id": 0,
              "name": "118.89.140.118",
              "count": 100
          },
          {
              "id": 1,
              "name": "45.77.86.38",
              "count": 50
          }
          ...
      ],
      "links": [
          {
              "source": 0,
              "target": 1
          },
          {
              "source": 1,
              "target": 2
          },
          ...
      ]
  }
  ```

  

- Error 4xx：

  | 字段   | 类型   | 描述       |
  | ------ | ------ | ---------- |
  | status | String | "err"      |
  | result | String | 错误的原因 |

##### topo - 获取最大拓扑结构

- url：`/topo/max`

- method：`GET`

- header：

  | 字段        | 类型   | 描述         |
  | ----------- | ------ | ------------ |
  | domain_name | String | 要查询的域名 |

- Success 200:

  | 字段   | 类型   | 描述                 |
  | ------ | ------ | -------------------- |
  | status | String | "success"            |
  | result | Object | 最大拓扑结构的图数据 |

  ```json
  result: {
      "node": [
          {
              "id": 0,
              "name": "118.89.140.118",
              "count": 100
          },
          {
              "id": 1,
              "name": "45.77.86.38",
              "count": 50
          }
          ...
      ],
      "links": [
          {
              "source": 0,
              "target": 1
          },
          {
              "source": 1,
              "target": 2
          },
          ...
      ]
  }
  ```

- Error 4xx：

  | 字段   | 类型   | 描述       |
  | ------ | ------ | ---------- |
  | status | String | "err"      |
  | result | String | 错误的原因 |

##### location

- url：`/location`

- method：`GET`

- header：

  | 字段        | 类型   | 描述         |
  | ----------- | ------ | ------------ |
  | domain_name | String | 要查询的域名 |

- Success 200:

  | 字段   | 类型   | 描述                 |
  | ------ | ------ | -------------------- |
  | status | String | "success"            |
  | result | Object | 域名解析IP的地理信息 |

  ```json
  result: [
      {
          "lng": 118.8028, 
          "lat": 32.0647,
          "ip": "202.112.23.167",
          "location": "中国-江苏-南京",
          "count": 25
  	}
      ...
  ]
  ```

- Error 4xx：

  | 字段   | 类型   | 描述       |
  | ------ | ------ | ---------- |
  | status | String | "err"      |
  | result | String | 错误的原因 |

##### active

- url：`/active`

- method：`GET`

- header：

  | 字段        | 类型   | 描述         |
  | ----------- | ------ | ------------ |
  | domain_name | String | 要查询的域名 |

- Success 200:

  | 字段   | 类型   | 描述                                 |
  | ------ | ------ | ------------------------------------ |
  | status | String | "success"                            |
  | result | Object | 域名解析IP的活跃度和历史测度（30天） |

  ```json
  result: [
      {
          "ip": "118.89.140.118",
          "active": 90,
          "count": [100,120,80,70...],
          "opposite_ip_count": [10,15,8,9...],
          "ip_geo_entropy": [1.12,2.34,0.86,4.77...]
  	}
      ...
  ]
  ```

- Error 4xx：

  | 字段   | 类型   | 描述       |
  | ------ | ------ | ---------- |
  | status | String | "err"      |
  | result | String | 错误的原因 |

##### service

- url：`/service`

- method：`GET`

- header：

  | 字段        | 类型   | 描述         |
  | ----------- | ------ | ------------ |
  | domain_name | String | 要查询的域名 |

- Success 200:

  | 字段   | 类型   | 描述                                       |
  | ------ | ------ | ------------------------------------------ |
  | status | String | "success"                                  |
  | result | Object | 域名解析IP的预测服务类型和历史测度（30天） |

  ```json
  result: [
      {
          "ip": "118.89.140.118",
          "type": 60,
          "is_dga": 0,
          "ttl": 86400,
          "credit": 70,
          "ip_count": [10,15,8,9...],
          "byte_per_mess": [123.5,240,160.8,188.3...],
          "port": [
              {
                 "port": 80,
                 "freq": 1200,
              }
              ...
          ]
      }
      ...
  ]
  ```

- Error 4xx：

  | 字段   | 类型   | 描述       |
  | ------ | ------ | ---------- |
  | status | String | "err"      |
  | result | String | 错误的原因 |

##### 