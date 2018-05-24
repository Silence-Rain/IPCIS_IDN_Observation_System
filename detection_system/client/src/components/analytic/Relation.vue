<template>
	<div>
		<div class="label">
			<Select v-model="selectIndex" style="width:120px;" @on-change="selectChange">
				<Option v-for="item in graphLabel" :value="item.value" :key="item.value">{{ item.label }}</Option>
			</Select>
		</div>
		<hr color="#f5f7f9"/>
		<!-- 根据选择框内容展示稳定/最大拓扑 -->
		<div v-show="showIndex">
			<keep-alive>
				<div id="chartSteady" class="chart"></div>
			</keep-alive>
		</div>
		<div v-show="!showIndex">
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
				steady: {},					// 稳定拓扑图数据
				max: {},					// 最大拓扑图数据
				selectIndex: 0,				// 选择器选中项
				chartSteady: null,			// 稳定拓扑echarts对象
				chartMax: null,				// 最大拓扑echarts对象
				graphLabel: [
					{
						value: 0,
						label: "稳定拓扑"
					},
					{
						value: 1,
						label: "最大拓扑"
					}
				]
			}
		},

		computed: {
			// 根据选择框内容展示稳定/最大拓扑
			showIndex () {
				return (this.selectIndex == 0) ? true : false
			}
		},

		created () {
			// 从localStorage中获取目标域名和解析IP列表
			this.ips = JSON.parse(localStorage.getItem("ips"))
			this.targetDomain = localStorage.getItem("domain")
		},

		activated () {
			// 页面重新激活时，响应式调整图的尺寸
			this.chartSteady.resize()
			this.chartMax.resize()
		},

		mounted () {
			// 导入echarts库和组件
			let echarts = require("echarts/lib/echarts")
			require('echarts/lib/chart/graph')
			require('echarts/lib/component/legend')
			require('echarts/lib/component/tooltip')
			require('echarts/lib/component/title')
			
			// 初始化echarts对象
			this.chartSteady = echarts.init(document.getElementById("chartSteady"))
			this.chartMax = echarts.init(document.getElementById("chartMax"))

			// 请求稳定拓扑
			// 设置并展示稳定拓扑图
			this.chartSteady.showLoading()
			this.axios.get(this.baseUrl + "/topo/steady", 
				{params: {domain_name: this.targetDomain}})
				.then((response) => {
					this.chartSteady.hideLoading()

					// 设置稳定拓扑图
					this.steady = response.data.result
					let optionSteady = this.graphInit(this.steady)
					this.chartSteady.setOption(optionSteady)

					// 服务器端自动化存储生成的拓扑
					// 延时1s已保证动画效果完成，图完全加载
					setTimeout(() => {
						var img = this.chartSteady.getDataURL()
						this.axios.post(this.baseUrl + "/saveImage",
							JSON.stringify({img: img}))
					}, 1000)
					
					// 实现响应式调整尺寸
					window.addEventListener("resize", () => {
						this.chartSteady.resize()
					})
				})
				.catch((response) => {
					this.chartSteady.hideLoading()
					this.$Message.error("网络错误，请稍后再试！")
					console.log(response)
				})

			// 请求最大拓扑
			// 设置并展示最大拓扑图
			this.chartMax.showLoading()
			this.axios.get(this.baseUrl + "/topo/max", 
				{params: {domain_name: this.targetDomain}})
				.then((response) => {
					this.chartMax.hideLoading()

					// 设置最大拓扑图
					this.max = response.data.result
					let option = this.graphInit(this.max)
					this.chartMax.setOption(option)

					// 服务器端自动化存储生成的拓扑
					// 延时1s已保证动画效果完成，图完全加载
					setTimeout(() => {
						var img = this.chartSteady.getDataURL()
						this.axios.post(this.baseUrl + "/saveImage",
							JSON.stringify({img: img}))
					}, 1000)

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

		methods: {
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
				graph.nodes.forEach((node, index) => {
					node.itemStyle = null
					node.value = node.count
					// 根据活动计数决定节点尺寸
					node.symbolSize = (Math.log2(node.count) + 1) * 5
					node.label = {
						normal: {
							show: node.symbolSize > 5
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
					legend: [{
						data: categories.map(function (item) {
							return item.name;
						}),
						top: 'bottom'
					}],
					// 提示气泡
					tooltip: {},
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
									curveness: 0.3
								}
							}
						}
					]
				}

				return option
			},

			// 选择框选项变化时，响应式调整尺寸
			selectChange (value) {
				this.$nextTick(() => {	
					this.chartMax.resize()
					this.chartSteady.resize()
				})
			}
		}
	}
</script>

<style scoped>
hr{
	margin: 10px 0;
	background-color: #f5f7f9;
}
.chart{
	width: 80%;
	height: 500px;
	margin: 20px;
}
</style>