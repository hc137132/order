<template>
  <v-sheet>
    <p>
      {{ obj.name }}
    </p>


  </v-sheet>
</template>

<script setup>
import { reactive, ref, onMounted, watch } from 'vue'
import api from '@/util/api'

const obj = reactive({
  name: ''

})
const props = defineProps({
  id: null,
})
onMounted(() => {
  if (props.id) {
    let data = new FormData()
    data.append('userid', props.id)
    api.httptk.post('/userdata', data).then(response => {
      console.log(response.data)
      obj.name = response.data.email
    })


  }


})


</script>

<style lang="scss" scoped></style>