<template>
	<div>
		<keep-alive>
			<div id="chart" style="width:600px;height:400px;"></div>
		</keep-alive>
	</div>
</template>

<script>
	export default {
		data () {
			return {

			}
		},

		mounted () {
			let echarts = require("echarts/lib/echarts")
			require('echarts/lib/chart/line')
			require('echarts/lib/component/tooltip')
			require('echarts/lib/component/legend')

			let chart = echarts.init(document.getElementById("chart"))
			chart.setOption({
				title: {
					text: "近7天IP流量趋势"
				},
				xAxis: {
			        type: 'category',
			        data: ['4/17', '4/18', '4/19', '4/20', '4/21', '4/22', '4/23']
			    },
			    yAxis: {
			        type: 'value'
			    },
			    series: [{
			        data: [50, 65, 60, 80, 45, 70, 100],
			        type: 'line'
			    }]
			})
		}
	}
</script>

<style scoped>

</style>