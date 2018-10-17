<template>
	<div>
		<div class="label">域名基本信息</div>
	    <Table stripe :loading="localLoading" :columns="basicCol" :data="basicInfo"></Table>
	    
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
	            basicInfo: [],				// 域名基本信息
	            whoisInfo: [],				// 域名whois归属信息
	            ipInfo: [],					// 域名解析IP信息
	            basicCol: [
	                {
	                    title: "语种",
	                    key: "lang"
	                },
	                {
	                    title: "生存时间（TTL）",
	                    key: "ttl"
	                },
	                {
	                    title: "发现时间",
	                    key: "timestamp"
	                }
	            ],
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
	                }
	            ]
	        }
		},

		created () {
			// 从localStorage中获取目标域名
			this.targetDomain = localStorage.getItem("domain")
		},

		mounted () {
			// this.staticInfo = [{
		 //        "is_dga": 0,
		 //        "ttl": 86400,
		 //        "credit": 70,
		 //    }]
			// this.ipInfo = [{
	  //           "ip": "118.89.140.118",
	  //           "location": "中国-上海-上海",
	  //           "dns": "8.8.8.8"
	  //       }]
			this.whoisInfo = [{
		        "registrar": "注册人",
		        "registrant": "注册机构",
		        "address": "注册机构地址",
		        "email": "test@email.com",
		        "register_date": "17-jun-2005",
		        "expire_date": "17-jun-2020"
			}]
			// this.bus.$emit("resolved_ips", this.getResolvedIPs())
			// 请求域名基本信息
			this.localLoading = true
			this.axios.post(this.baseUrl + "/info/basic", 
				JSON.stringify({domain_name: this.targetDomain}))
				.then((response) => {
					this.localLoading = false
					this.basicInfo = [response.data.result]
					this.ipInfo = response.data.result.ip
					// console.log(this.ipInfo)
					// 向父组件Index发布域名解析IP事件，更新父组件中解析IP列表
					this.bus.$emit("resolved_ips", this.getResolvedIPs())
				})
				.catch((response) => {
					this.localLoading = false
					this.$Message.error("网络错误，请稍后再试！")
				})
			// // 请求域名whois信息
			// this.remoteLoading = true
			// this.axios.post(this.baseUrl + "/info/whois", 
			// 	JSON.stringify({domain_name: this.targetDomain}))
			// 	.then((response) => {
			// 		this.remoteLoading = false
			// 		this.whoisInfo = [response.data.result.whois]
			// 	})
			// 	.catch((response) => {
			// 		this.remoteLoading = false
			// 		this.$Message.error("网络错误，请稍后再试！")
			// 	})
			
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