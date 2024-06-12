<template>
    <v-sheet width="100%" class="d-flex align-center" > 
        <v-icon :icon="obj.mdi" color="orange-darken-1"></v-icon>
        <span>{{ props.data.filename }}</span>
        <!-- <iframe ref="iframe" style="width: 100%; height: 600px;"></iframe> -->
        <v-spacer></v-spacer>
        <v-btn @click="openmydoc(obj.url)"  class="text-h6" elevation="0"> 
                <v-tooltip activator="parent" location="bottom" >查看</v-tooltip>
                <v-icon icon="mdi-fit-to-screen-outline" ></v-icon></v-btn>
            <v-btn @click="handledel(props.data)"  class="text-h6" elevation="0">
                <v-tooltip activator="parent" location="bottom" >删除</v-tooltip>
                <v-icon icon="mdi-trash-can-outline" color="error"></v-icon></v-btn>
    </v-sheet>
</template>
<script setup>
import { onMounted, reactive, ref } from 'vue'
// import Docxtemplater from "docxtemplater";
// import mammoth from "mammoth";

const emit=defineEmits(['fatherdef'])
const obj = reactive({
    preview: null,
    url: null,
    mdi:'',

})
const props = defineProps({
    data: null
})
const previewFile = (event) => {
    const file = event
    // console.log(file)
    if (file) {
        //file to url
        const reader = new FileReader();
        reader.onload = (e) => {
            const url = URL.createObjectURL(file);
            obj.url=url
    //   const iframe = preview.value;
        //   console.log(encodeURIComponent(obj.url))
   //   iframe.src = `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(url)}`;
        };
        reader.readAsDataURL(file);
      }
    };

onMounted(() => {
    // console.log(props.data)
    previewFile(props.data.file)
    // console.log(props.data.file.type.split('/'))
    if([ 'png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'psd', 'svg', 'tiff','image'].indexOf(props.data.file.type.split('/')[0])>=0){
        obj.mdi='mdi-image'
    }else if(['mp4', 'm2v', 'mkv','video'].indexOf(props.data.file.type.split('/')[0])>=0){
        obj.mdi='mdi-folder-play'
    }else{
        obj.mdi='mdi-file-arrow-up-down-outline'
    }

})
//open or loading file
function openmydoc(path) {
    window.open(path, '_blank')
}
const handledel=(data)=>{
    // console.log(data)
    emit('fatherdef',data)
}


</script>
<style></style>