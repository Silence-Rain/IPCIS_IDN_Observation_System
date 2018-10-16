<template>
	<div>
		<div class="label">概览</div>
		<Card class="card">
            <p slot="title">通信对端 IP 总数</p>
            <p style="font-size:35px;font-weight:bold;margin-left:10px;">{{this.ips.length}}</p>
        </Card>

		<div class="label">地理分布 - 表</div>
		<Table stripe :loading="isLoading" :columns="cols" :data="cluster"></Table>

		<div class="label">地理分布 - 地图</div>
		<hr color="#f5f7f9"/>
		<keep-alive>
			<div id="chart" style="width:100%;height:500px;margin-left:10px;"></div>
		</keep-alive>
	</div>
</template>

<script>
	import inMap from "inmap/dist/inmap.min.js"

	export default {
		data () {
			return {
				targetDomain: "",			// 要查询的目标域名
				ips: [],					// 目标域名解析IP列表
				raw: [],					// 原始IP活动数据
				isLoading: false,
				cols: [{
                    title: "位置",
                    key: "location"
                },
                {
                    title: "通信对端数",
                    key: "count"
                }]
			}
		},

		computed: {
			// 按照inMap要求，格式化后的IP活动数据
			acts () {
				let ret = []
				for (var item of this.raw) {
					let temp = {
				        name: item.location,
				        ip: item.ip,
				        geometry: {
				            type: 'Point',
				            coordinates: [item.lng, item.lat]
				        },
				        style: {
				            backgroundColor: (this.ips.indexOf(item.ip) == -1)
						? "#FF8C00" : "#0F0",
				            size: 5,
				        }
				    }

					// // 累加IP活动数
					// temp["count"] = item.count.reduce((acc, val) => {
					// 	return acc + val 
					// })
					// // 根据IP活动量设置节点大小
					// temp["style"] = {size: Math.log2(temp.count) + 1}
					// // 解析IP和对端IP标注不同颜色
					// temp["style"]["backgroundColor"] = (this.ips.indexOf(item.ip) == -1)
					// 	? "#FF8C00" : "#0F0"

					ret.push(temp)
				}
				return ret
			},
			cluster () {
				let set = {}
				let ret = []
				for (let item of this.raw) {
					// 域名自己的解析IP不计入对端
					if (this.ips.indexOf(item.ip) != -1) {
						continue
					}
					if (item.location in set) {
						set[item.location] += 1
					} else {
						set[item.location] = 1
					}
				}
				for (let item in set) {
					ret.push({location: item, count: set[item]})
				}

				return ret
			}
		},

		created () {
			// 从localStorage中获取目标域名和解析IP列表
			this.ips = JSON.parse(localStorage.getItem("ips"))
			this.targetDomain = localStorage.getItem("domain")
		},

		mounted () {
			this.raw = [
			    {
			        "lng": 118.8028, 
			        "lat": 32.0647,
			        "ip": "118.89.140.118",
			        "location": "中国-江苏-南京"
			    },
			    {
			        "lng": 119.8028, 
			        "lat": 32.0647,
			        "ip": "118.9.140.118",
			        "location": "中国-江苏-南京"
			    },
			    {
			        "lng": 148.8028, 
			        "lat": 21.0647,
			        "ip": "202.112.23.167",
			        "location": "中国-上海-上海"
			    }
			]
			this.mapInit(this.acts)
			// // 请求解析IP活动
			// this.axios.get(this.baseUrl + "/location", 
			// 	{params: {domain_name: this.targetDomain}})
			// 	.then((response) => {
			// 		this.raw = response.data.result
			// 		// 得到数据后初始化地图
			// 		this.mapInit(this.acts)
			// 	})
			// 	.catch((response) => {
			// 		this.$Message.error("网络错误，请稍后再试！")
			// 	})
		},

		methods: {
			//初始化地图
			mapInit (data) {
				let inmap = new inMap.Map({
					id: "chart",
					skin: "Blueness",
					// 初始地图中心
					center: [107.40, 33.42],
					// 缩放
					zoom: {
						value: 3, 
						show: true, 
						max: 10, 
						min: 2
					}
				})
				let overlay = new inMap.PointOverlay({
					// 气泡提示
					tooltip: {
						show: true,
						formatter: (params) => {
							return (
								"<div><div>IP："+params.ip+"</div><div>地点："+params.name+"</div></div>"
							);
						},
						offsets: {
							top: 15,
							left: 15
						}
					},
					style: {
						normal: {
							backgroundColor: "#FFF",
							size: 4
						},
						mouseOver: {
							backgroundColor: "#FFF",
							borderWidth: 0
						}
					},
					data: data
				})
				inmap.add(overlay)
			}
		}
	}

</script>

<style scoped>
hr{
	width: 650px;
	margin: 10px;
	background-color: #f5f7f9;
}
.label{
	margin: 10px;
	font-size: 16px;
}
.card{
	display: flex;
	flex-direction: column;
	align-items: left;
	margin: 0 10px;
	width: 200px;
	height: 130px;
}
</style>