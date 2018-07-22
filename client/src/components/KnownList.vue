<template>
	<div class="layout">
		<Layout>
			<!-- 顶部导航栏 -->
			<Header>
				<Menu mode="horizontal" theme="dark">
					<div class="nav-head">
						<div class="nav-head-logo">IPCIS</div>
						<div class="nav-head-title">
							<div>恶意域名检测系统</div>
							<div>Malicious Domain Detection System</div>
						</div>
					</div>
				</Menu>
			</Header>

			<Layout>
				<Content class="content">
					<div class="content-title">
						已知恶意域名列表
					</div>
					<div class="list-action">
						 <Button type="primary" shape="circle" icon="plus" @click="showAdd">添加恶意域名</Button>
						 <Input class="searchbar" v-model="targetDomain" icon="search" placeholder="搜索"></Input>
					</div>
					<Table style="margin:20px 0" stripe :loading="isLoading" :columns="tableHeader" :data="list" @on-row-click="redirectTo"></Table>
					<Page style="float:right;margin:10px;" :total="length" :current="curPage" :page-size="20" show-total @on-change="changePage"></Page>

					<Modal v-model="showAddModal" title="添加恶意域名" @on-ok="addDomain">
						<Input v-model="newDomain" placeholder="请输入完整域名"></Input>
					</Modal>
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
	export default {
		data () {
			return {
				targetDomain: "",			// 要查询的目标域名
				isLoading: false,			// 表格loading状态
				curPage: 1,					// 当前页数
				newDomain: "",				// 新增域名
				showAddModal: false,		// 新增域名对话框显示状态
				rawList: [],				// 所有已知恶意域名列表
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
						title: "活跃度",
						key: "active"
					},
					{
						title: "服务类型",
						key: "service"
					}
				]
			}
		},
		computed: {
			// 已知恶意域名列表长度
			length () {
				return this.rawList.length
			},
			// 当前显示的内容
			// 根据选择的页数展示20条记录
			// 根据搜索框中内容，正则匹配查询结果
			list () {
				if (this.targetDomain == "") {
					return this.rawList.slice((this.curPage - 1) * 20, this.curPage * 20)
				}
				else {
					var ret = []
					for (var i of this.rawList) {
						if (this.regMatch(this.targetDomain, i.domain_name)) {
							ret.push(i)
						}
					}
					this.curPage = 1
					if (ret.length == 0) {
						return [this.formatter("未查询到结果")]
					}
					else {
						return ret.slice((this.curPage - 1) * 20, this.curPage * 20)
					}
				}
			}
		},
		mounted () {
			localStorage.clear()
			
			// 请求已知恶意域名列表
			this.isLoading = true
			this.axios.get(this.baseUrl + "/list")
				.then((response) => {
					this.isLoading = false
					for (var item of response.data.result) {
						this.rawList.push(this.formatter(item))
					}
				})
				.catch((response) => {
					this.isLoading = false
					this.$Message.error("网络错误，请稍后再试！");
				})
		},
		methods: {
			// 重定向页面至所选择域名的详细信息
			redirectTo (data, index) {
				this.$router.push({
					name: "Analytic", 
					params: {"domain_name": this.rawList[index].domain_name}
				})
			},

			// 数据格式化
			formatter (domain, active = null, service = null) {
				return {
					"domain_name": domain,
					"active": active,
					"service": service
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

			showAdd () {
				this.showAddModal = true
			},

			// 提交新的恶意域名，后端开始对新域名进行背景信息富化
			addDomain () {
				this.axios.post(this.baseUrl.slice(0,-1)+"9/enrich", 
					JSON.stringify({domain_name: this.newDomain}))
					.then((response) => {
						// 后端信息富化完成
						if (response.data.result) {
							this.rawList.push(this.formatter(this.newDomain))
							this.$Notice.success({
								title: "添加新域名成功！"
							})
						}
						// 后端信息富化失败
						else {
							this.$Notice.error({
								title: "添加新域名失败：数据库错误"
							})
						}
					})
					.catch((response) => {
						this.$Notice.error({
							title: "添加新域名失败：网络错误"
						})
					})
				// 提交后等待后端完成富化
				this.$Notice.warning({
					title: "新域名已提交，请等待查询完成……"
				})
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
	padding: 0 100px;
	min-height: 280px;
	background: #fff;
}
.content-title{
	height: 40px;
	margin: 20px 0;
	padding: 0 10px;
	font-size: 20px;
	line-height: 40px;
}
.list-action{
	position: relative;
	padding: 0 10px;
	vertical-align: center;
}
.searchbar{
	width: 200px;
	border-radius: 16px;
	float: right;
}
.footer{
	text-align: center;
}
.footer div span{
	font-size: 12px;
	margin: 0 20px;
}
</style>