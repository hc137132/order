<template>

    <v-sheet class="d-flex align-center justify-center" width="100%" min-height="600">
        <v-sheet v-show="obj.show">
            <v-sheet class="d-flex align-center mt-2">
                <v-sheet width="100" class="text-h6 text-right ">
                    头像：
                </v-sheet>
                <v-sheet>
                    <div v-if="$store.state.userdata.avatar" style="width: 70px;height: 70px;border-radius: 50%;
  overflow: hidden;display: flex;align-items: center;justify-content: center;">
                        <img style="max-height: 100%;" :src="obj.avatar" alt="">
                    </div>
                    <v-icon icon="mdi-account-circle" v-if="!$store.state.userdata.avatar" size="80"
                        color="#42A5F5"></v-icon>
                </v-sheet>
            </v-sheet>
            <v-sheet class="d-flex align-center mt-3">
                <v-sheet width="100" class="text-h6 text-right">
                    email：
                </v-sheet>
                <v-sheet width="180" class="text-center"> <span class="text-h6">{{ obj.userdata.email
                        }}</span></v-sheet>
            </v-sheet>
            <v-sheet class="d-flex align-center mt-3">
                <v-sheet width="100" class="text-h6 text-right">
                    昵称：
                </v-sheet>
                <v-sheet> <span class="text-h6">{{ obj.userdata.nickname }}</span>

                </v-sheet>
            </v-sheet>
            <v-sheet class="d-flex align-top mt-3">
                <v-sheet width="100" class="text-h6 text-right">
                    电话：
                </v-sheet>
                <v-sheet><span class="text-h6 text-center">{{ obj.userdata.phonenumber }}</span>
                </v-sheet>
            </v-sheet>
            <v-sheet class="d-flex mt-3">
                <v-sheet width="100" class="text-h6 text-right">
                    简介：
                </v-sheet>
                <v-sheet width="200" min-height="200"><span class="text-h6">{{ obj.userdata.introduction
                        }}</span> </v-sheet>
            </v-sheet>
            <v-sheet class="mt-2  d-flex justify-center">
                <v-btn width="200" height="50" color="primary" class="text-h6" @click="updatauser">
                    修改资料</v-btn>
            </v-sheet>
        </v-sheet>

        <!-- 修改资料 -->
        <v-sheet v-show="obj.userupdatashow" width="80%" >
            <v-row>
                <v-col lg="6" md="12" sm="12">
                    <v-sheet class="d-flex align-center  ">
                        <v-sheet width="150" class="text-h6 text-right">
                            头像：
                        </v-sheet>
                        <v-sheet class="d-flex align-start justify-center" width="200">
                            <div size="70px" style="border-radius: 50% 50%;width: 100px;height: 100px;">
                                <img :src="obj.image" style="width: 100px;height: 100px;;border-radius: 50% 50%;">
                            </div>

                        </v-sheet>
                        <v-sheet class="text-center">
                            <v-btn color="primary" @click="obj.dialog = true" text="修改"></v-btn>

                            <v-dialog v-model="obj.dialog" width="auto">
                                <v-card width="500" title="Update Your Avatar">
                                    <Updataavatar @geturl="geturl"></Updataavatar>
                                    <template v-slot:actions>
                                        <v-btn class="ms-auto" text="取消" @click="obj.dialog = false"></v-btn>
                                    </template>
                                </v-card>
                            </v-dialog>

                        </v-sheet>

                    </v-sheet>

                </v-col>

                <v-col lg="6" md="12" sm="12">
                    <v-sheet class="d-flex align-center" height="100%">
                        <v-sheet width="150" class="text-h6 text-right">
                            Email：
                        </v-sheet>
                        <v-sheet width="200" class="text-center"> <span>{{ obj.userdata.email }}</span></v-sheet>
                    </v-sheet>
                </v-col>
            </v-row>
            <v-row>
                <v-col lg="6" md="12" sm="12">
                    <v-sheet class="d-flex align-center " width="100%">
                        <v-sheet width="150" class="text-h6 text-right">
                            昵称：
                        </v-sheet>
                        <v-sheet width="200"> <v-text-field variant="underlined"
                                v-model="obj.userupdata.nickname"></v-text-field></v-sheet>
                    </v-sheet>
                </v-col>
                <v-col lg="6" md="12" sm="12">
                    <v-sheet class="d-flex align-center ">
                        <v-sheet width="150" class="text-h6 text-right">
                            手机号码：
                        </v-sheet>
                        <v-sheet width="200"><v-text-field variant="underlined"
                                v-model="obj.userupdata.phonenumber"></v-text-field></v-sheet>
                    </v-sheet>
                </v-col>

            </v-row>
            <v-row>
                <v-col>
                    <v-sheet class="d-flex align-start " width="100%">
                        <v-sheet width="150" class="text-h6 text-right">
                            个人简介：
                        </v-sheet>
                        <v-sheet width="80%">
                            <v-textarea clearable v-model="obj.userupdata.introduction" variant="outlined"></v-textarea>

                        </v-sheet>
                    </v-sheet>
                </v-col>


            </v-row>
            <p class="text-body-2" v-show="obj.emailshow">将使用邮箱验证,请确保你的邮箱可用</p>
            <v-sheet class="mt-2 d-flex justify-center">
                <v-btn width="200" height="50" color="primary" class="text-h6" @click="handupdata"> 提交</v-btn>
            </v-sheet>

        </v-sheet>
        <!-- 修改密码 -->

    </v-sheet>
