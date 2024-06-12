<template>
  <div class="d-flex align-center justify-center">

    <!-- left -->
    <v-row justify="center">
      <!-- Logo -->
      <v-col sm="7" md="7" lg="4" align-self="center" justify="center">

        <v-sheet class="text-start">
          <h1 class="lh-tight ls-tighter font-bolder display-5">
            Build beautiful websites, faster.
          </h1>
          <v-sheet class="text-center">
            <img class="" width="300" src="../../assets/image/deer-3275594_1920.jpg"></v-sheet>
        </v-sheet>

      </v-col>

      <v-col sm="7" md="7" lg="4" class=" ">

        <div class="form" v-if="obj.login">

          <div class="mt-10 mt-lg-5 mb-6 d-flex align-items-center d-lg-block">
            <span class="d-inline-block d-lg-block h1 mt-lg-n12 mb-lg-6 me-3">👋</span>
            <h1 class="lh-tight ls-tighter font-bolder d-inline-block d-lg-block h2 font-bolder">
              Nice to see you!
            </h1>
          </div>


          <v-sheet class="mb-5" height="110">
            <label class="text-h6" for="email">
              Username
            </label>
            <v-sheet height="60">
              <v-text-field variant="outlined" v-model="obj.username"></v-text-field>
            </v-sheet>
            <span class="flash" v-if="obj.usernamealert"><v-icon color="error"
                icon="mdi-alert-circle-outline"></v-icon>请输入你的Email</span>


          </v-sheet>

          <v-sheet class="mb-5" height="110">

            <label class="text-h6">
              Password
            </label>
            <v-sheet height="60">
              <v-text-field variant="outlined" v-model="obj.password"></v-text-field>
            </v-sheet>
            <span class="flash" v-if="obj.passwordalert"><v-icon color="error"
                icon="mdi-alert-circle-outline"></v-icon>请输入你的password</span>
          </v-sheet>

          <v-sheet class="mb-8">
            <span><v-checkbox label="记住密码" color="primary" hide-details v-model="obj.remember"></v-checkbox> </span>
          </v-sheet>

          <div class="">
            <v-btn class="text-h6" block min-height='50' color="#03A9F4" @click="handsend">
              login
            </v-btn>
          </div>

          <div class="mt-8 d-flex justify-space-between">
            <v-sheet>
              <a href="/signup" class="text-decoration-none text-body-1" style="color: black;">Sign up/注册</a></v-sheet>
            <v-sheet>
              <a href="/reset" class="text-decoration-none text-body-1" style="color: black;">忘记密码</a>
            </v-sheet>
          </div>

        </div>
        <v-sheet class="form d-flex align-center justify-center" v-if="obj.robotverify">
          <robot @robotverify="result"></robot>

        </v-sheet>
      </v-col>
    </v-row>

    <v-dialog v-model="obj.dialog" width="auto">
      <v-card prepend-icon="mdi-update" max-width="400" title="登录失败" text="你的账号或密码有误，请重新输入，即将返回">
        <template v-slot:actions>
          <v-btn class="ms-auto" text="确定" @click="obj.dialog = false"></v-btn>
        </template>
      </v-card>
    </v-dialog>


  </div>
</template>

<script setup>
import { reactive, onMounted, watch } from 'vue'
import robot from '@/components/Robotverify/robot.vue'
import http from '@/util/axiosfz'
import router from '@/router';
import { useStore } from 'vuex'
import api from '@/util/api'
import { v4 as uuidv4 } from 'uuid';
import getdata from '@/plugins/getuserdata'
import wckt from '@/plugins/websocket'

const store = useStore()
const obj = reactive({
  login: true,
  robotverify: false,
  username: '',
  password: '',
  loginalert: false,
  result: false,
  remember: true,
  usernamealert: false, passwordalert: false,
  dialog: false



})
let ws = null
const useralert = () => {
  if (!obj.username) {
    obj.usernamealert = true
  } else {
    obj.usernamealert = false
  }
  if (!obj.password) {
    obj.passwordalert = true
  } else {
    obj.passwordalert = false
  }
}

const handsend = () => {
  useralert()
  if (!obj.usernamealert && !obj.passwordalert) {
    obj.login = false
    obj.robotverify = true
  }

}
//this is child send father value define function
const result = (val) => {
  obj.result = val
  if (val) {
    // console.log('welcome')
    //以下 define login function
    login()
  }
}

// watch(() => obj.remember, () => {
//   console.log(obj.remember)
// })

const login = () => {
  var formdata = new FormData()
  formdata.append('email', obj.username)
  formdata.append('password', obj.password)
  http.post('/login', formdata).then(res => {
    console.log(res)
    if (res.data.code === 0) {
      //login success,first add token
      // second updata store.state.userdata and store.state.login==true
      // third第三，create websocket
      // fourth第四，loading localtion indexdb message
      localStorage.setItem("token", res.data.token)// accept接收 server send token
      //get userdata add vuex
      var formdata = new FormData()
      formdata.append('email', obj.username)
      // console.log(api.updateuser(obj.username))
      api.httptk.post('/userdata', formdata).then(res => {
        console.log(res.data)
        store.commit('updatauser', res.data)//updateuser)
        store.commit('login', true)//更改login状态

        //create websocket and open/create indexdb
        wckt.startchat()
      }
      )


      //remember userid and password
      if (obj.remember) {
        localStorage.setItem("userId", obj.username)
        localStorage.setItem("password", obj.password)
      } else {
        //clear remember userid and password
        localStorage.removeItem("userId",)
        localStorage.removeItem("password",)
      }
      setTimeout(() => router.push('/userhome'), 2000)//2s 后跳转

    } else {
      //login lose
      obj.dialog = true
      setTimeout(() => location.reload(), 2000)

    }
  })
}
onMounted(() => {
  //load remember useremail and password
  let username = localStorage.getItem("userId");
  if (username) {
    obj.username = localStorage.getItem("userId");
    obj.password = localStorage.getItem("password");//

  }

})

</script>
<style lang="scss" scoped>
.box_from {
  width: 80%;
  height: 100%;


}

.form {
  margin: 100px auto;
  height: 31.25rem;
  width: 300px;

}

.flash {

  animation: flash 1s ease-in-out 3;
}


@keyframes flash {
  0% {

    opacity: 0;
  }

  50% {
    opacity: 0.5;
  }

  100% {
    opacity: 1;
  }
}
</style>
