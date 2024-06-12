<template>
    <v-sheet width="100%" class="pt-5 pl-3 pb-4 pr-5">
        <div class="d-flex align-center">
            <v-btn @click="router.back" prepend-icon="mdi-keyboard-backspace" color="primary">返回</v-btn>
            <v-spacer></v-spacer>
            <v-sheet v-show="obj.selfdata">
                <v-btn @click="payment" color="primary" v-if="!obj.data.payment">支付悬赏</v-btn>
                <v-btn @click="surefinish" color="primary" class="ml-2" v-show="obj.data.payment && !obj.data.finish">确认完成</v-btn>
                <v-btn color="primary" @click="handlereadd" class="ml-2">重新编辑</v-btn>
                <v-btn color="warning" class="ml-2" @click="handledel">删除项目</v-btn></v-sheet>
            <v-sheet v-show="!obj.selfdata">
                <v-btn class="ml-2 mr-5" color="primary" @click="receiveorder" v-show="!obj.data.takename">接单</v-btn>
                <v-btn class="ml-2 mr-5" color="primary" @click="orderfinish"
                    v-show="obj.data.takename == store.state.userdata.userid">提交</v-btn>
                <v-btn color="primary" icon="mdi-phone-incoming-outgoing-outline" @click="createchat(obj.data.takename)"></v-btn>

            </v-sheet>

        </div>
        <div v-show="!obj.selfdata" class="text-h6"> 发布：{{ obj.data.email }}</div>
        <div v-if="obj.selfdata && obj.orderfinisher" class="text-h6 mt-5">{{ obj.orderfinisher }}
            <span v-show="obj.finish">已完成 <span v-show="!obj.data.payment">支付后</span> </span>
            <span v-show="!obj.finish">未完成</span>
            <v-btn class="ml-3" :disabled="!obj.data.payment || !obj.finish" @click="obj.showfinish=!obj.showfinish" color="primary"> 查看提交
            </v-btn>
            <v-btn color="primary" class="ml-3" icon="mdi-phone-incoming-outgoing-outline" @click="createchatfinish(obj.data.takename)"></v-btn>
        </div>
        <v-sheet v-if="obj.showfinish">
           
            <Finish :orderid="obj.data.orderid" ></Finish>


        </v-sheet>

        <v-sheet>
            <v-sheet class="d-flex justify-center mt-5">
                <v-sheet width="800">
                    <v-row>
                        <v-col class="text-center text-h5 pl-4 pr-4">
                            {{ obj.data.title }}
                        </v-col>
                    </v-row>
                    <v-row width="100%">
                        <v-col>类别：{{ obj.data.type }}</v-col>
                        <v-col>完成时限：{{ obj.date }}</v-col>
                        <v-col>金额：{{ obj.data.money ? obj.data.money + '元' : '商议' }}</v-col>
                    </v-row>

                    <pre class="mt-4" v-for="text in obj.textlist" :key="text">&nbsp;&nbsp;{{ text }}</pre>
                    <Filedetail :data="data" v-for="data in obj.data.contentdetail?.files || []" :key="data.uuidname">
                    </Filedetail>
                </v-sheet>
            </v-sheet>
        </v-sheet>


        <v-dialog v-model="obj.showdel" width="auto">
            <v-card max-width="400">
                <v-card-title>
                    <v-icon icon="mdi-alert" color="warning"></v-icon>
                    注意
                </v-card-title>
                <v-card-item>
                    项目删除后将不可恢复，请提前下载项目文件
                </v-card-item>
                <template v-slot:actions>
                    <v-spacer></v-spacer>
                    <v-btn class="ms-auto" text="确定" @click="dialog"></v-btn>
                    <v-btn class="ms-auto" text="取消" @click="obj.showdel = false"></v-btn>
                </template>
            </v-card>
        </v-dialog>
    </v-sheet>
