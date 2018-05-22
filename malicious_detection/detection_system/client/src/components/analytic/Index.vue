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
                <!-- 侧边栏 -->
                <Sider hide-trigger style="background:#fff;">
                    <Menu active-name="0" theme="light" width="auto" @on-select="route">
                        <MenuItem name="0">
                            <Icon type="ios-information"></Icon>
                            概览
                        </MenuItem>
                        <Submenu name="-1">
                            <template slot="title">
                                <Icon type="ios-albums"></Icon>
                                实时动态
                            </template>
                            <MenuItem name="1">
                                IP地址通信活动关系
                            </MenuItem>
                            <MenuItem name="2">
                                域名活跃度
                            </MenuItem>
                            <MenuItem name="3">
                                IP地理位置分布
                            </MenuItem>
                        </Submenu>
                    </Menu>
                </Sider>

                
                <Content class="content">
                    <Layout>
                        <Breadcrumb class="current-target">
                            <BreadcrumbItem>{{targetDomain}}</BreadcrumbItem>
                            <BreadcrumbItem>{{pages[curPage][0]}}</BreadcrumbItem>
                        </Breadcrumb>
                        <!-- 页面主体部分 -->
                        <Content class="content">
                            <keep-alive>
                                <router-view/>
                            </keep-alive>
                        </Content>
                    </Layout>
                </Content>
            </Layout>
            <Footer class="footer">
                <div>
                    2018 &copy; Silence-Rain<span>联系方式：daniel.s.mo503@gmail.com</span>
                </div>
            </Footer>
        </Layout>
    </div>
</div>
</template>

<script>
    export default {
        data () {
            return {
                targetDomain: "ns2.hostkey.com",
                pages: [
                    ["概览", "Info"], 
                    ["IP地址通信活动关系", "Relation"],
                    ["域名活跃度", "Trend"], 
                    ["IP地理位置分布", "Map"]
                ],
                curPage: 0,
                ips: []
            }
        },

        mounted () {
            this.targetDomain = this.$route.params.domain_name
            this.route(0)
            this.bus.$on("upIp", (ips) => {
                this.ips = ips
            })
        },

        methods: {
            route (name) {
                if (name >= 0) {
                    this.curPage = name
                    this.$router.push({
                        name: this.pages[this.curPage][1],
                        params: {"domain_name": this.targetDomain, "ips": this.ips}
                    })
                }
            }
        }
    }
</script>

<style scoped>
.current-target{
    padding: 15px;
    font-size: 18px;
    font-weight: bold;
    background: #fff;
    border-bottom: 1px solid #f5f7f9;
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
.layout-nav{
    width: 420px;
    margin: 0 auto;
    margin-right: 20px;
}
.content{
    padding: 10px 20px 20px 20px;
    min-height: 280px;
    background: #fff;
}
.footer{
    text-align: center;
}
.footer div span{
    font-size: 12px;
    margin: 0 20px;
}
</style>