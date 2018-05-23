<template>
	<div>
		<div class="label">
			<div>IP地理位置分布</div>
		</div>
		<hr color="#f5f7f9"/>
		<keep-alive>
			<div id="chart" style="width:100%;height:500px;"></div>
		</keep-alive>
	</div>
</template>

<script>
	import inMap from "inmap/dist/inmap.min.js"

	export default {
		data () {
			return {
				targetDomain: "",
				raw: [],
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
			this.targetDomain = this.$route.params.domain_name
		},

		mounted () {
			this.axios.get(this.testUrl + "/location", 
				{params: {domain_name: this.targetDomain}})
				.then((response) => {
					this.raw = response.data.result
					this.mapInit(this.acts)
				})
				.catch((response) => {
					this.$Message.error("网络错误，请稍后再试！")
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
						value: 3, 
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
	margin: 5px;
	font-size: 18px;
	font-weight: bold;
}
</style>