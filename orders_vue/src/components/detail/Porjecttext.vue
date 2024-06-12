<template>
    <v-sheet >

        <v-card v-if="data.type === 'text'" class="mt-2" >
            <div class="ml-2 mr-2">
            <pre v-if="!obj.showretext" class="text-body-1" >{{ data.content }}</pre>
            <v-textarea variant="outlined" rows="3" row-height="15" counter v-model="data.content" v-if="obj.showretext"></v-textarea></div>
            <div class="text-end mb-1" style="overflow: auto;">
            <v-btn @click="handre(data)" :text="obj.btntext" elevation="0" class="text-h6 ">
                <v-tooltip activator="parent" location="bottom">{{obj.btntexttool}}</v-tooltip>
                <v-icon :icon="obj.btntext"></v-icon></v-btn>
            <v-btn @click="handDEL(data)" elevation="0" class="text-h6 " >
                <v-tooltip activator="parent" location="bottom">删除</v-tooltip>
                <v-icon icon="mdi-trash-can-outline" color="error"></v-icon></v-btn></div>
        </v-card>
        <v-sheet   v-if="data.type !== 'text'" class=" mt-2" height="100%">
            <Porjectfile @fatherdef="handDEL" :data="data"></Porjectfile>
        </v-sheet>
    </v-sheet>
</template>
<script setup>

import { onMounted, reactive } from 'vue'
import Porjectfile from './Porjectfile.vue';


const props = defineProps({
    data: Object,
   
})

const obj = reactive({
    showmp: false,
    showretext:false,
    btntext:'mdi-receipt-text-edit-outline',
    btntexttool:'编辑'
})
const emit = defineEmits(['func'])
//delete data function
function handDEL(index) {
    // console.log(index)
    emit('func', index)
}
function handre(index) {
    if(!obj.showretext){
        obj.showretext=true
        obj.btntext='mdi-check-bold'
        obj.btntexttool='确定'
    }else{
        obj.showretext=false
        obj.btntext='mdi-receipt-text-edit-outline'
        obj.btntexttool='编辑'
    }
    
}


</script>
<style lang="scss" scoped>
pre {
    word-wrap: break-word;
    white-space: pre-wrap;
}

</style>