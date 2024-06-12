<template>
    <v-sheet class="d-flex overflow-hidden" width="800" height="610">
        <v-sheet width="220" class="text-center">
            <v-sheet>
                <v-sheet>
                    <p class="text-h6 align-self-center"> 联系人list </p>
                </v-sheet>
                <v-sheet class="d-flex align-start">
                    <v-text-field label="Search" variant="underlined" density="comfortable" class="ml-1 mt-1"
                        v-model="obj.search"></v-text-field>
                    <!-- <v-btn    icon="mdi-account-search-outline" size="30" variant="text"  @click="search"></v-btn> -->
                </v-sheet>
            </v-sheet>
            <v-sheet height="500" class="overflow-auto ml-5" width="230">
                <div v-if="store.state.messagelist.length!==0">
                <Messagelist v-for="data, index in store.state.messagelist" :data="data" :index="index" :key="index"
                    :unread="handleunread(data)" :nowindex="obj.nowindex" @click="handlecreatechat(data, index)">
                </Messagelist> </div>
                <div v-if="store.state.messagelist.length==0" class="text-center text-h6">
                无联系人</div>
            </v-sheet>
        </v-sheet>
        <v-sheet class="border-s-lg border-success border-opacity-75">
            <div calss="text-center" style="position: absolute;
                    width: 200px;
                    top:200px;
                    right:240px;" v-if="obj.showup">
                              <p class="text-center">上传中...</p>
            <div style="border-radius:15px;overflow: hidden;">
                <v-progress-linear v-model="obj.skill" color="yellow" height="25">
                    <template v-slot:default="{ value }">
                        <strong>{{ obj.skill }}%</strong>
                    </template>
                </v-progress-linear>
            </div>
            </div>
            <v-sheet width="570" class="" height="400">
                <v-sheet height="400" width="100%" class="overflow-hidden">

                    <div v-if="obj.messagedetail">
                        <Messagedetail :data="obj.messagedetail"></Messagedetail>

                    </div>

                </v-sheet>


            </v-sheet>
            <v-sheet height="30" class="bg-teal-darken-1 text-start  rounded-lg">
                <v-menu location="end">
                    <!-- emoji -->
                    <template v-slot:activator="{ props }" id="drop">
                        <v-icon icon="mdi-emoticon-happy-outline" size="25" class="ml-3 mt-1 bg-yellow rounded-circle"
                            color="black" v-bind="props"></v-icon>
                    </template>

                    <v-card min-width="300" max-width="350">
                        <span>&#128544;</span>
                        <span v-for="em in obj.emojilist" :key="em">{{ em }}</span>
                    </v-card>
                </v-menu>
                <!-- input file -->
                <v-icon icon="mdi-folder-plus-outline" color="black" size="25" class="ml-3 mt-1"
                    onclick="document.getElementById('fileField').click()" style="cursor:pointer;"></v-icon>
                <input type="file" id="fileField" v-show="false" @change="uploadFiles">
            </v-sheet>

            <div>
                <!-- <div id="show" style="
                                opacity: 0;
                                text-align: center;
                                ">
                    <v-icon icon="mdi-folder-plus-outline" color="black" size="60" class=" mt-3"></v-icon>
                </div> -->
                <div @drop.prevent="handleFileDrop">
                    <v-textarea variant="outlined" style="border: none;outline:none;" @keydown.enter="send"
                        id="drop-area" v-model="obj.text" density="compact"> </v-textarea>
                </div>

                <div width="100%" class="d-flex justify-end mt-n5">
                    <v-btn color="success mr-5" @click="send">send</v-btn>
                </div>
            </div>

        </v-sheet>
        
    </v-sheet>

</template>
<script setup>

import { reactive, onMounted, watch } from 'vue';
import Messagelist from './Messagelist.vue'
import Messagedetail from './Messagdetail.vue';
import { useStore } from 'vuex';
import { v4 as uuidv4 } from 'uuid'
import def from '@/plugins/getdate'
import api from '@/util/api';

const store = useStore()
const obj = reactive({
    drop: false, text: '', dialog: false,
    contact: [],
    isshow: false,
    oldmessagelist: [ //里面的每一个dict就是一个联系人详情，
    ],
    messagelist:[],
    storemessage: null,
    userlist: [],
    newmessagelist: [],
    nowcontact: '',//当前联系人
    messagedetail: null,//nowcontact messaeglist
    search: '',
    emojilist: [], number: 0, nowindex: null,
    file: null,
    imageurl: null,
    showup: false,
    skill: 0,
})
const handleunread = (data) => {
    var unread = 0
    for (var a of data.content) {
        if (!a.unread && data.contact === a.from) {
            unread++
        }
    }
    return unread
}

