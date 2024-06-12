import axios from 'axios'
import store from '@/store'


const http=axios.create({
    baseURL:'/api',
    timeout:10000,
    headers: {
        
    }
 })


http.interceptors.request.use(
    function(config){
        store.state.loading=true
        return {
            ...config,
        }
    },
    function(error){
        return error
    }
)

// 响应拦截器
http.interceptors.response.use(req=>{
    store.state.loading=false
    return req

}, err=>{

})

export default http