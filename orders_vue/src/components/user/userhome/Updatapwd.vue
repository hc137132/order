<template>
    <v-sheet class="d-flex align-center justify-center" width="100%" min-height="600">

        <v-sheet width="400">

            <v-sheet class="d-flex align-center mt-3">
                <v-sheet class="text-h6">
                    用户ID：
                </v-sheet>
                <v-sheet> <span>{{ store.state.userdata.email }}</span></v-sheet>
            </v-sheet>

            <v-sheet class="d-flex align-center mt-3">
                <v-sheet class="text-h6" width="180">
                    原始密码：
                </v-sheet>
                <v-sheet width="100%"><v-text-field v-model="obj.password" variant="underlined"
                        :append-inner-icon="obj.show ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append-inner="obj.show = !obj.show"
                        :type="obj.show ? 'text' : 'password'"></v-text-field></v-sheet>
            </v-sheet>
            <p class="text-body-2" v-show="obj.pwderror"><v-icon icon="mdi-alert-circle-outline" color="error"
                    size="30"></v-icon> 你输入的密码有误</p>
            <v-sheet class="d-flex align-center mt-3">
                <v-sheet class="text-h6" width="180">
                    新密码：
                </v-sheet>
                <v-sheet width="100%">
                    <v-text-field v-model="obj.npassword" :append-inner-icon="obj.show1 ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append-inner="obj.show1 = !obj.show1" :type="obj.show1 ? 'text' : 'password'"
                        variant="underlined"></v-text-field>
                </v-sheet>

            </v-sheet>
            <v-sheet class="text-end text-body-2" v-if="obj.passwordalert">
                <p class="textcolor flash">
                    <v-icon icon="mdi-alert-circle-outline" color="error" size="20"></v-icon> 密码至少6位且包含大小写字母数字
                </p>
            </v-sheet>
            <v-sheet class="d-flex align-center mt-3">
                <v-sheet class="text-h6" width="180">
                    确认密码：
                </v-sheet>
                <v-sheet width="100%"><v-text-field :append-inner-icon="obj.show2 ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append-inner="obj.show2 = !obj.show2" :type="obj.show2 ? 'text' : 'password'"
                        v-model="obj.napassword" variant="underlined"></v-text-field>

                </v-sheet>


            </v-sheet>
            <p class="text-body-2" v-if="obj.istool"> <v-icon icon="mdi-alert-circle-outline" color="error"
                    size="30"></v-icon>你两次输入的密码不相同</p>
            <v-sheet class="mt-2 d-flex justify-center">
                <v-btn width="200" height="50" color="primary" class="text-h6" @click="handleupdatepwd"> 提交</v-btn>
            </v-sheet>

        </v-sheet>
    </v-sheet>
</template>

<script setup>
import { reactive, onUpdated, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import api from '@/util/api';

const store = useStore()
const router = useRouter()

const obj = reactive({
    userupdata: false,
    show: false,
    show1: false,
    show2: false,
    password: '',
    npassword: '',
    napassword: '',
    pwderror: false,
    passwordalert: false,

})
watch(() => obj.napassword, (newpwd, oldpwd) => {
    if (newpwd && newpwd !== obj.npassword) {
        obj.istool = true
        console.log('ssss')
    } else {
        obj.istool = false
    }
})
watch(() => obj.npassword, () => {

    if (obj.npassword.search(/(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)/)
        == -1 && obj.npassword.length > 5) {
        obj.passwordalert = true
    } else {
        obj.passwordalert = false
    }
})
const handleupdatepwd = () => {
    if (!obj.passwordalert && !obj.istool && obj.password && obj.napassword) {
        let formdata = new FormData()
        formdata.append('userid', store.state.userdata.userid)
        formdata.append('pwd', obj.password)
        formdata.append('newpwd', obj.npassword)
        api.httptk.post('/repwd',formdata).then(res => {
            console.log(res.data)
            if (res.data.code === 'success') {
                router.push('/userhome/user')
            } else {
                obj.pwderror = true
            }
         }
        )

    }



}






</script>
<style lang="scss" scoped></style>