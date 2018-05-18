import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Info from '@/components/Info'
import Trend from '@/components/Trend'
import Map from '@/components/Map'
import Relation from '@/components/Relation'

Vue.use(Router)

export default new Router({
  routes: [
    {
    	path: '/',
    	name: 'Index',
    	component: Index,
    	children:[
    		{
		    	path: "/Info",
		    	name: "Info",
		    	component: Info
		    },
		    {
		    	path: "/Trend",
		    	name: "Trend",
		    	component: Trend
		    },
		    {
		    	path: "/Map",
		    	name: "Map",
		    	component: Map
		    },
		    {
		    	path: "/Relation",
		    	name: "Relation",
		    	component: Relation
		    }
    	]
    }
  ]
})
