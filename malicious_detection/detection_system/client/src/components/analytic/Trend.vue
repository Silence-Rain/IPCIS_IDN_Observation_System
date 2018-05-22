<template>
	<div>
		<keep-alive>
			<div id="count_chart" style="width:100%;height:400px;"></div>
		</keep-alive>
			<hr color="#f5f7f9"/>
		<keep-alive>
			<div id="ip_chart" style="width:100%;height:400px;"></div>
		</keep-alive>
			<hr color="#f5f7f9"/>
		<keep-alive>
			<div id="entropy_chart" style="width:100%;height:400px;"></div>
		</keep-alive>
	</div>
</template>

<script>
	export default {
		data () {
			return {
				raw: [
					{
						ip: "118.89.140.118",
						active: 90,
						count: [220, 182, 191, 234, 290, 330, 310, 120, 132, 101, 134, 90, 230, 210],
						opposite_ip_count: [820, 932, 901, 934, 1290, 1330, 1320, 820, 932, 901, 934, 1290, 1330, 1320],
						ip_geo_entropy: [1.1, 2.2, 1.2, 2.3, 1.3, 2.4, 1.4, 2.5, 1.5, 2.6, 1.6, 2.7, 1.7, 2.8, 1.8, 2.9]
					}
				]
			}
		},

		computed: {
			timeLabels () {
				let cur = Date.parse(new Date())
				let ret = []
				for (var i = 0; i < 14; i++) {
					let dt = new Date(cur - i * 86400000)
					ret.unshift(dt.toLocaleDateString().slice(5))
				}
				return ret
			}
		},

		mounted () {
			let echarts = require("echarts/lib/echarts")
			require('echarts/lib/chart/line')
			require('echarts/lib/component/legend')
			require('echarts/lib/component/tooltip')
			require('echarts/lib/component/toolbox')
			require('echarts/lib/component/title')

			let countChart = echarts.init(document.getElementById("count_chart"))
			let ipChart = echarts.init(document.getElementById("ip_chart"))
			let entropyChart = echarts.init(document.getElementById("entropy_chart"))

			let countOption = this.graphInit("IP活动量趋势", this.raw, "count")
			let ipOption = this.graphInit("对端IP数量趋势", this.raw, "opposite_ip_count")
			let entropyOption = this.graphInit("对端IP地理分布熵趋势", this.raw, "ip_geo_entropy")

			countChart.setOption(countOption)
			ipChart.setOption(ipOption)
			entropyChart.setOption(entropyOption)

			window.addEventListener("resize", () => {
				countChart.resize()
				ipChart.resize()
				entropyChart.resize()
			})
		},

		methods: {
			graphInit (title, raw, key) {
				let labels = []
				let data = []

				for (var item of raw) {
					labels.push(item.ip)
					data.push({
			            name: item.ip,
			            type: 'line',
			            data: item[key]
			        })
				}

				return {
				    title: {
				        text: title
				    },
				    tooltip : {
				        trigger: 'axis',
				        axisPointer: {
				            type: 'cross',
				            label: {
				                backgroundColor: '#6a7985'
				            }
				        }
				    },
				    legend: {
				        data: labels,
				        top: "2%"
				    },
				    grid: {
				        left: '3%',
				        right: '4%',
				        bottom: '3%',
				        containLabel: true
				    },
				    toolbox: {
				        feature: {
				            saveAsImage: {}
				        },
				        right: "5%"
				    },
				    xAxis: [
				        {
				            type: 'category',
				            boundaryGap: false,
				            data: this.timeLabels
				        }
				    ],
				    yAxis: [
				        {
				            type: 'value'
				        }
				    ],
				    series: data
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
</style>