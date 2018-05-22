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
				// steady: {"nodes": [{"id": 0, "name": 3396847626, "count": 133}, {"id": 1, "name": 2449492302, "count": 169}], "links": [{"source": 1, "target": 0}]},
				// max: {"nodes": [{"id": 0, "name": 3544580385, "count": 1}, {"id": 1, "name": 3396862564, "count": 2}, {"id": 2, "name": 3396343685, "count": 1}, {"id": 3, "name": 3396804614, "count": 7}, {"id": 4, "name": 3525073927, "count": 1}, {"id": 5, "name": 3396343689, "count": 1}, {"id": 6, "name": 3396862634, "count": 9}, {"id": 7, "name": 3396847626, "count": 133}, {"id": 8, "name": 3396862635, "count": 2}, {"id": 9, "name": 3396816906, "count": 1}, {"id": 10, "name": 2449492302, "count": 169}, {"id": 11, "name": 3396804620, "count": 11}], "links": [{"source": 10, "target": 8}, {"source": 10, "target": 7}, {"source": 10, "target": 6}, {"source": 10, "target": 9}, {"source": 10, "target": 2}, {"source": 10, "target": 1}, {"source": 10, "target": 4}, {"source": 10, "target": 3}, {"source": 10, "target": 11}, {"source": 10, "target": 0}, {"source": 10, "target": 5}]},
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
				chartMax: null,
				ips: []
			}
		},

		computed: {
			showIndex () {
				return (this.selectIndex == 0) ? true : false
			}
		},

		created () {
			this.ips = this.$route.params.ips
		},

		mounted () {
			// this.targetDomain = this.$route.params.domain_name

			let echarts = require("echarts/lib/echarts")
			require('echarts/lib/chart/graph')
			require('echarts/lib/component/legend')
			require('echarts/lib/component/tooltip')
			require('echarts/lib/component/title')
			this.chartSteady = echarts.init(document.getElementById("chartSteady"))
			this.chartMax = echarts.init(document.getElementById("chartMax"))

			this.axios.get(this.testUrl + "/topo/steady", 
				{domain_name: this.targetDomain})
				.then((response) => {
					this.steady = response.data.result

					// let optionMax = this.graphInit(this.max)
					// this.chartMax.setOption(optionMax)
					let optionSteady = this.graphInit(this.steady)
					this.chartSteady.setOption(optionSteady)

					window.addEventListener("resize", () => {
						this.chartSteady.resize()
						this.chartMax.resize()
					})
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
				if (value == 1) {
					if (!this.max.hasOwnProperty("nodes")) {
						this.chartMax.showLoading()
						this.axios.get(this.testUrl + "/topo/max", 
							{domain_name: this.targetDomain})
							.then((response) => {
								this.chartMax.hideLoading()
								this.max = response.data.result
								let option = this.graphInit(this.max)
								chartMax.setOption(option);
							})
							.catch((response) => {
								this.chartMax.hideLoading()
								this.$Message.error("对方不想说话，所以等会再试吧");
							})
					}
				}
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