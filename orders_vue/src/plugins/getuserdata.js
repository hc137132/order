import api from '@/util/api'

const getdata =async (userid,email) => {
  let data=new FormData()
  let user=null
  console.log(userid,email)
  if(userid){
    data.append('userid',userid)
  }
  if(email){
    data.append('email',email)
  }
  const response = await api.httptk.post('/userdata', data)  
  console.log(response.data)  
  return response.data // 注意这里返回了 response.data  
}  


export default {getdata}
