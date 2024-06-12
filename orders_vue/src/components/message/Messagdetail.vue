<template>
    <div>
        <v-sheet class="d-flex justify-center overflow-hidden">
            <v-sheet class="text-h6 text-center mt-4" width="100%">与{{ props.data.userdata.email }}的会话
            
            </v-sheet>
       
        </v-sheet>
        <div ref="chatContainerRef" style="width: 100%;height: 350px;overflow: auto;">

            <v-sheet v-for="message, index in props.data.content">
                <!-- time -->
                <v-sheet
                    v-if="props.data.content[index].senddate - props.data.content[Math.max(0, index - 1)].senddate > 3600 || index == 0"
                    class="d-flex justify-center" width="100%">
                    <v-sheet class="pa-2 bg-">
                        <span class="text-body-2">
                            {{ def.date(message.senddate) }} {{ def.gettimetime(message.senddate) }}</span>
                    </v-sheet>
                </v-sheet>

                <!-- avatar and username -->
                <v-sheet v-if="props.data.contact === message.from">
                    <v-sheet>
                        <v-avatar>
                            <v-img v-if="props.data.userdata.avatar"
                                :src="'data:image/*;base64,' + props.data.userdata.avatar" alt="John"></v-img>
                            <v-icon icon="mdi-account-circle" v-if="!props.data.userdata.avatar" size="50"
                                color="#42A5F5"></v-icon>
                        </v-avatar><span>{{ props.data.userdata.email }}</span>
                    </v-sheet>
                    <!-- message -->
                    <v-sheet v-if="message.type == 'image'" class="d-flex" width="100%">
                        <img :src="message.content" alt="" style="max-width: 100px; max-height: 200px;" />
                    </v-sheet>
                    <v-sheet class="d-flex" v-if="message.type == 'text' || message.type == 'file'">
                        <v-sheet class="ma-2 rounded-lg bg-success pa-2" max-width="260">
                            <p v-if="message.type == 'file'" style="cursor: pointer;" class="text-center"
                                @click="download(message.content, message.uuidname)">
                                <v-icon icon="mdi-file-download-outline" size="30"> </v-icon>
                                <p>{{message.content}}</p>
                            </p>
                            <span v-if="message.type == 'text' "> {{ message.content }} </span>
                        </v-sheet>
                    </v-sheet>
                </v-sheet>

                <!-- right -->
                <v-sheet v-if="message.from === store.state.userdata.userid" class="text-end">

                    <v-sheet>
                        <v-avatar>
                            <v-img v-if="store.state.userdata.avatar"
                                :src="'data:image/*;base64,' + store.state.userdata.avatar" alt="John"></v-img>
                            <v-icon icon="mdi-account-circle" v-if="!store.state.userdata.avatar" size="50"
                                color="#42A5F5"></v-icon>
                        </v-avatar>
                    </v-sheet>

                    <!-- message -->
                    <v-sheet v-if="message.type == 'image'" class="d-flex justify-end " width="100%">
                        <img :src="message.content" alt="" style="max-width: 100px; max-height: 200px;cursor: pointer;"
                            @click="handleimage(message.content, message.uuidname)" />
                        <v-sheet width="20"></v-sheet>
                    </v-sheet>

                    <v-sheet width="100%" class="d-flex justify-end mr-3" v-if="message.type != 'image'">
                        <v-sheet class="ma-2 rounded-lg bg-success pa-2 " max-width="260">
                            <p v-if="message.type == 'file'" style="cursor: pointer;" class="text-center"
                                @click="download(message.content, message.uuidname)">
                                <v-icon icon="mdi-file-download-outline" size="30"> </v-icon>
                                <p>{{message.content}}</p>
                            </p>
                            <span v-if="message.type == 'text'"> {{ message.content }} </span>


                        </v-sheet>

                    </v-sheet>

                </v-sheet>

            </v-sheet>


        </div>

        <div class="showdown" v-if="obj.showdown">
            <p>下载中...</p>
            <div style="border-radius: 15px;overflow: hidden;">
                <v-progress-linear v-model="obj.skill" color="yellow" height="25">
                    <template v-slot:default="{ value }">
                        <strong>{{ obj.skill }}%</strong>
                    </template>
                </v-progress-linear>
            </div>


        </div>

    </div>
