<template>
	<div class="layout">
		<Layout>
			<!-- 顶部导航栏 -->
			<Header>
				<Menu mode="horizontal" theme="dark">
					<div class="nav-head">
						<div class="nav-head-logo">IPCIS</div>
						<div class="nav-head-title">
							<div>国际化域名累计观测系统</div>
							<div>Accumulative International Domain Name Observation System</div>
						</div>
					</div>
				</Menu>
			</Header>

			<Layout>
				<Content class="content">
					<Row>
						<Col span="11">
							<Card class="card">
								<p slot="title">已收集国际化域名列表（点击查看详情）</p>
								<div class="list-action">
									<Input class="searchbar" v-model="searchTarget" icon="search" placeholder="搜索域名，语种"></Input>
									<Button type="primary" @click="exportData"><Icon type="ios-download-outline"></Icon>导出为csv</Button>
								</div>
								<Table style="margin:10px" stripe :loading="isLoading" :columns="tableHeader" :data="showList" @on-row-click="redirectTo" ref="idns"></Table>
								<Page style="margin:10px;" :total="length" :current="curPage" :page-size="10" show-total @on-change="changePage"></Page>
							</Card>
						</Col>
						<Col span="11" offset="1">
							<Card class="card">
								<p slot="title">语种分布比例概览</p>
								<keep-alive>
									<div id="distribution_pie" style="width:100%;height:400px;"></div>
								</keep-alive>
							</Card>
						</Col>
					</Row>

					<Row>
						<Col span="23">
							<Card class="card">
								<p slot="title">语种分布数量概览</p>
								<keep-alive>
									<div id="distribution_bar" style="width:100%;height:550px;"></div>
								</keep-alive>
							</Card>
						</Col>
					</Row>

					<Row>
						<Col span="23">
							<Card class="card">
								<p slot="title">地理分布概览</p>
								<div class="select">
									选择语种：
									<Select v-model="lang" style="width:150px;height:20px;margin:0 10px;" @on-change="selectChange" filterable>
										<Option v-for="item in langs" :value="item" :key="item">{{ item }}</Option>
									</Select>
								</div>
								<keep-alive>
									<div id="geo_map" style="width:100%;height:550px;"></div>
								</keep-alive>
							</Card>
						</Col>
					</Row>

				</Content>
			</Layout>

			<!-- 底部footer -->
			<Footer class="footer">
				<div>
					2018 &copy; Silence-Rain<span>联系方式：daniel.s.mo503@gmail.com</span>
				</div>
			</Footer>
		</Layout>
	</div>
</template>

