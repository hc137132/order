<template>
  <div class="container">

    <v-sheet class="afrom" v-show="obj.showac">

      <div class="mt-10 mt-lg-5 mb-6 d-flex align-items-center d-lg-block">
        <span class="d-inline-block d-lg-block h1 mt-lg-n12 mb-lg-6 me-3">👋</span>
        <h1 class="lh-tight ls-tighter font-bolder d-inline-block d-lg-block h2 font-bolder">
          欢迎你的加入!
        </h1>
      </div>

      <v-sheet class="">
        <label class="text-h6">
          username
        </label>
        <v-sheet height="60">
          <v-text-field color="primary" variant="outlined" v-model="obj.username"></v-text-field></v-sheet>
        <v-sheet class="text-end text-body-2 ">
          <p class="textcolor">
            <v-tooltip activator="parent" location="end" text="用户名已存在" v-if="obj.usernamere">
              <template v-slot:activator="{ props }">
                <v-icon icon="mdi-account-cancel-outline" color="error" size="25" v-bind="props"></v-icon>
              </template>
            </v-tooltip>
            <v-tooltip activator="parent" location="end" text="用户名可以使用" v-if="obj.usernamedate">
              <template v-slot:activator="{ props }">
                <v-icon icon="mdi-account-check-outline" color="success" size="25" v-bind="props"></v-icon>
              </template>
            </v-tooltip>
          </p>
          <p class="textcolor flash" v-if="obj.usernameuse"><v-icon icon="mdi-account-alert" color="error"
              size="20"></v-icon>用户名长度不小于6</p>
        </v-sheet>
      </v-sheet>
      <v-sheet class="mt-1" height="100">
        <label class="text-h6">
          Email
        </label>
        <v-sheet height="60">
          <v-text-field color="primary" variant="outlined" v-model="obj.email"></v-text-field>
        </v-sheet>
        <v-sheet class="text-end text-body-2" v-if="obj.emailalert">
          <p class="textcolor flash">
            <v-icon icon="mdi-email-alert" color="error"></v-icon>
            邮箱格式错误
          </p>
        </v-sheet>
      </v-sheet>

      <v-sheet class=" mt-1" height="100">
        <label class="text-h6">
          password
        </label>
        <v-sheet width="100%" height="60">
          <v-text-field color="primary" v-model="obj.password" :append-inner-icon="obj.show1 ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append-inner="obj.show1 = !obj.show1" :type="obj.show1 ? 'text' : 'password'"
            variant="outlined"></v-text-field>
        </v-sheet>
        <v-sheet class="text-end text-body-2" v-if="obj.passwordalert">
          <p class="textcolor flash">
            <v-icon icon="mdi-alert-circle-outline" color="error" size="20"></v-icon> 密码至少6位且包含大小写字母数字
          </p>
        </v-sheet>
      </v-sheet>
      <v-sheet class=" mt-1" height="150">
        <label class="text-h6">
          确认密码：
        </label>
        <v-sheet width="100%" height="60"><v-text-field color="primary"
            :append-inner-icon="obj.show2 ? 'mdi-eye' : 'mdi-eye-off'" @click:append-inner="obj.show2 = !obj.show2"
            :type="obj.show2 ? 'text' : 'password'" v-model="obj.againpassword" variant="outlined"></v-text-field>

        </v-sheet>
        <v-sheet class="text-end text-body-2" v-if="obj.again">
          <p class="textcolor flash">
            <v-icon icon="mdi-alert-circle-outline" color="error" size="20"></v-icon>
            两次密码有误
          </p>
        </v-sheet>

      </v-sheet>
      <div class="d-grid">
        <v-btn @click="send" color="primary" class="text-h6" block height="50">
          注 册
        </v-btn>
      </div>


    </v-sheet>
    <v-sheet class="d-flex align-center flex-column">
     
      
      <v-card class="text-center afrom" variant="outlined" elevation="16" color="primary" width="350" height="400">
        <v-card-item>
          <v-card-title class="text-h4 mt-8 text-high-emphasis mb-2">
            请输入验证码
          </v-card-title>
          <v-card-text class="text-body-2 text-medium-emphasis mt-2">
            已向邮箱{{ obj.email }}发送验证码，有效期为五分钟
          </v-card-text>
        </v-card-item>

        <v-otp-input v-model="obj.otp"></v-otp-input>
        <v-sheet height="80">
          <v-progress-circular :size="50" color="primary" indeterminate v-show="obj.loading"></v-progress-circular>
          <p v-show="obj.otperror">验证码错误请重新输入</p>
        </v-sheet>

        <v-btn :disabled="obj.disbtn" class="text-h6" width="200" height="40" color="primary"
          @click="handleac">重新发送</v-btn>
        <p class="text-body-2 text-medium-emphasis"><span v-show="obj.showtimetext">有效期为</span>{{ obj.actime }}<span
            v-if="obj.showtimetext">s</span></p>
      </v-card></v-sheet>
  </div>
