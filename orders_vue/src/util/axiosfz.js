import axios from 'axios'
import store from '@/store'

// function http(url,header){
//     return axios({
//         url:'/api'+url,
//         headers:{

//         }

//     })
// }

const http=axios.create({
    baseURL:'/api',
    timeout:10000,
    headers: {
        
    }
 })


// 拦截器的使用
// 发请求之前拦截
http.interceptors.request.use(
    function(config){
        // console.log(config)
        store.state.loading=true
        return {
            ...config,
            // aaa:'hecheng'//add data
        }
    },
    function(error){
        console.log(error)
        return error
    }
)

// 响应拦截器
http.interceptors.response.use(req=>{
    store.state.loading=false
    return req

}, err=>{

    console.log('response error:'+err)
})

export default http