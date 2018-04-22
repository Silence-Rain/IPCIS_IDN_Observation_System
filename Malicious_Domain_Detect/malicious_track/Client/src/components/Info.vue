<template>
	<div>
		<div class="label">域名基本特征</div>
	    <Table stripe :loading="isLoading" :columns="staticCol" :data="staticInfo"></Table>
	    <div class="label">域名解析特征</div>
	    <Table stripe :loading="isLoading" :columns="dynCol" :data="dynInfo"></Table>
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
	                    title: "注册时长/年",
	                    key: "register_years"
	                }
	            ],
	            staticInfo: [
	                {
	                    is_dga: true,
	                    ttl: 86400,
	                    register_years: 16
	                }
	            ],
	            dynCol: [
	                {
	                    title: "子域名",
	                    key: "domain_name"
	                },
	                {
	                    title: "解析IP",
	                    key: "ip_1"
	                },
	                {
	                    title: "活动量",
	                    key: "ip_activity"
	                }
	            ],
	            dynInfo: [
	                {
	                    domain_name: "aaa.test.com",
	                    ip_1: "118.89.140.118",
	                    ip_activity: 100
	                },
	                {
	                    domain_name: "bbb.test.com",
	                    ip_1: "192.168.1.1",
	                    ip_activity: 50
	                }
	            ]
	        }
		}
	}
</script>

<style scoped>
.label{
    margin: 10px;
    font-size: 16px;
}
</style>