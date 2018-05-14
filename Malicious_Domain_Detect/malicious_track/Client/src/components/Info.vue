<template>
	<div>
		<div class="label">域名基本信息</div>
	    <Table stripe :loading="isLoading" :columns="staticCol" :data="staticInfo"></Table>
	    <div class="label">域名归属信息</div>
	    <Table stripe :loading="isLoading" :columns="whoisCol" :data="whoisInfo"></Table>
	    <div class="label">域名解析IP信息</div>
	    <Table stripe :loading="isLoading" :columns="ipCol" :data="ipInfo"></Table>
	</div>
</template>

<script>
	export default {
		data () {
			return {
				isLoading: false,
	            staticCol: [
	                {
	                    title: "是否DGA",
	                    key: "is_dga"
	                },
	                {
	                    title: "生存时间（TTL）",
	                    key: "ttl"
	                },
	                {
	                    title: "信誉分数",
	                    key: "credit"
	                }
	            ],
	            staticInfo: [
	                {
	                    is_dga: true,
	                    ttl: 86400,
	                    credit: 70
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
	            whoisInfo: [
	                {
						registrar: "莫少煌",
						registrant: "东南大学",
						address: "江苏省南京市东南大学九龙湖校区",
						email: "test@email.com",
						register_date: "17-jun-2005",
						expire_date: "17-jun-2020"
					}
	            ],
	            ipCol: [
	                {
	                    title: "解析IP地址",
	                    key: "ip"
	                },
	                {
	                    title: "IP地理位置",
	                    key: "location"
	                },
	                {
	                    title: "IP活动量",
	                    key: "count"
	                }
	            ],
	            ipInfo: [
	                {
	                    ip: "118.89.140.118",
	                    location: "中国-上海-上海",
	                    count: 150
	                }
	            ]
	        }
		},

		mounted () {
			// this.axios.post("localhost:8888/info", {domain_name: this.name})
			// 	.then((response) => {
			// 		this.staticInfo = response.static
			// 		this.whoisInfo = response.whois
			// 		this.ipInfo = response.ip
			// 	})
			// 	.catch((response) => {
			// 		alert("加载错误，请稍后再试！")
			// 	})
		}
	}
</script>

<style scoped>
.label{
    margin: 10px;
    font-size: 16px;
}
</style>