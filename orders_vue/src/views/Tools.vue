<template>
  

<v-sheet :style="obj.style" width="0" height="0">
  <v-badge
          color="error"
          :content="obj.number"
          inline
        ></v-badge>
</v-sheet>

</template>

<script setup>
import {reactive,defineProps,onMounted} from 'vue'
const props = defineProps({
    data:null,
})
const obj=reactive({
  style:'position:relative;',
  x:'',
  y:'',
  number:'',
  datadict:null
})
onMounted(()=>{
  obj.x=props.data.x
  obj.y=props.data.y
  obj.number=props.data.number
  obj.style=`position:relative;top:${obj.y}px;left:${obj.x}px`
})

</script>
<style lang="scss" scoped>

</style>
