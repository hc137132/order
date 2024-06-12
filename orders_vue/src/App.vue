<template>
  <v-app>

    <v-app-bar elevation="2" v-if="store.state.app">

      <v-spacer></v-spacer>
      <v-btn class="rounded-pill" @click="router.push('/home')">
            <v-icon color="#03A9F4" icon="mdi-home" size="30"></v-icon>
         大厅
        </v-btn>
      <span class="text-center mr-5" v-if="!store.state.login">

        <v-btn class="rounded-pill" @click="login">
            <v-icon color="#03A9F4" icon="mdi-login-variant" size="30"></v-icon>
          login/登录
        </v-btn>
      </span>


      <span v-if="store.state.login">
        <v-btn class="rounded-pill" @click="router.push('/userhome')">
          <v-icon color="#03A9F4" icon="mdi-account-outline" size="36"></v-icon>
          <v-tooltip activator="parent" location="bottom">个人中心</v-tooltip>
        </v-btn>

        <v-btn class="rounded-pill"  @click="obj.message=true">    
                <v-icon color="light-blue" icon="mdi-message-outline" size="30" ></v-icon><v-badge :content="obj.sumunread" v-if="obj.sumunread!=0" color="error" offset-y="-10"> </v-badge>
              <v-tooltip activator="parent" location="bottom">消息</v-tooltip>
            </v-btn>
        <v-dialog width="auto" transition="dialog-top-transition" v-model="obj.message">

         
            <message> </message>
          
        </v-dialog>

        <v-btn class="rounded-pill" @click="handleexit">
          <v-icon color="light-blue" icon="mdi-location-exit" size="30"></v-icon>
          <v-tooltip activator="parent" location="bottom">退出登录</v-tooltip>
        </v-btn>

      </span>
      <v-sheet width="50"></v-sheet>
    </v-app-bar>

    <v-main>
      
        <div style="position: absolute;top:50%;left: 50%;" v-if="store.state.loading">
        <v-progress-circular :size="70" :width="7" color="teal" indeterminate></v-progress-circular>
      </div>
     
      <router-view>
      </router-view>
    </v-main>
    <v-spacer></v-spacer>
    <v-footer class=" text-center d-flex flex-column">




      <v-divider>分割线</v-divider>

      <div>
        {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
      </div>
    </v-footer>

  </v-app>
</template>
<script setup>
// use theme
import Message from './components/message/Message.vue'
import { useTheme } from "vuetify"
import router from './router';
import { useStore } from 'vuex'
import api from '@/util/api'
import { onMounted,watch,reactive,computed } from 'vue';
import getuserdata from '@/plugins/getuserdata';
import wskt from '@/plugins/websocket'

const store = useStore()
const theme = useTheme();
theme.value = 'myCustomLightTheme'
const obj=reactive({
  sumunread:0,message:false

})

const login = () => {
  router.push('/login')
}
onMounted(() => {
  api.httptk.get('/typehandle').then(res => {
    store.commit('typehandle', res.data)//updateuser)
  })
  if(store.state.login && !store.state.ws){
    wskt.startchat()

  }
 

})

const handleexit = () => {
  wskt.closechat()
  store.commit('updatauser', {})
  localStorage.removeItem('token')
  router.push('/home')
  store.commit('login', false)
  
}
watch(()=>store.state.login,()=>{
  if(store.state.login===false){

     location.reload()
  }

})
watch(()=>store.state.messagelist,()=>{
  obj.sumunread=0
  
      for(let a of store.state.messagelist){
          for(let b of a.content){
              if(b && b.to===store.state.userdata.userid && !b.unread){
                obj.sumunread++
              }
          }
      }

},{deep:true})

watch(()=>store.state.openmessage,()=>{
    obj.message=true

})

</script>

<style lang="scss" scoped></style>
