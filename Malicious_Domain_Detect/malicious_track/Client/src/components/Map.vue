<template>
	<div>
		<div class="label">
			<div>IP活动地理位置分布</div>
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
	import inMap from "inmap/dist/inmap.min.js"
	import { MP } from '../js/map.js'

	export default {
		data () {
			return {
				acts: [
				{
			        lng: 118.8028, 
			        lat: 32.0647,
			        ip: "202.112.23.167",
			        location: "中国-江苏-南京",
			        count: 25
				},
				{
			        lng: 112.95, 
			        lat: 28.43,
			        ip: "118.89.140.118",
			        location: "中国-湖南-长沙",
			        count: 12
				},
				{
			        lng: 113.27, 
			        lat: 21.13,
			        ip: "192.168.1.1",
			        location: "中国-江苏-南京",
			        count: 18
				}
				]

			}
		},

		mounted () {
			// this.$nextTick(function() {
			// 	let that = this
			// 	MP().then(BMap => {
			// 		that.mapInit(that.acts)
			// 	})
			// })
			this.mapInit(this.acts)
		},

		methods: {
			download () {

			},

			//地图数据构造函数
			mapData (lng, lat, ip, location, size) {
				return {
					lng: lng,
					lat: lat,
					ip: ip,
					location: location,
					style: {
						backgroundColor: "#FF8C00",
						size: (size >= 25) ? 13 : (size * 0.4)
					}
				}
			},

			//初始化地图
			mapInit (data) {
				let inmap = new inMap.Map({
					id: "chart",
					skin: "Blueness",
					center: [107.40, 33.42],
					zoom: {
						value: 2, 
						show: true, 
						max: 10, 
						min: 2
					}
				})
				let overlay = new inMap.DotOverlay({
					tooltip: {
						show: true,
						formatter: (params) => {
							return (
								"<div><div>IP："+params.ip+"</div><div>地点："+params.location+"</div></div>"
							);
						},
						offsets: {
							top: 15,
							left: 15
						},
						customClass: "auto"
					},
					style: {
						normal: {
							backgroundColor: "#fff", 
							size: 4
						},
						mouseOver: {
							backgroundColor: "#fff",
							borderWidth: 0
						}
					},
					data: data
				})
				inmap.add(overlay)
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
.auto{
	background-color: #778899;
	border: 0;
	border-radius: 5px;
	color: #fff;
}
</style>