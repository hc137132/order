<template>
  <v-app>


    <v-system-bar window class="end">
      <v-icon icon="mdi-abjad-arabic"></v-icon>
      <v-spacer></v-spacer>
      <v-icon icon="mdi-signal" class="ms-2"></v-icon>
      <v-icon icon="mdi-battery" class="ms-2"></v-icon>

      
    </v-system-bar>


    <v-main>

      <v-sheet width="300" class="mx-auto mt-5" v-show="obj.isShow">
        <p class="text-body-1">你将使用邮箱验证</p>
        <v-text-field  label="Username"></v-text-field>
        <p class="text-body-2">该用户不存在</p>
        <v-btn block class="align-self-center bg-purple-lighten-2" height="50" @click="send">Submit</v-btn>


      </v-sheet>
      <v-sheet width="300" class="mx-auto mt-5" v-show="obj.isshow">
        <p>已向username：{{ obj.username }}发送验证码,请输入验证码</p>
        <v-otp-input v-model="obj.data" length="6"></v-otp-input>

        <v-btn block class="align-self-center bg-purple-lighten-2" height="50">Submit</v-btn>
        <v-sheet class="d-flex 
align-center">
        未收到验证码<v-btn variant="text" class="align-self-center">
 重新发送 
</v-btn></v-sheet>
      </v-sheet>
    </v-main>
    <!-- <footer></footer> -->

    <v-footer class="bg-indigo-lighten-1 text-center d-flex flex-column">
      <div>
        <v-btn v-for="icon in icons" :key="icon" class="mx-4" :icon="icon" variant="text"></v-btn>
      </div>

      <div class="pt-0">
        Phasellus feugiat arcu sapien, et iaculis ipsum elementum sit amet. Mauris cursus commodo interdum. Praesent ut
        risus eget metus luctus accumsan id ultrices nunc. Sed at orci sed massa consectetur dignissim a sit amet dui.
        Duis commodo vitae velit et faucibus. Morbi vehicula lacinia malesuada. Nulla placerat augue vel ipsum ultrices,
        cursus iaculis dui sollicitudin. Vestibulum eu ipsum vel diam elementum tempor vel ut orci. Orci varius natoque
        penatibus et magnis dis parturient montes, nascetur ridiculus mus.
      </div>

      <v-divider></v-divider>

      <div>
        {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
      </div>
    </v-footer>
  </v-app>
</template>

<script>
import { reactive } from 'vue'

export default {


  setup() {
    const obj = reactive({
      username: '',
      data: '555333',
      isShow:true,
      isshow:false
    })
    const send=()=>{
      obj.isShow=false
      obj.isshow=true
    }
    return {
      obj,
      send
    }
  }

}
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
</style>
