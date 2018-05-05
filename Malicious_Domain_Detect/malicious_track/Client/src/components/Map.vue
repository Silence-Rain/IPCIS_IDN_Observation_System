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
	import {MP} from '../js/map.js'
	import axios from 'axios'

	export default {
		data () {
			return {
				inMap: null,
				acts: [
				{
					from: {
						city: "118.89.140.118",
						lnglat: [112.95, 28.43]
					},
					to: {
						city: "211.65.193.23",
						lnglat: [121.48, 31.22]
					}
				},
				{
					from: {
						city: "118.89.140.118",
						lnglat: [112.95, 28.43]
					},
					to: {
						city: "192.168.1.1",
						lnglat: [113.27, 21.13]
					}
				},
				{
					from: {
						city: "202.112.23.167",
						lnglat: [116.41, 39.91]
					},
					to: {
						city: "118.89.140.118",
						lnglat: [112.95, 28.43]
					}
				}
				]

			}
		},

		created () {
			// let url = "http://211.65.197.210:8080/IPCIS/activityDatabase/?" + 
			// 		"IpSets=211.65.193.193:32-211.65.197.210:32-202.112.23.167:32-211.65.192.172:32" + 
			// 		"&TableName=2018-05-03&Mode=1"

			// axios.get(url)
			// 	.then((response) => {
			// 		console.log(response);
			// 	})
			// 	.catch((response) => {
			// 		console.log("000");
			// 	});

			// this.$nextTick(() => {
			// 	var that = this

			// 	MP().then(BMap => {
			// 		this.inMap = new inMap.Map({
			// 			id: "chart",
			// 			skin: "Blueness",
			// 			center: [107.40, 33.42],
			// 			zoom: {
			// 				value: 4, 
			// 				show: true, 
			// 				max: 13, 
			// 				min: 4
			// 			},
			// 		})

			// 		let overlay = new inMap.MoveLineOverlay({
			// 			data: this.acts
			// 		});

			// 		console.log(this.inMap)

			// 		this.inMap.add(overlay)
			// 		console.log(this.inMap)
			// 	})
			// })
		},

		mounted () {
			var that = this
			this.$nextTick(() => {

				MP().then(BMap => {
					that.inMap = new inMap.Map({
						id: "chart",
						skin: "Blueness",
						center: [107.40, 33.42],
						zoom: {
							value: 2, 
							show: true, 
							max: 10, 
							min: 2
						},
					})

					let overlay = new inMap.MoveLineOverlay({
						data: that.acts
					});

					that.inMap.add(overlay)
					console.log(that.inMap === this.inMap)
				})
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