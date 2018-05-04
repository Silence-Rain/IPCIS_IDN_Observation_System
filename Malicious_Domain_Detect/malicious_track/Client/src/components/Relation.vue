<template>
	<div>
		<div class="label">
			<div>通信对象关系</div>
			<Button type="primary" class="btn" @click="download">
				<Icon type="ios-cloud-download" size="15" color="#fff"></Icon>
				下载
			</Button>
		</div>
		<keep-alive>
			<div id="chart" style="width:400px;height:400px;"></div>
		</keep-alive>
	</div>
</template>

<script>
	export default {
		data () {
			return {
				data: [
                {
                    name: '118.89.140.118',
                    value: 6,
                    children: [
                        {
                            name: '211.65.193.23',
                            value: 4
                        },
                        {
                            name: '192.168.1.1',
                            value: 4
                        },
                        {
                            name: '202.112.23.167',
                            value: 4
                        }
                    ]
                }
            ]
			}
		},

		mounted () {
			let echarts = require("echarts/lib/echarts")
			require('echarts/lib/chart/tree')

			let chart = echarts.init(document.getElementById("chart"))
			chart.setOption({
				series: [
		         	{
		                type: 'tree',

		                data: this.data,

		                top: '1%',
		                left: '7%',
		                bottom: '1%',
		                right: '20%',

		                symbolSize: 7,

		                label: {
		                    normal: {
		                        position: 'left',
		                        verticalAlign: 'middle',
		                        align: 'right',
		                        fontSize: 9
		                    }
		                },

		                leaves: {
		                    label: {
		                        normal: {
		                            position: 'right',
		                            verticalAlign: 'middle',
		                            align: 'left'
		                        }
		                    }
		                },

		                expandAndCollapse: true,
		                animationDuration: 550,
		                animationDurationUpdate: 750
		            }
		        ]
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