onMounted(() => {
    
    
    if(store.state.messgaelist!==0){
         handlecreatechat(store.state.messagelist[0], 0)
    }
    for (var n = 128512; n <= 128640; n++) {
        obj.emojilist.push('&#' + n + ';')
    }


})
watch(() => obj.search, (value, oldvalue) => {
        store.commit('filtermessage',obj.search)


})

const send =async() => {

    if (!store.state.ws || !obj.nowcontact ||obj.text===''||obj.text.trim()==='') {
        obj.text=''
        return
    }
    var data = {
        messageid: uuidv4(), from: store.state.userdata.userid, to: obj.nowcontact,
        type: 'text', content: obj.text, uuidname: '', senddate: def.gettime(new Date()), unread: false
    }
    store.state.ws.send(JSON.stringify(data))
    DBadd(data)//add indexdb
    store.commit('addmessage', { a: obj.nowcontact, b: data })
    await claen()
    
}
const claen=async()=>{
    obj.text=''
}
const DBadd = (message) => {
    if (!store.state.db) {
        console.error('Database is not ready');
        return;
    }
    const tx = store.state.db.transaction(['message'], 'readwrite');
    const store1 = tx.objectStore('message');
    store1.add(message).onsuccess = function (event) {
    };
}

const handlecreatechat = (data, index) => {
    var ele = document.querySelectorAll('.ashow')
    var ava = document.querySelectorAll('.av')
    obj.nowcontact = data.contact
    obj.messagedetail = data
    obj.nowindex = index
    for (var n = 0; n < ele.length; n++) {

        ele[n].classList.remove('ahover')
        ava[n].classList.remove('avathover')

    }
    ele[index].classList.add('ahover')
    ava[index].classList.add('avathover')


}

function handleFileDrop(event) {
    event.preventDefault();
    handlefileuopload(event.dataTransfer.files[0])
}

function uploadFiles() {
    handlefileuopload(document.getElementById("fileField").files[0])
}
const handlefileuopload = async(file) => {
    let filenamelist = file.name.split('.').length - 1
    if (['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'psd', 'svg', 'tiff', 'image'].indexOf(file.name.split('.')[filenamelist]) >= 0) {
        //
        const reader = new FileReader();
        reader.onload = function (e) {
            const base64String = e.target.result;

            var data = {
                messageid: uuidv4(), from: store.state.userdata.userid, to: obj.nowcontact,
                type: 'image', content: base64String, uuidname: file.name, senddate: def.gettime(new Date()), unread: false
            }

            store.state.ws.send(JSON.stringify(data))
            DBadd(data)//add indexdb
            store.commit('addmessage', { a: obj.nowcontact, b: data })

        };
        reader.readAsDataURL(file);
    } else {
        obj.showup = true
        obj.skill=0
        let uuidname = uuidv4() + '.' + file.name.split('.').slice(-1)
        var data = {
            messageid: uuidv4(), from: store.state.userdata.userid, to: obj.nowcontact,
            type: 'file', content: file.name, uuidname: uuidname, senddate: def.gettime(new Date()), unread: false
        }
       
        var fromdata = new FormData()
        fromdata.append('file', file)
        fromdata.append('type', 'up')
        fromdata.append('uuidname', uuidname)
        fromdata.append('adddate',def.gettime(new Date()))
        
       await api.httpdetail.post('/messagefile', fromdata, {
            onUploadProgress: (progressEvent) => {
                const totalLength = progressEvent.total;
                if (totalLength !== null) {
                    obj.skill = Math.round((progressEvent.loaded * 100) / totalLength);
                }
            }
        }).then(response => {
            obj.showup = false
        })

        store.state.ws.send(JSON.stringify(data))
        DBadd(data)//add indexdb
         store.commit('addmessage', { a: obj.nowcontact, b: data })

    }

}

</script>

<style lang="scss" scoped>
.a {
    background-color: white;
    // border: 2px solid rgb(23, 131, 203);
    border-radius: 2px;
    // border-bottom: 1px solid rgb(147, 147, 144) // elevation: abs($number: )
    // box-shadow:60px -16px teal
}

.show {
    position: relative;
    top: -70px;
    opacity: 1;

    text-align: center;


}

.ahover {
    box-shadow: 10px 5px 5px rgb(81, 130, 79);
    border: 1.5px solid rgb(13, 160, 72);
    height: 70px;
}

.avathover {
    width: 60px;
}

.showfile {
    position: absolute;
    align-items: center;
    justify-content: center;
    width: 100px;
    height: 100px;
    top: 50px;
    left: 100px;
    border: 1px solid black;

}
</style>