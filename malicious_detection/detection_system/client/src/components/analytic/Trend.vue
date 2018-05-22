<template>
	<div>
		<div class="title">IP计算活跃度概览</div>
		<div class="cards" v-for="item in raw">
			<div class="card">
				<p style="font-size:35px;font-weight:bold;">{{item.active}}</p>
				<p>{{item.ip}}计算活跃度</p>
			</div>
		</div>
		<hr color="#f5f7f9"/>
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
				targetDomain: "ns2.hostkey.com",
				raw: []
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

		created () {
			this.targetDomain = this.$route.params.domain_name
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

			countChart.showLoading()
			ipChart.showLoading()
			entropyChart.showLoading()

			this.axios.get(this.testUrl + "/active", 
				{params: {domain_name: "ns2.hostkey.com"}})
				.then((response) => {
					countChart.hideLoading()
					ipChart.hideLoading()
					entropyChart.hideLoading()

					this.raw = response.data.result

					let countOption = this.graphInit("IP活动量趋势", this.raw, "count")
					let ipOption = this.graphInit("对端IP数量趋势", this.raw, "opposite_ip_count")
					let entropyOption = this.graphInit("对端IP地理分布熵趋势", this.raw, "ip_geo")

					countChart.setOption(countOption)
					ipChart.setOption(ipOption)
					entropyChart.setOption(entropyOption)

					window.addEventListener("resize", () => {
						countChart.resize()
						ipChart.resize()
						entropyChart.resize()
					})
				})
				.catch((response) => {
					countChart.hideLoading()
					ipChart.hideLoading()
					entropyChart.hideLoading()
					
					this.$Message.error("对方不想说话，所以等会再试吧")
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
.title{
	font-size: 18px;
	font-weight: bold;
	margin: 0 5px;
}
.cards{
	display: flex;
	flex-direction: row;
	padding: 20px;
}
.card{
	display: flex;
	flex-direction: column;
	align-items: left;
	margin: 0 10px;
}
</style>