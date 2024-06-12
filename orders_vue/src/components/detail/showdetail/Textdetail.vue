<template>
   <div class="text-body-2 text-start">
        <pre>
            {{props.data.content}}
        </pre>

   </div>
</template>
<script setup>
import { reactive,onMounted } from 'vue';


const props = defineProps({
    data: null
})
const obj=reactive({

})

</script>
<style lang="scss" scoped>


</style>