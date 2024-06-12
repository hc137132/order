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
//接收父data时，首先定义子data
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
  //define定义 child style
  obj.style=`position:relative;top:${obj.y}px;left:${obj.x}px`
})
//点击添加徽章

</script>
<style lang="scss" scoped>

</style>
