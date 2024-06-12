<template>
  <div style="margin: 50px auto;width: 600px;">
    <div class="d-flex align-center"><v-sheet width="300" height="40">

        <v-text-field variant="outlined" density="compact" v-model="text">

        </v-text-field>
      </v-sheet>

      <v-btn color="primary" class="ml-3" @click="handleadd">添加</v-btn>
    </div>
    <div v-for="data in store.state.type" :key="data">
      <v-sheet width="300" class="d-flex align-center justify-space-between mt-3">
        <p>{{ data }}</p> <v-btn color="error" @click="handledelete(data)">删除</v-btn>
      </v-sheet>
    </div>


  </div>
</template>
<script setup>
import { ref } from 'vue'
import api from '@/util/api'
import { useStore } from 'vuex';

const store = useStore()
const text = ref('')
const handleadd = () => {
  let data = new FormData()
  data.append('text', text.value)
  data.append('type', 'add')
  api.http.post('/typehandle', data).then(response => {
    location.reload()
  })
}
const handledelete=(te)=>{
  let data = new FormData()
  data.append('text', te)
  data.append('type', 'delete')
  api.http.post('/typehandle',data).then(
  response=>{
    location.reload()
  }

  )


}

</script>