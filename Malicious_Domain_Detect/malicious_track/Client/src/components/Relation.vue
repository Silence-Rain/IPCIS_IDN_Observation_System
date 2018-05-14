<template>
	<div>
		<div class="label">
			<div>目标IP地址通信活动关系</div>
			<Button type="primary" class="btn" @click="download">
				<Icon type="ios-cloud-download" size="15" color="#fff"></Icon>
				下载
			</Button>
		</div>
		<keep-alive>
			<div id="chart" style="width:500px;height:500px;"></div>
		</keep-alive>
	</div>
</template>

<script>
	export default {
		data () {
			return {
				graph: {
					nodes: [
						{
							id: 0,
							name: "118.89.140.118",
							count: 100
						},
						{
							id: 1,
							name: "45.77.86.38",
							count: 50
						},
						{
							id: 2,
							name: "test",
							count: 30
						}
					],
					links: [
						{
							source: 0,
							target: 1
						},
						{
							source: 1,
							target: 2
						}
					]
				}
			}
		},

		mounted () {

			let echarts = require("echarts/lib/echarts")
			require('echarts/lib/chart/graph')
			let chart = echarts.init(document.getElementById("chart"))

			let option = {
				title: {
					text: '目标IP地址通信活动关系图',
					subtext: 'Circular layout',
					top: 'bottom',
					left: 'right'
				},
				animationDurationUpdate: 1500,
				animationEasingUpdate: 'quinticInOut',
				series: [
					{
						name: '通信节点',
						type: 'graph',
						layout: 'circular',
						circular: {
							rotateLabel: true
						},
						data: this.graph.nodes,
						links: this.graph.links,
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
			chart.setOption(option)

		 	// chart.showLoading()
			// this.axios.get("localhost:8888/topo/steady")
			// 	.then((response) => {
			// 		chart.hideLoading()
			// 		console.log(response)
			// 		let option = graphInit(response)			
			// 		chart.setOption(option);
			// 	})
			// 	.catch((response) => {
			// 		chart.hideLoading()
			// 		alert("加载错误，请稍后再试！")
			// 	})

		},

		methods: {
			download () {
				
			},

			graphInit(data) {
				let graph = data
				let categories = [
					{name: data.nodes[0].name}, 
					{name: data.nodes[0].name+"对端"}
				]

				graph.nodes.forEach(function (node, index) {
					node.itemStyle = null
					node.value = node.count
					node.symbolSize = node.count / 2
					node.label = {
						normal: {
							show: node.symbolSize > 1
						}
					}
					node.category = (index == 0) ? 0 : 1
				})

				let option = {
					title: {
						text: '目标IP地址通信活动关系图',
						top: 'bottom',
						left: 'right'
					},
					legend: [{
						data: categories.map((item) => {
							return item.name;
						})
					}],
					animationDurationUpdate: 1500,
					animationEasingUpdate: 'quinticInOut',
					series : [
						{
							name: '通信节点',
							type: 'graph',
							layout: 'circular',
							circular: {
								rotateLabel: true
							},
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
			}
		}
	}
</script>

<style scoped>
.label{
	display: flex;
	flex-direction: row;
	align-items: center;
	margin: 10px;
	font-size: 16px;
}
.btn{
	width: 70px;
	height: 30px;
	margin-left: 50px;
	font-size: 12px;
}
</style>