<template>
    <div class="layout">
        <Layout>
            <!-- 顶部导航栏 -->
            <Header>
                <Menu mode="horizontal" theme="dark" active-name="1">
                    <div class="layout-logo">IPCIS 恶意域名跟踪系统</div>
                    <div class="layout-nav">
                        <Icon type="search" size="20" color="#fff" style="margin:7px;"></Icon>
                        <Input v-model="targetDomain" placeholder="输入要查询的域名..." clearable style="width: 200px"></Input>
                    </div>
                </Menu>
            </Header>

            <Layout style="padding: 0 50px;">              
                <Breadcrumb class="current-target">
                    <BreadcrumbItem>{{targetDomain}}</BreadcrumbItem>
                    <BreadcrumbItem>{{pages[curPage]}}</BreadcrumbItem>
                </Breadcrumb>
                <Content class="content">
                    <Layout>
                        <!-- 侧边栏 -->
                        <Sider hide-trigger :style="{background: '#fff'}">
                            <Menu active-name="0" theme="light" width="auto">
                                <MenuItem name="0">
                                    <router-link to="/Info">
                                        <Icon type="ios-information"></Icon>
                                        概览
                                    </router-link>
                                </MenuItem>
                                <Submenu name="1">
                                    <template slot="title">
                                        <Icon type="ios-albums"></Icon>
                                        实时动态
                                    </template>
                                    <MenuItem name="1-1">
                                        <router-link to="/Trend">
                                            流量趋势
                                        </router-link>
                                    </MenuItem>
                                    <MenuItem name="1-2">
                                        <router-link to="/Map">
                                            地理位置分布
                                        </router-link>
                                    </MenuItem>
                                    <MenuItem name="1-3">
                                        <router-link to="/Relation">
                                            通信对象
                                        </router-link>
                                    </MenuItem>
                                </Submenu>
                            </Menu>
                        </Sider>

                        <!-- 页面主体部分 -->
                        <Content class="content">
                            <router-view></router-view>
                        </Content>
                    </Layout>
                </Content>
            </Layout>
            <Footer class="layout-footer-center">2018 &copy; Silence-Rain</Footer>
        </Layout>
    </div>
</div>
</template>

<script>
    export default {
        data () {
            return {
                targetDomain: "test.com",
                pages: ["概览", "流量趋势", "地理位置分布", "通信对象"],
                curPage: 0,
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
.current-target{
    margin: 15px;
    font-size: 18px;
    font-weight: bold;
}
.layout{
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
}
.layout-logo{
    width: 300px;
    float: left;
    position: relative;
    color: #fff;
    font-size: 23px;
    font-weight: bold;
}
.layout-nav{
    width: 420px;
    margin: 0 auto;
    margin-right: 20px;
}
.content{
    padding: 10px;
    min-height: 280px;
    background: #fff;
}
.layout-footer-center{
    text-align: center;
}
</style>