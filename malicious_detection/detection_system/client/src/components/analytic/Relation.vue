<template>
	<div>
		<div class="label">
			<Select v-model="selectIndex" style="width:120px;" @on-change="selectChange">
				<Option v-for="item in graphLabel" :value="item.value" :key="item.value">{{ item.label }}</Option>
			</Select>
		</div>
		<hr color="#f5f7f9"/>
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
				targetDomain: "ns2.hostkey.com",
				ips: [],
				steady: {},
				max: {},
				graphLabel: [
					{
						value: 0,
						label: "稳定拓扑"
					},
					{
						value: 1,
						label: "最大拓扑"
					}
				],
				selectIndex: 0,
				chartSteady: null,
				chartMax: null
			}
		},

		computed: {
			showIndex () {
				return (this.selectIndex == 0) ? true : false
			}
		},

		created () {
			this.ips = this.$route.params.ips
			this.targetDomain = this.$route.params.domain_name
		},

		activated () {
			this.chartSteady.resize()
			this.chartMax.resize()
		},

		mounted () {
			let echarts = require("echarts/lib/echarts")
			require('echarts/lib/chart/graph')
			require('echarts/lib/component/legend')
			require('echarts/lib/component/tooltip')
			require('echarts/lib/component/title')
			
			this.chartSteady = echarts.init(document.getElementById("chartSteady"))
			this.chartMax = echarts.init(document.getElementById("chartMax"))

			this.chartSteady.showLoading()
			this.axios.get(this.testUrl + "/topo/steady", 
				{params: {domain_name: this.targetDomain}})
				.then((response) => {
					this.chartSteady.hideLoading()

					this.steady = response.data.result
					let optionSteady = this.graphInit(this.steady)
					this.chartSteady.setOption(optionSteady)

					window.addEventListener("resize", () => {
						this.chartSteady.resize()
					})
				})
				.catch((response) => {
					this.chartSteady.hideLoading()
					this.$Message.error("对方不想说话，所以等会再试吧");
				})

			this.chartMax.showLoading()
			this.axios.get(this.testUrl + "/topo/max", 
				{params: {domain_name: this.targetDomain}})
				.then((response) => {
					this.chartMax.hideLoading()

					this.max = response.data.result
					let option = this.graphInit(this.max)
					this.chartMax.setOption(option)

					window.addEventListener("resize", () => {
						this.chartMax.resize()
					})
				})
				.catch((response) => {
					this.chartMax.hideLoading()
					this.$Message.error("对方不想说话，所以等会再试吧");
				})
		},

		methods: {
			graphInit(data) {
				let graph = data

				let cnt = []
				for (var i of data.nodes) {
					cnt.push(i.count)
				}
				let ind = cnt.indexOf(Math.max(...cnt))

				let categories = [
					{name: "通信对端"}
				]
				for (var item of this.ips) {
					categories.push({name: item})
				}

				graph.nodes.forEach((node, index) => {
					node.itemStyle = null
					node.value = node.count
					node.symbolSize = (Math.log2(node.count) + 1) * 5
					node.label = {
						normal: {
							show: node.symbolSize > 5
						}
					}
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
					legend: [{
						data: categories.map(function (item) {
							return item.name;
						}),
						top: 'bottom'
					}],
					tooltip: {},
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