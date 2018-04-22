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
                    <BreadcrumbItem>{{pages[curPage][0]}}</BreadcrumbItem>
                </Breadcrumb>
                <Content class="content">
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
                                        流量趋势
                                    </MenuItem>
                                    <MenuItem name="2">
                                        地理位置分布
                                    </MenuItem>
                                    <MenuItem name="3">
                                        通信对象
                                    </MenuItem>
                                </Submenu>
                            </Menu>
                        </Sider>

                        <!-- 页面主体部分 -->
                        <Content class="content">
                            <router-view/>
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
                pages: [
                ["概览", "Info"], 
                ["流量趋势", "Trend"], 
                ["地理位置分布", "Map"], 
                ["通信对象", "Relation"]
                ],
                curPage: 0,
            }
        },

        methods: {
            route (name) {
                if (name >= 0) {
                    this.curPage = name
                    this.$router.push(this.pages[this.curPage][1])
                }
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