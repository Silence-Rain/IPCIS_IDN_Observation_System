<template>
	<div>
		<div class="select">
			查询近
			<Select v-model="time_length" style="width:50px;height:20px;margin:0 10px;" @on-change="selectChange">
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

		<div>
			<keep-alive>
				<div id="chartMax" class="chart"></div>
			</keep-alive>
		</div>
	</div>
</template>

<script>
	export default {
		data () {
			return {
				targetDomain: "",			// 要查询的目标域名
				ips: [],					// 目标域名解析IP列表
				max: {},					// 最大拓扑图数据
				chartMax: null,				// 最大拓扑echarts对象
				time_length: 1,
				time_range: [1, 2, 3, 4, 5, 6, 7],
				graphData: {nodes: [], links: []}
			}
		},

		computed: {
			opposite_count () {
				return this.graphData.nodes.length - this.ips.length
			}
		},

		created () {
			// 从localStorage中获取目标域名和解析IP列表
			this.ips = JSON.parse(localStorage.getItem("ips"))
			this.targetDomain = localStorage.getItem("domain")
		},

		// activated () {
		// 	// 页面重新激活时，响应式调整图的尺寸
		// 	this.chartMax.resize()
		// },

		mounted () {
			// 导入echarts库和组件
			let echarts = require("echarts/lib/echarts")
			require('echarts/lib/chart/graph')
			require('echarts/lib/component/legend')
			require('echarts/lib/component/tooltip')
			require('echarts/lib/component/title')
			
			// 初始化echarts对象
			this.chartMax = echarts.init(document.getElementById("chartMax"))

			// 请求最大拓扑
			// 设置并展示最大拓扑图
			this.chartMax.showLoading()
			this.requestIPRecord()
		},

		methods: {
			requestIPRecord () {
				this.axios.post(this.baseUrl + "/topo", 
				JSON.stringify({ips: this.ips, length: this.time_length}))
				.then((response) => {
					this.chartMax.hideLoading()

					// 设置最大拓扑图
					this.graphData = response.data.result
					let option = this.graphInit(this.graphData)
					this.chartMax.setOption(option)

					// 实现响应式调整尺寸
					window.addEventListener("resize", () => {
						this.chartMax.resize()
					})
				})
				.catch((response) => {
					this.chartMax.hideLoading()
					this.$Message.error("网络错误，请稍后再试！")
					console.log(response)
				})
			},
			// 初始化Les Miserable拓扑图
			graphInit(data) {
				let graph = data

				// 设置图例：解析IP，通信对端
				let categories = [
					{name: "通信对端"}
				]
				for (var item of this.ips) {
					categories.push({name: item})
				}

				// 为每个图节点添加属性
				graph.nodes.forEach((node, index, arr) => {
					node.itemStyle = null
					node.symbolSize = (arr.length > 120) ? 2 : 5
					node.label = {
						normal: {
							show: this.ips.indexOf(node.name) >= 0
						}
					}
					// 为每个节点分配图例
					if (this.ips.indexOf(node.name) == -1) {
						node.category = 0
					}
					else {
						node.category = this.ips.indexOf(node.name) + 1
					}
				})

				let option = {
					title: {
						text: "目标IP通信活动关系"
					},
					// 图例
					legend: {
				        type: 'scroll',
				        orient: 'vertical',
				        right: 10,
				        top: 20,
				        bottom: 20,
				        data: categories.map(function (item) {
							return item.name;
						})
				    },
					// 提示气泡
					tooltip: {
				    },
					// 下载图片按钮
					toolbox: {
						feature: {
							saveAsImage: {}
						},
						right: "5%"
					},
					animationDurationUpdate: 1500,
					animationEasingUpdate: 'quinticInOut',
					series : [
						{
							name: '通信节点',
							type: 'graph',
							layout: 'circular',
							data: graph.nodes,
							links: graph.links,
							categories: categories,
							roam: true,
							label: {
								normal: {
									position: 'right',
									formatter: '{b}'
								}
							},
							lineStyle: {
								normal: {
									color: 'source',
									curveness: 0.3,
									width: 2
								}
							}
						}
					]
				}

				return option
			},

			// 选择框选项变化时，响应式调整尺寸
			selectChange (value) {
				this.requestIPRecord()
				this.$nextTick(() => {	
					this.chartMax.resize()
				})
			},

		}
	}
</script>

<style scoped>
hr{
	margin: 10px 0;
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
.subtitle{
	line-height: 36px;
	margin-left: 20px;
}
.slider{
	width: 240px;
	margin: 0 10px;
}
.chart{
	width: 80%;
	height: 500px;
	margin: 20px;
}
</style>