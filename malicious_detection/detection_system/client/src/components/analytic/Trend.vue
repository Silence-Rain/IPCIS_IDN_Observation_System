<template>
	<div>
		<div class="label">
			<div>近7天IP流量趋势</div>
			<Button type="primary" class="btn" @click="download">
				<Icon type="ios-cloud-download" size="15" color="#fff"></Icon>
				下载
			</Button>
		</div>
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

			let chart = echarts.init(document.getElementById("chart"))
			chart.setOption({
				xAxis: {
			        type: 'category',
			        boundaryGap: false,
			        data: ['4/17', '4/18', '4/19', '4/20', '4/21', '4/22', '4/23']
			    },
			    yAxis: {
			        type: 'value'
			    },
			    series: [{
			        data: [50, 65, 60, 80, 45, 70, 100],
			        type: 'line',
			        areaStyle: {color: "#F4A460"}
			    }]
			})
		},

		methods: {
			download () {
				
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