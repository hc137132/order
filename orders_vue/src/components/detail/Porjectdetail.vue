<template>
    <v-sheet width="100%" class="pt-5 pl-3 pb-4 pr-5">
        <p class="text-center text-h4">{{props.data.title}}</p>
        <v-sheet class="text-body-1 mt-5 d-flex align-center justify-space-between "><div class=""><b>类别：</b>{{props.data.type}}</div>
            <div class="ml-2"><b> 完成时限：</b>{{obj.date}} </div>
            <div class="ml-2"><b>悬赏金额：</b> {{ props.data.money ? props.data.money+'元' :'商议'}}</div> 
        </v-sheet>
        <p class="mt-5"><b> 需求详情 </b></p>
            <v-sheet class="d-flex justify-center">
            
            <v-sheet width="90%">
               
                <pre v-for="data in props.data.text" class="mt-2">&nbsp;&nbsp;{{data.content}}</pre>

                <file v-for="data in props.data.file" :data="data"></file>

            </v-sheet>

        </v-sheet>

    </v-sheet>
</template>
<script setup>
import { reactive,onMounted } from 'vue';
import def from '@/plugins/getdate'
import Text from './Textdetail.vue'
import file from './Filedetail.vue'


const props = defineProps({
    data: null
})
const obj=reactive({
    date:null

})

onMounted(()=>{
    if(props.data.date==='商议'){
        obj.date=props.data.date

    }else{
        obj.date=def.date(props.data.date) 
    }


})



</script>
<style lang="scss" scoped>

pre {
    word-wrap: break-word;
    white-space: pre-wrap;
}
</style>