<template>
	<div>
		<div class="select">
			查询近
			<Select v-model="time_length" style="width:50px;height:20px;margin:0 10px;">
				<Option v-for="item in time_range" :value="item" :key="item">{{ item }}</Option>
			</Select>
			天内的情况
		</div>
		<hr color="#f5f7f9"/>
		<div class="label">概览</div>
		<Card class="card">
            <p slot="title">通信对端 IP 总数</p>
            <p style="font-size:35px;font-weight:bold;margin-left:10px;">{{opposite_count}}</p>
        </Card>

		<div class="label">地理分布 - 按管理归属聚合</div>
		<Table stripe :loading="isLoading" :columns="cols_auth" :data="auth_list"></Table>
		<Page style="margin:10px;" :total="auth_length" :current="auth_page" :page-size="10" show-total @on-change="changeAuthPage"></Page>

		<div class="label">地理分布 - 按地理位置聚合</div>
		<Table stripe :loading="isLoading" :columns="cols_location" :data="location_list"></Table>
		<Page style="margin:10px;" :total="location_length" :current="location_page" :page-size="10" show-total @on-change="changeLocationPage"></Page>

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
				time_length: 1,
				time_range: [1, 2, 3, 4, 5, 6, 7],
				ips: [],					// 目标域名解析IP列表
				raw: [],					// 原始IP活动数据
				opposite_count: 0,
				isLoading: false,
				auth_cluster: [],
				location_cluster: [],
				cols_auth: [{
                    title: "管理归属",
                    key: "auth"
                },
                {
                    title: "通信对端数",
                    key: "count"
                }],
				cols_location: [{
                    title: "位置",
                    key: "location"
                },
                {
                    title: "通信对端数",
                    key: "count"
                }],
                auth_page: 1,
                location_page: 1
			}
		},

		computed: {
			// 按照inMap要求，格式化后的IP活动数据
			acts () {
				let ret = []
				for (var item of this.raw["self"]) {
					let temp = {
				        name: "解析 IP",
				        location: "",
				        ip: item.ip,
				        geometry: {
				            type: 'Point',
				            coordinates: [item.lng, item.lat]
				        },
				        style: {
				            backgroundColor: "#0F0",
				            size: 5,
				        }
				    }
					ret.push(temp)
				}
				for (var item of this.raw["opposite"]) {
					let temp = {
				        name: item.auth,
				        location: item.location,
				        ip: item.ip,
				        geometry: {
				            type: 'Point',
				            coordinates: [item.lng, item.lat]
				        },
				        style: {
				            backgroundColor:"#FF8C00",
				            size: 5,
				        }
				    }
					ret.push(temp)
				}

				return ret
			},
			auth_length () {
				return this.auth_cluster.length
			},
			location_length () {
				return this.location_cluster.length
			},
			auth_list () {
				return this.auth_cluster.slice((this.auth_page - 1) * 10, this.auth_page * 10)
			},
			location_list () {
				return this.location_cluster.slice((this.location_page - 1) * 10, this.location_page * 10)
			}
		},

		created () {
			// 从localStorage中获取解析IP列表
			this.ips = JSON.parse(localStorage.getItem("ips"))
		},

		mounted () {
			// 请求解析IP活动
			this.axios.post(this.baseUrl + "/location", 
				JSON.stringify({ips: this.ips, length: this.time_length}))
				.then((response) => {
					this.raw = response.data.result

					this.opposite_count = this.raw["opposite"].length
					this.cluster()
					// 得到数据后初始化地图
					this.mapInit(this.acts)
				})
				.catch((response) => {
					this.$Message.error("网络错误，请稍后再试！")
				})
		},

		methods: {
			cluster () {
				let auth_set = {}
				let location_set = {}

				for (let item of this.raw["opposite"]) {
					// 按管理归属聚合
					if (item.auth in auth_set) {
						auth_set[item.auth] += 1
					} else {
						auth_set[item.auth] = 1
					}
					// 按地理位置聚合
					if (item.location in location_set) {
						location_set[item.location] += 1
					} else {
						location_set[item.location] = 1
					}
				}

				for (let item in auth_set) {
					this.auth_cluster.push({auth: item, count: auth_set[item]})
				}
				for (let item in location_set) {
					this.location_cluster.push({location: item, count: location_set[item]})
				}
			},
			changeAuthPage (page) {
				this.auth_page = page
			},
			changeLocationPage (page) {
				this.location_page = page
			},
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
								"<div><div>IP："+params.ip+"</div><div>管理归属："+params.name+"</div><div>位置："+params.location+"</div></div>"
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
.select{
	height: 40px;
	display: flex;
	flex-direction: row;
	vertical-align: center;
	line-height: 40px;
	font-size: 15px;
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