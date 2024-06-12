<template>
<v-sheet class="text-center" width="100%" style="margin-top: 100px;">
  
<p class="text-h3">404 Not Found</p>

<p class="text-h6 mt-5">Sorry, the page you requested could not be found.</p>

</v-sheet>

</template>

<script setup>
import store from '@/store';
import {onMounted,onUnmounted} from 'vue'

onMounted(()=>{
  store.state.app=false

})
onUnmounted(()=>{
  store.state.app=true


})

</script>
<style lang="scss" scoped>

</style>
