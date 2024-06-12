<template>
    <v-sheet >
        <p>{{ obj.aa }}</p>
    </v-sheet>
</template>
<script setup>


import api from '@/util/api'
import { reactive, onUpdated, onMounted, watch } from 'vue';


const obj = reactive({
    aa: '',
})
const props = defineProps({
    data: null,type:null
})

onMounted(() => {
    
    let formdata = new FormData();
    formdata.append('id', props.data.orderid);
    formdata.append('type', 'get');
    api.httpdetail.post('/orderfinish', formdata)
        .then(res => {
            if (res.data.finish && props.data.finish) {
                obj.aa='已完成'
            } else if (res.data.finish && ! props.data.finish){
                if(props.type==='getfinish'){
                        obj.aa='已提交'
                }else{
                    obj.aa='待确认'
                }
                
            } else {
                obj.aa='未完成'
            }
        })
      

})

</script>