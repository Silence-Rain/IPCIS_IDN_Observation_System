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
				targetDomain: "",			// 要查询的目标域名
				raw: [],					// 原始解析IP活动数据
				countChart: null,			// 活动量趋势echarts对象
				ipChart: null,				// 对端IP数量趋势echarts对象
				entropyChart: null			// 对端IP地理分布熵趋势echarts对象
			}
		},

		computed: {
			// 计算从今天到14天前的日期，作为x轴下标
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
			// 从localStorage中获取目标域名
			this.targetDomain = localStorage.getItem("domain")
		},

		activated () {
			// 页面重新激活时，响应式调整图的尺寸
			this.countChart.resize()
			this.ipChart.resize()
			this.entropyChart.resize()
		},

		mounted () {
			// 导入echarts库和组件
			let echarts = require("echarts/lib/echarts")
			require('echarts/lib/chart/line')
			require('echarts/lib/component/legend')
			require('echarts/lib/component/tooltip')
			require('echarts/lib/component/toolbox')
			require('echarts/lib/component/title')

			// 初始化echarts对象
			this.countChart = echarts.init(document.getElementById("count_chart"))
			this.ipChart = echarts.init(document.getElementById("ip_chart"))
			this.entropyChart = echarts.init(document.getElementById("entropy_chart"))

			// 请求解析IP活动数据
			this.countChart.showLoading()
			this.ipChart.showLoading()
			this.entropyChart.showLoading()
			this.axios.get(this.baseUrl + "/active", 
				{params: {domain_name: this.targetDomain}})
				.then((response) => {
					this.countChart.hideLoading()
					this.ipChart.hideLoading()
					this.entropyChart.hideLoading()

					this.raw = response.data.result

					// 设置趋势图
					let countOption = this.graphInit("IP活动量趋势", this.raw, "count")
					let ipOption = this.graphInit("对端IP数量趋势", this.raw, "opposite_ip_count")
					let entropyOption = this.graphInit("对端IP地理分布熵趋势", this.raw, "ip_geo")
					this.countChart.setOption(countOption)
					this.ipChart.setOption(ipOption)
					this.entropyChart.setOption(entropyOption)

					// 实现响应式调整尺寸
					window.addEventListener("resize", () => {
						this.countChart.resize()
						this.ipChart.resize()
						this.entropyChart.resize()
					})
				})
				.catch((response) => {
					this.countChart.hideLoading()
					this.ipChart.hideLoading()
					this.entropyChart.hideLoading()
					
					this.$Message.error("网络错误，请稍后再试！")
				})
		},

		methods: {
			// 初始化趋势折线图
			graphInit (title, raw, key) {
				let labels = []
				let data = []
				// 从原始数据中取出key对应的维度
				for (var item of raw) {
					labels.push(item.ip)
					data.push({
						name: item.ip,
						type: 'line',
						data: item[key],
						smooth: true
					})
				}

				return {
					title: {
						text: title
					},
					// 提示气泡
					tooltip : {
						trigger: 'axis',
						axisPointer: {
							type: 'cross',
							label: {
								backgroundColor: '#6a7985'
							}
						}
					},
					// 图例
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
					// 下载图片按钮
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