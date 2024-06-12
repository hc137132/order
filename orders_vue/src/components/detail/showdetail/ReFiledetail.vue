<template>
    <v-sheet  @click="handle" style="cursor:pointer">
    <div >
        <v-icon :icon="obj.mdi" color="orange-darken-1"></v-icon>
        <span > {{props.data.filename}}</span>
</div>
<v-dialog v-model="obj.dialog" max-width="600">
            <v-card>

                <v-img :src="obj.url" alt="" v-if="obj.mdi === 'mdi-image'"></v-img>
                <video :src="obj.url" autoplay controls v-if="obj.mdi === 'mdi-folder-play'"></video>

                <v-spacer></v-spacer>
                <div class="d-flex justify-end"> <v-btn variant="text" @click="obj.dialog = false" class="mr-5"><span
                            class="text-body-1">关闭</span></v-btn></div>


            </v-card>
        </v-dialog>
    </v-sheet>
</template>
<script setup>
import { reactive, onMounted } from 'vue';


const props = defineProps({
    data: null
})
const obj = reactive({
    mdi:'',url:'',dialog:false
})

onMounted(() => {
    if (['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'psd', 'svg', 'tiff', 'image'].indexOf(props.data.file.type.split('/')[0]) >= 0) {
        obj.mdi = 'mdi-image'
    } else if (['mp4', 'm2v', 'mkv', 'video'].indexOf(props.data.file.type.split('/')[0]) >= 0) {
        obj.mdi = 'mdi-folder-play'
    } else {
        obj.mdi = 'mdi-file-arrow-up-down-outline'
    }

})
const previewFile = (event) => {
    const file = event
    if (file) {
        //file to url
        const reader = new FileReader();
        reader.onload = (e) => {
            const url = window.URL.createObjectURL(file);
            obj.url = url
           
        };
        reader.readAsDataURL(file);
    }
};

const handle=()=>{
    obj.dialog=true
    previewFile(props.data.file)
    if (obj.mdi=== 'mdi-file-arrow-up-down-outline'){
        obj.dialog=false
        const a=document.createElement('a')
        a.href=obj.url
        a.download=props.data.filename
        a.click()   
    }
}


</script>
<style lang="scss" scoped >
   

</style>