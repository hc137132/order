<template>
    <v-sheet >
        <v-img :src="obj.url" alt="" ></v-img>
        <v-sheet class="d-flex align-center">
        <div>
            <v-icon :icon="obj.mdi" color="orange-darken-1"></v-icon>
            <span> {{ props.data.filename }}</span>
           
        </div>
        <v-spacer></v-spacer>
        <div class="d-flex align-center justify-space-between">
            <v-card class="rounded-pill" width="100" v-if="obj.showdown">
            <v-progress-linear v-model="obj.skill" color="info" height="15">
                    <p class="text-body-2"> {{ Math.ceil(obj.skill) }}%</p>
                    </v-progress-linear>
                </v-card>
        
            <v-btn @click="handledown" elevation="0"> 下载</v-btn>
        
        </div>
         </v-sheet>
    </v-sheet>
</template>
<script setup>
import { reactive, onMounted } from 'vue';
import api from '@/util/api'
import { useStore } from 'vuex'
const store = useStore()

const props = defineProps({
    data: null
})
const obj = reactive({
    mdi: '', url: null,skill:0,
    showdown:false
})

onMounted(() => {
    // console.log(props.data.filename)
    if (['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'psd', 'svg', 'tiff', 'image'].indexOf(props.data.filename.split('.')[1]) >= 0) {

        handle()
        obj.mdi = 'mdi-image'
    } else if (['mp4', 'm2v', 'mkv', 'video'].indexOf(props.data.filename.split('.')[1]) >= 0) {
        obj.mdi = 'mdi-folder-play'
    } else {
        obj.mdi = 'mdi-file-arrow-up-down-outline'
    }

})

const handle = () => {
    return new Promise((resolve, reject) => {
        var formdata = new FormData()
        formdata.append('t_fid', props.data.uuidname)
        formdata.append('email', store.state.userdata.email)
        api.httpdetail.post('/getorderdetail', formdata,{
            responseType: 'blob',
            onDownloadProgress: (progressEvent) => {
                const totalLength = progressEvent.total;
                const downloadedLength = progressEvent.loaded;
                obj.skill = Math.round((downloadedLength / totalLength) * 100);
            }
        }).then(res => {
            const blob = new Blob([res.data]);
            obj.url = URL.createObjectURL(blob);
            resolve(); 
        }).catch(error => {
            reject(error); 
        });
    });
};

const  handledown= async()=>{
    obj.showdown=true
    obj.skill=0
    await handle()
    const a=document.createElement('a')
        a.href=obj.url
        a.download=props.data.filename
        a.click()   

}


</script>
<style lang="scss" scoped></style>