<script>
	import inMap from "inmap/dist/inmap.min.js"

	export default {

		data () {
			return {
				searchTarget: "",			// 要查询的目标域名
				isLoading: false,			// 表格loading状态
				curPage: 1,					// 当前页数
				newDomain: "",				// 新增域名
				rawList: [],				// 所有已知域名列表
				rawActs: [],				// 所有已知域名活动数据
				distributionPie: null,
				distributionBar: null,
				langs: [],
				lang: "全部语种",
				tableHeader: [
					{
						title: "域名",
						key: "domain_name",
						render: (h, params) => {
							return h('div', [
								h('a', {
									style: {
										textDecoration: "underline"
									}
								}, params.row.domain_name)
							])
						}
					},
					{
						title: "语种",
						key: "lang"
					}
				]
			}
		},
		computed: {
			// 已知恶意域名列表长度
			length () {
				return this.list.length
			},
			// 根据筛选条件得到的实际列表
			// 根据搜索框中内容，正则匹配查询结果
			list () {
				if (this.searchTarget == "") {
					return this.rawList
				} else {
					let ret = []
					// 搜索栏输入的是语种内容
					if (/(文|语)$/.test(this.searchTarget)) {
						for (let i of this.rawList) {
							if (this.regMatch(this.searchTarget, i.lang)) {
								ret.push(i)
							}
						}
					} else {
						for (let i of this.rawList) {
							if (this.regMatch(this.searchTarget, i.domain_name)) {
								ret.push(i)
							}
						}
					}

					this.curPage = 1
					return (ret.length == 0) ? [] : ret
				}
			},
			// 当前显示的内容
			// 根据选择的页数展示10条记录
			showList () {
				return this.list.slice((this.curPage - 1) * 10, this.curPage * 10)
			},
			// 按照inMap要求，格式化后的IP活动数据
			acts () {
				let ret = []
				for (var item of this.rawActs["self"]) {
					let temp = {
						auth: item.auth,
						domain: item.domain,
						location: item.location,
						ip: item.ip,
						geometry: {
							type: 'Point',
							coordinates: [item.lng, item.lat]
						},
						style: {
							backgroundColor: "#0F0",
							size: 5,
						}
					}
					ret.push(temp)
				}

				return ret
			}
		},
		activated () {
			this.distributionPie.resize()
		},
		mounted () {
			// 导入echarts库和组件
			let echarts = require("echarts/lib/echarts")
			require('echarts/lib/chart/pie')
			require('echarts/lib/chart/bar')
			require('echarts/lib/component/legend')
			require('echarts/lib/component/legend/ScrollableLegendModel')
			require('echarts/lib/component/legend/ScrollableLegendView')
			require('echarts/lib/component/legend/scrollableLegendAction')
			require('echarts/lib/component/tooltip')

			localStorage.clear()

			this.distributionPie = echarts.init(document.getElementById("distribution_pie"))
			this.distributionBar = echarts.init(document.getElementById("distribution_bar"))
			
			// 请求已知域名列表
			this.isLoading = true
			this.distributionPie.showLoading()
			this.distributionBar.showLoading()

			this.axios.get(this.baseUrl + "/list")
				.then((response) => {
					this.isLoading = false
					this.distributionPie.hideLoading()
					this.distributionBar.hideLoading()

					this.langs = ["全部语种"].concat(response.data.result.all_lang)
					for (var item of response.data.result.res) {
						this.rawList.push(this.formatter(item))
					}

					let pieOption = this.pieInit(this.rawList)
					let barOption = this.barInit(this.rawList)
					this.distributionPie.setOption(pieOption)
					this.distributionBar.setOption(barOption)

					// 实现响应式调整尺寸
					window.addEventListener("resize", () => {
						this.distributionPie.resize()
						this.distributionBar.resize()
					})
				})
				.catch((response) => {
					this.isLoading = false
					this.distributionPie.hideLoading()
					this.distributionBar.hideLoading()
					console.log(response)
					this.$Message.error("网络错误，请稍后再试！");
				})

			// 请求解析IP活动
			this.requestIPRecord()			
		},
		methods: {
			requestIPRecord () {
				this.axios.post(this.baseUrl + "/location_all", 
					JSON.stringify({lang: this.lang || "全部语种" }))
					.then((response) => {
						this.rawActs = response.data.result
						// 得到数据后初始化地图
						this.mapInit(this.acts)
					})
					.catch((response) => {
						this.$Message.error("网络错误，请稍后再试！")
					})
			},
			exportData () {
				this.$refs.idns.exportCsv({
					filename: `已知国际化域名-${this.searchTarget || "全部语种"}`,
					columns: this.tableHeader,
					data: this.list
				})
			},
			// 初始化饼状图
			pieInit (data) {
				let legendData = []
				let seriesData = []
				let seriesDataRaw = {}
				let selected = {}

				for (let i in data) {
					let item = data[i]
					if (legendData.indexOf(item.lang) == -1) {
						legendData.push(item.lang)
						seriesDataRaw[item.lang] = 1
					} else {
						seriesDataRaw[item.lang] += 1
					}
				}
				for (let i in seriesDataRaw) {
					let item = seriesDataRaw[i]
					seriesData.push({name: i, value: item, label: {show: item > 10}, labelLine: {show: item > 10}})
				}
				seriesData.sort((a, b) => b.value - a.value)
				this.aaaa = seriesData

				let option = {
					tooltip : {
						trigger: 'item',
						formatter: "{a} <br/>{b} : {c} ({d}%)"
					},
					legend: {
						type: 'scroll',
						orient: 'vertical',
						right: 10,
						top: 20,
						bottom: 20,
						data: legendData,
						selected: selected
					},
					series : [
						{
							name: '域名数量',
							type: 'pie',
							radius : '55%',
							center: ['40%', '50%'],
							data: seriesData,
							itemStyle: {
								emphasis: {
									shadowBlur: 10,
									shadowOffsetX: 0,
									shadowColor: 'rgba(0, 0, 0, 0.5)'
								}
							}
						}
					]
				}

				return option
			},
			// 初始化柱状图
			barInit (data) {
				let xlabel = []
				let ydata = []
				for (let item of this.aaaa) {
					xlabel.push(item.name)
					ydata.push(item.value)
				}
				let option = {
					tooltip : {
						trigger: 'axis',
						axisPointer: {
							type: 'shadow',
							label: {
								show: true
							}
						}
					},
					xAxis: {
						type: 'category',
						name: "语种",
						axisLabel: {
							rotate: 60
						},
						data: xlabel
					},
					yAxis: {
						type: 'value',
						name: '数量',
						splitNumber: 10,
					},
					series: [{
						data: ydata,
						type: 'bar',
						color: ["#2f4554"]
					}]
				}

				return option
			},
			//初始化地图
			mapInit (data) {
				let inmap = new inMap.Map({
					id: "geo_map",
					skin: "Blueness",
					// 初始地图中心
					center: [107.40, 33.42],
					// 缩放
					zoom: {
						value: 3, 
						show: true, 
						max: 10, 
						min: 2
					}
				})
				let overlay = new inMap.PointOverlay({
					// 气泡提示
					tooltip: {
						show: true,
						formatter: (params) => {
							return (
								"<div><div>域名："+params.domain+"</div><div>IP："+params.ip+"</div><div>管理归属："+params.auth+"</div><div>位置："+params.location+"</div></div>"
							);
						},
						offsets: {
							top: 15,
							left: 15
						}
					},
					style: {
						normal: {
							backgroundColor: "#FFF",
							size: 4
						},
						mouseOver: {
							backgroundColor: "#FFF",
							borderWidth: 0
						}
					},
					data: data
				})
				inmap.add(overlay)
			},

			// 重定向页面至所选择域名的详细信息
			redirectTo (data, index) {
				this.$router.push({
					name: "Index", 
					params: {"domain_name": this.list[(this.curPage - 1) * 10 + index].domain_name}
				})
			},

			// 数据格式化
			formatter (item) {
				return {
					"domain_name": item.domain_name,
					"lang": item.lang || "英语"
				}
			},

			// 正则匹配。使用src作为模板测试dst
			regMatch (src, dst) {
				let pat = new RegExp(src)
				return pat.test(dst)
			},

			changePage (page) {
				this.curPage = page
			},

			selectChange () {
				this.requestIPRecord()
			}
		}
	}
