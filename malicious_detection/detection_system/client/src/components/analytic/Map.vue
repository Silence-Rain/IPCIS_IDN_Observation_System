<template>
	<div>
		<div class="label">
			<div>IP活动地理位置分布</div>
		</div>
		<hr color="#f5f7f9"/>
		<keep-alive>
			<div id="chart" style="width:650px;height:500px;"></div>
		</keep-alive>
	</div>
</template>

<script>
	import inMap from "inmap/dist/inmap.min.js"

	export default {
		data () {
			return {
				targetDomain: "ns2.hostkey.com",
				raw: [
				// {
			 //        lng: 118.8028, 
			 //        lat: 32.0647,
			 //        ip: "202.112.23.167",
			 //        location: "中国-江苏-南京",
			 //        count: [25,12,21]
				// },
				// {
			 //        lng: 112.95, 
			 //        lat: 28.43,
			 //        ip: 2449492302,
			 //        location: "中国-湖南-长沙",
			 //        count: [12,10,9]
				// },
				// {
			 //        lng: 113.27, 
			 //        lat: 21.13,
			 //        ip: "192.168.1.1",
			 //        location: "中国-江苏-南京",
			 //        count: [18,42,24]
				// }
				],
				ips: []
			}
		},

		computed: {
			acts () {
				let ret = []
				for (var item of this.raw) {
					let temp = item
					temp["count"] = item.count.reduce((acc, val) => {
						return acc + val 
					})
					temp["style"] = {size: Math.log2(temp.count) + 1}
					temp["style"]["backgroundColor"] = (this.ips.indexOf(item.ip) == -1)
						? "#FF8C00" : "#0F0"
					ret.push(temp)
				}
				return ret
			}
		},

		created () {
			this.ips = this.$route.params.ips
		},

		mounted () {
			// this.targetDomain = this.$route.params.domain_name
			
			this.axios.get("https://118.89.140.118:8888/location", 
				{domain_name: "ns2.hostkey.com"})
				.then((response) => {
					this.raw = response.data.result
					this.mapInit(this.acts)
				})
				.catch((response) => {
					this.$Message.error("对方不想说话，所以等会再试吧")
				})
			
		},

		methods: {
			//初始化地图
			mapInit (data) {
				let inmap = new inMap.Map({
					id: "chart",
					skin: "Blueness",
					center: [107.40, 33.42],
					zoom: {
						value: 4, 
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
						}
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
hr{
	width: 650px;
	margin: 10px 0;
	background-color: #f5f7f9;
}
.label{
	display: flex;
	flex-direction: row;
	align-items: center;
	width: 650px;
    margin: 10px;
    font-size: 16px;
}
</style>