</template>

<script setup>
import { reactive, onUpdated, watch } from 'vue'
import http from '@/util/axiosfz'




const obj = reactive({
  showtimetext: true,
  disbtn: true,
  again: false,
  password: '',
  passwordalert: false,
  emailalert: false,
  againpassword: '',
  username: '',
  email: '',
  show1: false,
  show2: false,
  usernameuse: false,
  flag: false,
  showac: true,
  actime: 5,
  otp: '',
  djg_otop: '',
  otperror: false,
  loading: false,
  usernamere: false,//用于verify username 是否whether 重复repetition
  usernamedate: false,
  usernamere: false,
})
watch(() => obj.againpassword, (newvalue, oldvalue) => {
  if (obj.flag) {
    if (obj.againpassword.length >= obj.password.length && obj.againpassword != obj.password) {
      obj.again = true
    } else {
      obj.again = false
    }
  }
})
watch(() => obj.email, () => {
  if (obj.flag) {
    if (obj.email.search(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/)
      != -1) {
      obj.emailalert = false
    } else {
      obj.emailalert = true
    }
  }
})
watch(() => obj.username, () => {
  if (obj.username.length >= 6) {
    obj.usernameuse=false
    var data = new FormData()
    data.append('username', obj.username)
    http.post('/usernamedete', data).then(res => {
      console.log(res.data)
      if(res.data.code===0){
        obj.usernamedate=false
        obj.usernamere=true

      }else{
        obj.usernamere=false
        obj.usernamedate=true
      }
    })

  } else {
    obj.usernameuse = true
    obj.usernamedate=false
    obj.usernamere=false
  }

})
const showalert = () => {
  if (obj.email.search(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/)
    != -1) {
    obj.emailalert = false
  } else {
    obj.emailalert = true
  }
  if (obj.password.search(/(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)/)
    != -1 && obj.password.length > 5) {
    obj.passwordalert = false
  } else {
    obj.passwordalert = true
  }
  if (obj.againpassword != obj.password) {
    obj.again = true
  } else {
    obj.again = false
  }
  if (obj.username.length >= 6) {
    obj.usernameuse = false

  } else {
    obj.usernameuse = true
  }
}
watch(() => obj.password, () => {
  if (obj.flag) {
    if (obj.password.search(/(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)/)
      != -1 && obj.password.length > 5) {
      obj.passwordalert = false
    } else {
      obj.passwordalert = true
    }
  }
})
const send = () => {
  obj.flag = true
  showalert()
  //verification fromdata is? true,验证formdata是否有效
  if (obj.username && obj.email && obj.password && obj.againpassword && !obj.usernameuse &&
    !obj.emailalert && !obj.passwordalert && !obj.again && !obj.usernamere) {
    obj.showac = false
    obj.actime = 6
    count()
    //send email auth code
    var data = new FormData()
    data.append('email', obj.email)
    http.post('/emailauth', data).then(res => {
      console.log(res.data)
      obj.djg_otop = res.data.auth
    })


  }


}
const signupsend = () => {
  var formdata = new FormData()
  formdata.append('username', obj.username)
  formdata.append('email', obj.email)
  formdata.append('password', obj.password)
  console.log(formdata)
  http.post('/signup', formdata).then(res => {
    console.log(res.data)

  })
}

// 倒数计时器函数
const count = () => {
  if (obj.actime <= 0) {
    obj.disbtn = false
    clearTimeout(ss)
    obj.showtimetext = false
    obj.actime = '未收到验证码请点击重新发送'
  } else {
    obj.disbtn = true
    obj.showtimetext = true
    obj.actime--
    var ss = setTimeout(count, 1000)
  }
}

// sgain send
const handleac = () => {
  obj.actime = 6
  count()
  var data = new FormData()
  data.append('email', obj.email)
  http.post('/emailauth', data).then(res => {
    console.log(res.data)
    obj.djg_otop = res.data.auth
  })


}
watch(() => obj.otp, (newvalue) => {

  if (newvalue.length === 6 && newvalue === obj.djg_otop) {
    obj.loading = true
    signupsend()

  } else if (newvalue.length === 6 && newvalue !== obj.djg_otop) {
    obj.otperror = true
  }
  else {
    obj.otperror = false
  }
})
</script>
<style lang="scss" >
.afrom {
  margin: 100px auto;
  width: 300px;

}

.textcolor {
  color: rgb(170, 5, 5);

}

.flash {
  animation: flash 1s ease-in-out 3;
}

@keyframes flash {
  0% {
    opacity: 1;
  }

  50% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}
</style>
