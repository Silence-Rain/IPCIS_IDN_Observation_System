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
				targetDomain: "",
				isLoading: false,
				curPage: 1,
				newDomain: "",
				showAddModal: false,
				tableHeader: [
					{
						title: "域名",
						key: "domain_name"
					},
					{
						title: "活跃度",
						key: "active"
					},
					{
						title: "预测服务类型",
						key: "service"
					}
				],
				rawList: []
			}
		},
		computed: {
			length () {
				return this.rawList.length
			},
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
			this.isLoading = true
			this.axios.get(this.testUrl + "/list")
				.then((response) => {
					this.isLoading = false
					for (var item of response.data.result) {
						this.rawList.push(this.formatter(item))
					}
				})
				.catch((response) => {
					this.isLoading = false
					this.$Message.error("对方不想说话，所以等会再试吧");
				})
		},
		methods: {
			redirectTo (data, index) {
				this.$router.push({
					name: "Analytic", 
					params: {"domain_name": this.rawList[index].domain_name}
				})
			},

			formatter (domain, active = null, service = null) {
				return {
					"domain_name": domain,
					"active": active,
					"service": service
				}
			},

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

			addDomain () {
				this.rawList.push(this.formatter(this.newDomain))
				//TODO: 此时开始自动化富化信息
			}
		}
	}
</script>

<style scoped>
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