</template>
<script setup>
import { reactive, onMounted, watch, ref, onUpdated } from 'vue';
import { useStore } from 'vuex';
import api from '@/util/api'
import def from '@/plugins/getdate'

const chatContainerRef = ref(null);
const store = useStore()
const obj = reactive({
    list: [], showdown: false, skill: 0,
})

const props = defineProps({
    data: null,
    db: null,
})
onMounted(() => {
    
    scrollToBottom();
  
  

})
const scrollToBottom = () => {
    if (chatContainerRef.value) {
        chatContainerRef.value.scrollTop = chatContainerRef.value.scrollHeight;
    }
};
watch(() => props.data, (newvalue, oldvalue) => {
    // 改变unread==true
    handlestoreunread(props.data)

    // console.log(props.data.content,newvalue.content)

}, { deep: true })

onUpdated(scrollToBottom)


const handlestoreunread = (data) => {
    var list = []
    if (data) {
        for (let a in data.content) {
            if (!data.content[a].unread) {
                var b = data.content[a]
                b.unread = true
                list.push(b)//改变store，
                // console.log('yes read')
                handleunread(data.content[a].messageid)//改变indexdb

            } else {
                list.push(data.content[a])
            }
        }
    }
    //    console.log({contact:data.contact,content:list})
    store.commit('updatemessage', { contact: data.contact, content: list })
}
// 消除 indexdb unread
const handleunread = (id) => {

    const request = indexedDB.open('message', 1)
    request.onsuccess = function (event) {
        const db = event.target.result;
        // 创建一个读写事务  
        const transaction = db.transaction(['message'], 'readwrite');
        const objectStore = transaction.objectStore('message');

        // 使用 get 方法根据主键查找数据  
        const getRequest = objectStore.get(id);

        getRequest.onsuccess = function (event) {
            const data = event.target.result;
            if (data) {
                // 修改数据  
                data.unread = false;
                // console.log(data.unread)
                //   使用 put 方法更新数据  
                const putRequest = objectStore.put(data);
                putRequest.onsuccess = function (event) {
                    // console.log('Data updated successfully');  
                };

                putRequest.onerror = function (event) {
                    console.error('Error updating data', event.target.errorCode);
                };
            } else {
                console.log('No data found for the given primary key');
            }
        };

        getRequest.onerror = function (event) {
            console.error('Error fetching data', event.target.errorCode);
        };

    }
}

const handleimage = (imgurl, filename) => {

    if (window.navigator.msSaveOrOpenBlob) {
        const bstr = atob(imgurl.split(',')[1])
        let n = bstr.length
        const u8arr = new Uint8Array(n)
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n)
        }
        const blob = new Blob([u8arr])
        window.navigator.msSaveOrOpenBlob(blob, 'chart-download' + '.' + 'png')
    } else {
        // 这里就按照chrome等新版浏览器来处理
        const a = document.createElement('a')
        a.href = imgurl
        a.download = filename
        // a.setAttribute('download', 'chart-download')
        a.click()
    }
}




const download = (filename, id) => {
    console.log(filename,id)
    obj.showdown = true
    obj.skill = 0
    var formdata = new FormData()
    formdata.append('type','down')
    formdata.append('uuidname', id)
    api.httpdetail.post('/filedown', formdata, {
        responseType: 'blob',
        onDownloadProgress: (progressEvent) => {
            const totalLength = progressEvent.total;
            const downloadedLength = progressEvent.loaded;
            // console.log(totalLength, downloadedLength);
            obj.skill = Math.round((downloadedLength / totalLength) * 100);
            // console.log(`Download Progress: ${progress}%`);
            // 在这里更新进度条或者其他 UI
            if(obj.skill===100){
                obj.showdown=false
            }
        }
    }).then(res => {
        const blob = new Blob([res.data]);
        let url = URL.createObjectURL(blob);
        const a = document.createElement('a')
        a.href = url
        a.download = filename
        a.click()

    }).catch(error => {
        ; // 异步操作失败时 reject Promise
    });

}


</script>
<style lang="scss" scoped>
.showdown {
    text-align: center;
    width: 240px;
    height: 50px;

    position: absolute;
    top: 200px;
    right: 185px;
}
</style>