</template>
<script setup>
import { reactive, onMounted, onBeforeMount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/util/api'
import Filedetail from '../showdetail/Filedetail.vue'
import { useStore } from 'vuex';
import getdata from '@/plugins/getuserdata'
import Finish from '@/components/projectfinish/Finish.vue'
// import 
const store = useStore()
// import route from '@/router';
const route = useRoute()
const router = useRouter()

const obj = reactive({
    data: {},
    textlist: [],
    selfdata: false,
    userid: null,
    orderfinisher: null,
     showfinish: false, 

})
const payment = () => {
    var formdata = new FormData()
    formdata.append('orderid', route.query.orderid)
    formdata.append('userid', store.state.userdata.userid)
    // api.httptk.post('/payment',formdata).then(
    // response=>{
    //     console.log(response.data)
    //     // 这里return 的是后端的支付链接或
    //     if (response.data.paymentUrl) {
    //       // 跳转到支付页面
    //       window.location.href = response.data.paymentUrl;
    //     } else if (response.data.qrCodeUrl) {
    //       // 显示支付二维码
    //       this.showQrCode(response.data.qrCodeUrl);
    //     }

    // }
    // )
    // 使用websocket监控支付结果
    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/payment/${route.query.orderid}/`);

    ws.onopen = () => {
        console.log('WebSocket connection established');
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        // if (data.message === 'success') {
        //   console.log('Payment result received successfully');
        //   alert('支付成功');

        // }
    };

}
const getorderfinisher = (id) => {
    if(id){
let formdata = new FormData()
    formdata.append('userid', id)
    api.httptk.post('/userdata', formdata).then(response => {
       
            obj.orderfinisher = response.data.email
        
        
    })

    }
    

}

const receiveorder = () => {
    var formdata = new FormData()
    formdata.append('orderid', route.query.orderid)
    formdata.append('userid', store.state.userdata.userid)
    api.httptk.post('/receiveorder', formdata).then(
        response => {
            if (response.data.res == 'success') {
                
               
                router.push('/userhome/tproject')
            } else {

            }

        }
    )
}
const orderfinish = (data) => {
    
    router.push({
        path: '/userhome/tproject/finish', query: {
            orderid: obj.data.orderid
        }
    })
}


onBeforeMount(() => {
    
    var formdata = new FormData()
    formdata.append('id', route.query.orderid)
    api.httptk.post('/getorderdetail', formdata).then(res => {
        obj.data = res.data
        getorderfinisher(obj.data.takename)
        getfinish(obj.data.orderid)
        obj.data.contentdetail = JSON.parse(obj.data.contentdetail)
        obj.email = res.data.email
        if (store.state.userdata.email === res.data.email) {
            obj.selfdata = true
        } else {
            obj.selfdata = false
        }


        for (var n in obj.data.contentdetail.text.sort(function (a, b) { return a.index - b.index })) {
            var formdata = new FormData()
            formdata.append('t_fid', obj.data.contentdetail.text[n].uuidname)
            formdata.append('email', res.data.email)
            api.httptk.post('/getorderdetail', formdata).then(res => {
                obj.textlist.push(res.data.content)
            }
            )
        }
    })

})
const getfinish = (id) => {
    let formdata = new FormData()
    formdata.append('id', id)
    formdata.append('type', 'get')
    api.httptk.post('/orderfinish', formdata).then(res => {
        obj.finish = res.data.finish


    })



}
const surefinish=()=>{
    let formdata = new FormData()
    formdata.append('id', obj.data.orderid)
    api.httptk.post('/surefinish',formdata).then(response=>{
        if(response.data){
            router.push('/userhome/myproject')
        }

    }


    )
}

const handlereadd = () => {
    router.push({
        path: '/userhome/myproject/reprojectadd', query: {
            orderid: obj.data.orderid, email: obj.data.email
        }
    })
}



const createchat = async () => {
    let userdata = null
    userdata = await getdata.getdata(false, obj.data.email)
    let flag = false
    for (let a of store.state.messagelist) {
        if (a.contact === userdata.userid) {
            flag = true
        }
    }
    if (!flag) {
        store.commit('createchat', userdata)
    }
    flag = false
    store.commit('openmessage')


}
const createchatfinish = async (userid) => {
    let userdata = null
    
    userdata = await getdata.getdata(userid,false)
   
    let flag = false
    for (let a of store.state.messagelist) {
        if (a.contact === userdata.userid) {
            flag = true
        }
    }
    if (!flag) {
        store.commit('createchat', userdata)
    }
    flag = false
    store.commit('openmessage')


}


const dialog = () => {

    obj.showdel = false
    var formdata = new FormData()
    formdata.append('oldorderid', obj.data.orderid)
    formdata.append('email', obj.data.email)
    api.httptk.post('/updataorder', formdata).then(res => {

    })

}
const handledel = () => {
    obj.showdel = true

}


</script>
<style lang="scss" scoped>
pre {
    word-wrap: break-word;
    white-space: pre-wrap;
}
</style>