</template>

<script setup>
import { reactive, onUpdated, watch, onMounted, onBeforeMount } from 'vue';
import { useStore } from 'vuex'
import Updataavatar from './cropper1.vue'
import api from '@/util/api'
import { v4 as uuidv4 } from 'uuid'

// const uuid = require('uuid')
const store = useStore()
const obj = reactive({
    userupdata: {
        avatar: null,
        introduction: '', nickname: '', phonenumber: '',

    },
    show: true,
    email: '',
    image: null,
    filesize: 40,
    istool: false,
    imgfile: '',
    filename: '',
    avatar: null, dialog: false,
    userdata: null,
    userupdatashow: false,
    arr: ['avatar', 'introduction', 'nickname', 'phonenumber']

})

onBeforeMount(() => {
    obj.userdata = store.state.userdata
    obj.arr.forEach((val) => {
        obj.userupdata[val] = store.state.userdata[val]

    })
    

})


const geturl = (val) => {
    if (val) {
        obj.image = val
        obj.userupdata.avatar = val
    }
    obj.dialog = false
}

onMounted(() => {
    obj.userdata = store.state.userdata
    obj.avatar = `data:image/png;base64,${store.state.userdata.avatar}`
    obj.image = `data:image/png;base64,${obj.userupdata.avatar}`
    


})

function getfile(e) {
    var files = e.target.files
    var newimg = window.URL.createObjectURL(files[0])
    obj.image = newimg
    obj.filename = files[0].name
}
function handledrop(event) {
    event.preventDefault();
    obj.filesize = 40
    const file = event.dataTransfer.files
    var newimg = window.URL.createObjectURL(file[0])
    obj.filename = file[0].name
    obj.image = newimg

}
function enter(event) {
    event.stopPropagation();
    event.preventDefault();
    obj.filesize = 70
}
function leave(event) {
    event.stopPropagation();
    event.preventDefault();
    obj.filesize = 40
}
const updatauser = () => {
    obj.userupdatashow = !obj.userupdatashow
    obj.show = !obj.show
}





const handupdata = () => {
    var data = new FormData()
    data.append('email', obj.userdata.email)
    obj.arr.forEach((val) => {
        if (obj.userdata[val] != obj.userupdata[val] && obj.userupdata[val]!== '') {
            data.append(val, obj.userupdata[val])
        }else if(obj.userdata[val] != obj.userupdata[val] && obj.userupdata[val] === ''){
            data.append(val, '%Null%')
        }
    })
    api.httptk.post('/userupdate', data).then(res => {
        api.httptk.post('/userdata', data).then(res => {
                store.commit('updatauser', res.data)//updateuser)
                location.reload()

    }
    )

})
}



</script>
<style lang="scss" scoped></style>