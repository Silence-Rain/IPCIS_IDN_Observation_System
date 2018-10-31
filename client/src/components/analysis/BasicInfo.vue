<template>
	<div>
		<Tag type="dot" color="primary">{{ lang }}</Tag>
		<!-- <Tag v-if="!isIdentical" type="dot" color="error">whois信息与解析IP信息不符</Tag> -->
	    
	    <hr color="#f5f7f9"/>
	    <div class="label">域名 whois 信息</div>
	    <Table stripe :loading="remoteLoading" :columns="whoisCol" :data="whoisInfo"></Table>
	    <hr color="#f5f7f9"/>
	    <div class="label">域名解析 IP 信息</div>
	    <Table stripe :loading="localLoading" :columns="ipCol" :data="ipInfo"></Table>
	</div>
</template>

<script>
	export default {
		data () {
			return {
				targetDomain: "",			// 要查询的目标域名
				localLoading: false,		// 基本信息表loading状态
				remoteLoading: false,		// whois信息表loading状态
	            lang: "",					// 域名语种
	            whoisInfo: [],				// 域名whois归属信息
	            ipInfo: [],					// 域名解析IP信息
	            // isIdentical: false,			// 域名解析IP是否与whois信息相同
	            whoisCol: [
	                {
	                    title: "注册人",
	                    key: "registrar"
	                },
	                {
	                    title: "注册机构",
	                    key: "registrant"
	                },
	                {
	                    title: "注册机构地址",
	                    key: "address"
	                },
	                {
	                    title: "E-Mail",
	                    key: "email"
	                },
	                {
	                    title: "注册时间",
	                    key: "register_date"
	                },
	                {
	                    title: "失效时间",
	                    key: "expire_date"
	                }
	            ],
	            ipCol: [
	                {
	                    title: "解析IP地址",
	                    key: "ip"
	                }, 
	                {
	                    title: "解析IP地理位置",
	                    key: "location"
	                }, 
	                {
	                    title: "解析IP归属",
	                    key: "auth"
	                }
	            ]
	        }
		},

		created () {
			// 从localStorage中获取目标域名
			this.targetDomain = localStorage.getItem("domain")
		},

		mounted () {
			this.whoisInfo = [{
		        "registrar": "注册人",
		        "registrant": "注册机构",
		        "address": "注册机构地址",
		        "email": "test@email.com",
		        "register_date": "17-jun-2005",
		        "expire_date": "17-jun-2020"
			}]
			// 请求域名基本信息
			this.localLoading = true
			this.axios.post(this.baseUrl + "/info/basic", 
				JSON.stringify({domain_name: this.targetDomain}))
				.then((response) => {
					this.localLoading = false
					this.lang = response.data.result.lang
					this.ipInfo = response.data.result.ip
					// 向父组件Index发布域名解析IP事件，更新父组件中解析IP列表
					this.bus.$emit("resolved_ips", this.getResolvedIPs())
				})
				.catch((response) => {
					this.localLoading = false
					this.$Message.error("网络错误，请稍后再试！")
				})
			// 请求域名whois信息
			this.remoteLoading = true
			this.axios.post(this.baseUrl + "/info/whois", 
				JSON.stringify({domain_name: this.targetDomain}))
				.then((response) => {
					this.remoteLoading = false
					this.whoisInfo = [response.data.result.whois]
				})
				.catch((response) => {
					this.remoteLoading = false
					this.$Message.error("网络错误，请稍后再试！")
				})
			
		},

		methods: {
			// 获取解析IP列表
			getResolvedIPs () {
				let ret = []
				for (var item of this.ipInfo) {
					ret.push(item.ip)
				}
				return ret
			}
		}
	}
</script>

<style scoped>
hr{
	margin: 10px 0;
	background-color: #f5f7f9;
}
.label{
    margin: 10px;
    font-size: 16px;
}
</style>