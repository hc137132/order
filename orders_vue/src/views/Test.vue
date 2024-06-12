<template>
   <v-layout>   
      <v-main >
        <div>
        <p>from <input type="text" v-model="obj.fromuser"></p>
        <p>to <input type="text" v-model="obj.touser"></p>
        <v-btn @click="handlewsk">点击连接</v-btn>
        <input type="text" v-model="obj.text" style="border:1px solid black">
    <v-btn class="mr-5" @click="send">test</v-btn>
    <v-btn @click="close">close</v-btn>
</div>

</v-main>
<v-btn @click="storetest"> storetest</v-btn>

    </v-layout>
 
</template>

<script setup>

import {reactive,onMounted,watch} from 'vue';
import api from '@/util/api'

import def from '@/plugins/getdate'
import {useStore} from 'vuex';
import wskt from '@/plugins/websocket'
const store=useStore()
const obj=reactive({
  style:'position:absolute;',overlay:false,skill:50,
  complist:[],fromuser:'',touser:'',
  drawer:true,number:0,
  rail:true,
  datalist: [{ name: '个人资料', url: '/userhome/user' },
  { name: '我的发布', url: '/userhome/myproject' },
  { name: '我的任务', url: '/userhome/tproject' },
  { name: '安全中心', url: '/userhome/updatapwd' },],
  datalist:[],
      myname:'',
      text:'',
      usertext:''


})
let ws=null
const send=()=>{
      
       wskt.startchat()
}
 
 
    onMounted(()=>{
    
    }) 

    
    
    const handconn=()=>{

      const wss=new WebSocket(`ws://127.0.0.1:8000/ws/${obj.fromuser}/`)
      wss.send(obj.usertext)
      wss.onmessage=function(event){
      obj.datalist.push(event.data)
    }
      
    }



const handel=(e)=>{

  var x = e.pageX;
        var y = e.pageY-10;
        var x = e.pageX-10;
        var zx=e.offsetX
        var zy=e.offsetY
        var data={x:x,y:y,number:obj.complist.length+1}
        obj.complist.push(data)
        obj.style=`position:absolute;top:${y}px;left:${x}px`

}
function over(id, n, e) {
  document.querySelectorAll('#card')[n].classList.add('bg-blue-darken-3')
}
function leave(id, n, e) {
  document.querySelectorAll('#card')[n].classList.remove('bg-blue-darken-3')
}
const handle = (n, url) => {
  // console.log(n)
  // 
  var elelist = document.querySelectorAll('#card')
  elelist.forEach(ele => {
    ele.classList.remove('bg-primary')
  })
  elelist[n].classList.add('bg-primary')
  if (url) {
    router.push(url)
  }
}
const getorders=()=>{
let oneday=86400
  console.log(def.date(def.gettime(new Date())+oneday*30))
  console.log(def.date(def.gettime(new Date())+oneday*15))
}
</script>
<style lang="scss" scoped>
.a {
  width:300px;
  height: 100px;
  border: 1px solid red ;
 
  
}
.b{

width: 50px; height: 50px;
border: 2px solid black;

}

.d{

width: 50px; height: 50px;
border: 2px solid rgb(10, 201, 156);

}
.form {
  margin: 100px auto;
  height: 31.25rem;
  width: 300px;
}</style>
