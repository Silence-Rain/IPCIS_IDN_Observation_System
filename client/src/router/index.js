import Vue from 'vue'
import Router from 'vue-router'
import DomainList from '@/components/DomainList'
import Index from '@/components/analysis/Index'
import BasicInfo from '@/components/analysis/BasicInfo'
import GeoDistribution from '@/components/analysis/GeoDistribution'
import TransTopo from '@/components/analysis/TransTopo'

Vue.use(Router)

export default new Router({
  routes: [
	{
		path: "/",
		name: "DomainList",
		component: DomainList
	},
	{
		path: "/analysis",
		name: "Index",
		component: Index,
		children:[
			{
				path: "/info",
				name: "BasicInfo",
				component: BasicInfo
			},
			{
				path: "/map",
				name: "GeoDistribution",
				component: GeoDistribution
			},
			{
				path: "/topo",
				name: "TransTopo",
				component: TransTopo
			}
		]
	}
  ]
})
