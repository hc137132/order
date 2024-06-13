<template>
  <div v-show="store.state.login">


    <v-navigation-drawer v-model="obj.drawer" :rail="obj.rail" permanent @click="obj.rail = false" >

      <v-sheet class="d-flex mb-3 mt-3 ml-1 align-center justify-end" height="100" >


        <div :style="obj.style" >
          <img style="max-height: 100%;" :src="obj.avatar" v-if="obj.avatar">
          <v-icon icon="mdi-account-circle" v-if="!obj.avatar" size="80" color="#42A5F5"></v-icon>
        </div>

        <span class="text-h6 ml-2" v-show="!obj.rail">个人主页</span>
        <v-btn icon="mdi-chevron-left" variant="text" @click.stop="obj.rail = !obj.rail" v-show="!obj.rail"></v-btn>
      </v-sheet>
      <v-divider></v-divider>

      <v-card id="card" @click="handle(n, data.url)" class="d-flex mt-1 text-center align-center justify-center a" elevation="0"
        height="80" v-for="data, n in obj.datalist" :key="data.name" >
        <v-icon :icon="data.icon" size="35"></v-icon>

        <span class="text-h6" v-show="!obj.rail">{{ data.name }}</span>

      </v-card>

    </v-navigation-drawer>


    <div class="pa-3">
    
        <router-view></router-view>
      
     
    </div>


</div>
</template>

<script setup>

import router from '@/router';
import { reactive, onMounted, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
// import http from '@/util/axiosfz'
import date from '@/plugins/getdate'
import api from '@/util/api'
import { watch } from 'vue';
const store = useStore()
const obj = reactive({
  datalist: [{ name: '个人资料', url: '/userhome/user', icon: 'mdi-account-file-outline' },
  { name: '我的发布', url: '/userhome/myproject', icon: 'mdi-clipboard-plus-outline' },
  { name: '我的任务', url: '/userhome/tproject', icon: 'mdi-clipboard-account-outline' },
  { name: '安全中心', url: '/userhome/updatapwd', icon: 'mdi-security' }],
  isHovering: 12,
  hovercolor: '',
  token: null,
  avatar: null,
  drawer: true,
  rail: true,
  style: 'width: 70px;height:70px;border-radius: 50%;overflow: hidden;display: flex;align-items: center;justify-content: center;'

})
function over(id, n, e) {
  document.querySelectorAll('#card')[n].classList.add('bg-indigo-lighten-2')

  // e.target.classList.add('bg-primary') bg-blue-darken-3
}
function leave(id, n, e) {
  document.querySelectorAll('#card')[n].classList.remove('bg-indigo-lighten-2')
  // document.querySelectorAll('#card')[n].classList.remove('bg-primray')
 

  // e.target.classList.remove('bg-primary')
  // ['avatar','introduction','nickname','phonename']
}
const handle = (n, url) => {
  var elelist = document.querySelectorAll('#card')
  elelist.forEach(ele => {
    ele.classList.remove('bg-primary')
 
  
  })
  elelist[n].classList.add('bg-primary')
  if (url) {
    router.push(url)
  }
}
//component mount 
onBeforeMount(() => {
  if(store.state.userdata.avatar){
     obj.avatar = `data:image/png;base64,${store.state.userdata.avatar}`
     var data = new FormData()
    data.append('email', store.state.userdata.email)
    api.httptk.post('/userdata', data).then(res => {
                store.commit('updatauser', res.data)
                
            })
  }
  if (localStorage.getItem('token')) {
    api.httptk.get('/verifytoken').then(res => {
     
      if (res.data.user) {

      } else {
        router.push('/home')
        store.commit('login',false)

      }
    })
  } else {
    router.push('/home')
    store.commit('login',false)
  }


})

onMounted(() => {
  style()
  if(store.state.userdata.avatars){
     obj.avatar = `data:image/png;base64,${store.state.userdata.avatar}`
  }else{

  }

  
 
  const route = useRoute()
  for (var index in obj.datalist) {
    if (obj.datalist[index].url.split('/')[2] === route.fullPath.split('/')[2]) {
      handle(index)
    }
  }

})
const style = () => {
  if (!obj.rail) {
    obj.style = 'transition: all 0.3s linear 0s;width:70px;height:70px;border-radius: 50%;overflow: hidden;display: flex;align-items: center;justify-content: center;'
  } else {
    obj.style = 'transition: all 0.3s linear 0s;width:50px;height:50px;border-radius: 50%;overflow: hidden;display: flex;align-items: center;justify-content: center;'
  }
}
watch(() => obj.rail, () => {
  style()
})

</script>
<style lang="scss" scoped>
.a{
background-color: none;

}
.a:hover{
  background-color: #1976D2;
}

</style>