</script>

<style scoped>
.ivu-table .a{
	font-style: underline;
	color: #72ACE3
}
.layout{
	border: 1px solid #d7dde4;
	background: #f5f7f9;
	position: relative;
	border-radius: 4px;
	overflow: hidden;
}
.nav-head{
	display: flex;
	flex-direction: row;
	width: 500px;
	height: 60px;
	color: #fff;
}
.nav-head-logo{
	margin: 5px 15px;
	font-size: 24px;
	font-weight: bold;
}
.nav-head-title{
	display: flex;
	flex-direction: column;
	align-items: left;
	font-size: 14px;
}
.nav-head-title div{
	height: 30px;
	margin: -5px 0;
}
.content{
	padding: 0 50px;
	min-height: 280px;
	background: #EFF0F4;
}
.card{
	display: flex;
	flex-direction: column;
	align-items: left;
	margin: 20px;
	width: 100%;
}
.select{
	height: 40px;
	display: flex;
	flex-direction: row;
	vertical-align: center;
	line-height: 40px;
	font-size: 15px;
	margin-bottom: 10px;
}
.list-action{
	position: relative;
	padding: 0 10px;
	vertical-align: center;
}
.searchbar{
	width: 200px;
	border-radius: 16px;
	margin-right: 20px;
}
.label{
	margin: 10px;
	font-size: 16px;
}
.footer{
	text-align: center;
}
.footer div span{
	font-size: 12px;
	margin: 0 20px;
}
</style>