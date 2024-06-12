<template>
    <v-sheet  @click="handle" style="cursor:pointer">
    <div >
        <v-icon :icon="obj.mdi" color="orange-darken-1"></v-icon>
        <span > {{props.data.filename}}</span>
</div>
    </v-sheet>
</template>
<script setup>
import { reactive, onMounted } from 'vue';


const props = defineProps({
    data: null
})
const obj = reactive({
    mdi:'',
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


const handle=()=>{
    const file = props.data.file
    if (file) {
       
       const reader = new FileReader();
       reader.onload = (e) => {
           const url = URL.createObjectURL(file);
           window.open(url, '_blank')
       }
       reader.readAsDataURL(file)
     }
}


</script>
<style lang="scss" scoped >
   

</style>