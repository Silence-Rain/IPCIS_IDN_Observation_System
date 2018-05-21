import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/analytic/Index'
import KnownList from '@/components/KnownList'
import Info from '@/components/analytic/Info'
import Trend from '@/components/analytic/Trend'
import Map from '@/components/analytic/Map'
import Relation from '@/components/analytic/Relation'

Vue.use(Router)

export default new Router({
  routes: [
    {
    	path: "/known_list",
    	name: "KnownList",
    	component: KnownList
    },
    {
    	path: "/analytic",
    	name: "Analytic",
    	component: Index,
    	children:[
    		{
		    	path: "/info",
		    	name: "Info",
		    	component: Info
		    },
		    {
		    	path: "/trend",
		    	name: "Trend",
		    	component: Trend
		    },
		    {
		    	path: "/map",
		    	name: "Map",
		    	component: Map
		    },
		    {
		    	path: "/relation",
		    	name: "Relation",
		    	component: Relation
		    }
    	]
    }
  ]
})
