<template>
  <v-sheet >

    <v-sheet class="afrom" v-show="obj.emailpage">

      <div class="mt-10 mt-lg-5 mb-6 d-flex align-items-center d-lg-block">
        <span class="d-inline-block d-lg-block h1 mt-lg-n12 mb-lg-6 me-3">👋</span>
        <h1 class="lh-tight ls-tighter font-bolder d-inline-block d-lg-block h2 font-bolder">
          欢迎你的加入!
        </h1>
      </div>


      <v-sheet class="mt-1" height="150">
        <label class="text-h6">
          请输入你的Email
        </label>
        <v-sheet height="60">
          <v-text-field color="primary" variant="outlined" v-model="obj.email"></v-text-field>
        </v-sheet>



        <v-sheet class="text-end text-body-2">
          <span class="textcolor flash" v-if="obj.emailrename">
            <v-tooltip activator="parent" location="end" text="email已被注册">
              <template v-slot:activator="{ props }">
                <v-icon icon="mdi-account-cancel-outline" color="error" size="25" v-bind="props"></v-icon>
              </template>
            </v-tooltip>
          </span>
          <span v-if="obj.emailusename" class="">
            <v-tooltip activator="parent" location="end" text="email可以使用">
              <template v-slot:activator="{ props }">
                <v-icon icon="mdi-account-check-outline" color="success" size="25" v-bind="props"></v-icon>
              </template>
            </v-tooltip>
          </span>
          <span class="textcolor flash" v-if="obj.emailalert">
            <v-icon icon="mdi-email-alert" color="error"></v-icon>
            邮箱格式错误
          </span>
        </v-sheet>
      </v-sheet>


      <div class="d-grid mt-4">
        <v-btn @click="send" color="primary" class="text-h6" block height="50">
          注 册
        </v-btn>
      </div>


    </v-sheet>
    <v-sheet class="d-flex align-center flex-column" v-if="obj.otppage">

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

      <v-sheet class="afrom" v-if="obj.passwordpage">
        <p class="text-h3">欢迎使用</p>
      <p class="text-h5">邮箱{{obj.email}}验证成功</p>
        <v-sheet class=" mt-1" height="110">
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
  
      <v-sheet class=" mt-1" height="180">
       
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
        <v-btn @click="handlesnginup" color="primary" class="text-h6" block height="50">
          注 册
        </v-btn>
      </div>
      </v-sheet>
      <v-sheet class="d-flex justify-center align-center mt-5" height="600" v-if="obj.successpage">
        <v-sheet width="300" class="text-center">
          <p class="flashA"><v-icon icon="mdi-check-circle" size="160" color="success"></v-icon></p>
          <p class="text-h4 mt-5">注册成功</p>
          <p class="text-body-1">{{obj.backlogintime}}s后返回登录</p>
        </v-sheet>
      </v-sheet>
  </v-sheet>
</template>

<script setup>
import { reactive, onUpdated, watch } from 'vue'
import http from '@/util/axiosfz'
import { useRouter } from 'vue-router'
import { v4 as uuidv4 } from 'uuid'; 

const router=useRouter()
const obj = reactive({
  emailpage: true,
  otppage: false,
  email: '',
  emailalert: false,
  flag: false,
  otp: '',
  showtimetext: true,
  disbtn: true,
  actime: 300,
  djg_otop: '111111',
  emailrename: false,
  emailusename: false,
  password: '',
  passwordalert: false,
  emailalert: false,
  againpassword: '',
  show1:false,
  show2:false,
  again:false,
  successpage:false,
  passwordpage:false,
  backlogintime:3,

})
const emailalert = () => {
  if (obj.email.search(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/) != -1) {
    obj.emailalert = false

  } else {
    obj.emailalert = true
    obj.emailrename = false
    obj.emailusename = false
  }
}
//first page verify
const send = () => {
  obj.flag = true
  emailalert()
  if (obj.email && !obj.emailalert && !obj.emailrename) {
    obj.emailpage = false
    obj.otppage = true
    count()
    var data = new FormData()
    data.append('email', obj.email)
    http.post('/emailauth', data).then(res => {
      console.log(res.data)
      obj.djg_otop = res.data.auth
    })

  }

}
//验证Email是否已被使用
const emailusename = () => {
  var data = new FormData()
  data.append('email', obj.email)
  http.post('/usernamedete', data).then(res => {
    console.log(res.data.code)
    if (res.data.code === 0) {
      obj.emailusename = true
      obj.emailrename = false
    } else if (res.data.code === 1) {
      obj.emailrename = true
      obj.emailusename = false
    }

  })
}
watch(() => obj.email, () => {
  if(obj.flag){
    if (obj.email.length > 5) {
    emailalert()
  } else {
    obj.emailalert = false
    obj.emailrename = false
    obj.emailusename = false
  }

  if (obj.email.length > 5 && obj.emailalert === false) {
    emailusename()
  }}
  
})
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
// password 验证verify
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
watch(() => obj.againpassword, (newvalue, oldvalue) => {
    if (obj.againpassword.length >= obj.password.length && obj.againpassword != obj.password) {
      obj.again = true
    } else {
      obj.again = false
    }
  
})
// angin send
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
//watch otp page
watch(() => obj.otp, (newvalue) => {

  if (newvalue.length === 6 && newvalue === obj.djg_otop) {
    obj.loading = true
    obj.otppage=false
    obj.passwordpage=true

  } else if (newvalue.length === 6 && newvalue !== obj.djg_otop) {
    obj.otperror = true
  }
  else {
    obj.otperror = false
  }
})

//click signin注册 function
const handlesnginup=()=>{
  if(
    obj.password && obj.againpassword && obj.password===obj.againpassword && !obj.passwordalert
  ){
    
    var year = new Date().getFullYear()
    var month = new Date().getMonth()+1
    var day = new Date().getDate()

    var date = year + '-' + month + '-' + day
    var formdata=new FormData()
    formdata.append('email', obj.email)
    formdata.append('password', obj.password)
    formdata.append('date', date)
    formdata.append('userid', uuidv4().replace(/-/g, ''))
    console.log(formdata)
    http.post('/signup', formdata).then(res => {
    console.log(res.data)})
    obj.passwordpage=false
    obj.successpage=true
    countA()
    
    }

  }
  //倒计时count down function
  const countA = () => {
    console.log(obj.backlogintime)
  if (obj.backlogintime <= 0) {
    clearTimeout(ssa)  
    router.push('/login')
  } else {
  
    obj.backlogintime--
    var ssa = setTimeout(countA, 1000)
    
  }

}
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
.flashA {
  animation: flash 2s ease-in-out 1;
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
@keyframes flashA {
  0% {
    opacity: 0;
  }


  100% {
    opacity: 1;
  }
}
</style>
