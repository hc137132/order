import axios from 'axios'
// import {useStore} from 'vuex'
// const store = require('@/store')
import store from '@/store'


const http=axios.create({
    baseURL:'/api',
    timeout:10000,
    headers: {
        'Content-Type': 'multipart/form-data'
    }
 })

 const httpdetail=axios.create({
    baseURL:'/api',
    timeout:null,
    headers: {
        'Content-Type': 'multipart/form-data',
    }
 })
const httptk=axios.create({
    baseURL:'/api',
    timeout:10000,
    headers: {
        'Content-Type': 'multipart/form-data',
        
    },
    
}
)
httpdetail.interceptors.request.use(
    function(config){
        // console.log(store.state)
      
        // console.log(window.localStorage.getItem('token'),555555)
     
        config.headers.Authorization=window.localStorage.getItem('token')
        
        
        return config
        
    },
    function(error){
        console.log(error)
        return error
    }
)
// 拦截器的使用
// 发请求之前拦截
httptk.interceptors.request.use(
    function(config){
        // console.log(store.state)
        store.state.loading=true
        // console.log(window.localStorage.getItem('token'),555555)
        if(window.localStorage.getItem('token')){
            config.headers.Authorization=window.localStorage.getItem('token')
        }
        
        return config
        
    },
    function(error){
        console.log(error)
        return error
    }
)

// 响应拦截器
httptk.interceptors.response.use(req=>{
    store.state.loading=false
    return req

}, err=>{

    console.log('response error:'+err)
})

export default {http,httptk,httpdetail}