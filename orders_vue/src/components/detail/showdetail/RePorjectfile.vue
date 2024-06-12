<template>
    <v-sheet width="100%" class="d-flex align-center">
        <v-icon :icon="obj.mdi" color="orange-darken-1"></v-icon>
        <span>{{ props.data.filename }}</span>
        <v-spacer></v-spacer>
 <v-progress-circular  class='mr-4' v-if="!props.data.file" color="green" indeterminate></v-progress-circular>
        <v-btn @click="openmydoc(obj.url)"  class="text-h6" elevation="0"   v-if="props.data.file">
            <v-tooltip activator="parent" location="bottom">查看</v-tooltip>
            <v-icon icon="mdi-fit-to-screen-outline"></v-icon>
           
        </v-btn>
        <v-btn @click="handledel(props.data)"  class="text-h6" elevation="0">
            <v-tooltip activator="parent" location="bottom">删除</v-tooltip>
            <v-icon icon="mdi-trash-can-outline" color="error"></v-icon></v-btn>


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
import { onMounted, reactive, ref } from 'vue'
// import Docxtemplater from "docxtemplater";
// import mammoth from "mammoth";

const emit = defineEmits(['fatherdef'])
const obj = reactive({
    preview: null, dialog: false,
    url: null,
    mdi: '',

})
const props = defineProps({
    data: null, skill: 100
})
const previewFile = (event) => {
    const file = event
    if (file) {
        //file to url
        const reader = new FileReader();
        reader.onload = (e) => {
            const url = window.URL.createObjectURL(file);
            obj.url = url
            //   const iframe = preview.value;
            //   console.log(encodeURIComponent(obj.url))
            //   iframe.src = `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(url)}`;
        };
        reader.readAsDataURL(file);
    }
};

onMounted(() => {
    previewFile(props.data.file)
    if (['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'psd', 'svg', 'tiff', 'image'].indexOf(props.data.filename.split('.').slice(-1)[0]) >= 0) {
        obj.mdi = 'mdi-image'
    } else if (['mp4', 'm2v', 'mkv', 'video'].indexOf(props.data.filename.split('.').slice(-1)[0]) >= 0) {
        obj.mdi = 'mdi-folder-play'
    } else {
        obj.mdi = 'mdi-file-arrow-up-down-outline'
    }

})
//open or loading file
function openmydoc(path) {
    obj.dialog = true
   if(obj.mdi==='mdi-file-arrow-up-down-outline'){
    obj.dialog=false
    const a=document.createElement('a')
        a.href=obj.url
        a.download=props.data.filename
        a.click()   


   }




}
const handledel = (data) => {
    emit('fatherdef', data)
}


</script>
<style></style>