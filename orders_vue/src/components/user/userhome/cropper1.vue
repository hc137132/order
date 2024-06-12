<template>
  <div class="d-flex align-center justify-start">
    <div class="img-container text-center d-flex align-center justify-center mr-5 ml-5" @dragenter="enter" @drop="handledrop"
      @dragleave="leave" @dragover.prevent>
      <img :src="obj.url" v-show="obj.url" ref="image" style="max-width: 200px;max-height: 150px;">
      <v-sheet v-show="!obj.url">
        <v-icon icon="mdi-file-upload-outline" :size="obj.filesize"></v-icon>
        <p>拖拽此处上传</p>
      </v-sheet>

    </div>

    <v-sheet width="100" class="text-center ml-5">
      <v-sheet width="100%" class="d-flex justify-center">
      <div class="before " style="width: 100px;height: 100px;border-radius: 50% 50%;"> </div>
    </v-sheet>
      <div class="d-flex align-center justify-space-around mt-3">

        <v-btn onclick="document.getElementById('aaaa').click()" color="primary" prepend-icon="mdi-file"> 选择文件</v-btn>
        <input type="file" id="aaaa" @change="changefile($event)" v-show="obj.aaa" />
        <v-btn @click="sureSava" prepend-icon="mdi-file" color="primary" class="ml-2">确定</v-btn>
      </div>

    </v-sheet>


  </div>




</template>

<script setup>
import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.css'
import { reactive, onMounted, ref } from 'vue';
const emit = defineEmits(['geturl'])//default chlid send father

const obj = reactive({
  myCropper: null,
  afterImg: '',
  name: 'HelloWorld',
  url: null,
  filesize: 50,
  div: null,
})
const image = ref(null)




const changefile = (e) => {
  var file = e.target.files[0]
  if (!file) return;
  const reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onload = function (e) {
    obj.url = e.target.result
    image.src = obj.url

    init()
    obj.myCropper.replace(image.src)
  };



}



const init = () => {
  if (obj.myCropper) {
    obj.myCropper.destroy()
  }
  obj.myCropper = new Cropper(image.value, {
    viewMode: 1,
    dragMode: 'none',
    initialAspectRatio: 1,
    aspectRatio: 1,
    autoCrop: true,
    preview: '.before',
    background: false,
    autoCropArea: 0.6,
    zoomOnWheel: false,
    center: false,
    ready: function () {
    },
  })



}


function handledrop(event) {
  event.preventDefault();
  obj.filesize = 50
  const file = event.dataTransfer.files[0]
  const reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onload = function (e) {
    obj.url = e.target.result
    image.src = obj.url

    init()
    obj.myCropper.replace(image.src)


  }
}

function enter(event) {
  event.stopPropagation();
  event.preventDefault();
  obj.div = event.target
  obj.filesize = 70
}
function leave(event) {
  event.stopPropagation();
  event.preventDefault();
  if (event.target === obj.div) {
    obj.filesize = 50
  } else {

  }

}
const sureSava = () => {
  if (obj.myCropper) {
    obj.afterImg = obj.myCropper.getCroppedCanvas({
      imageSmoothingQuality: 'high'
    }).toDataURL('image/jpeg')
  }

  emit('geturl', obj.afterImg)
}


</script>

<style lang="scss" scoped>
.container {
  display: flex;
}

.before {
  width: 100px;
  height: 100px;
  overflow: hidden;
}

.img-container {
  height: 150px;
  width: 200px;
  overflow: hidden;
  border: 1px solid black;
}

.afterCropper {
  flex: 1;
  margin-left: 20px;
  border: 1px solid salmon;
  text-align: center;
}

.afterCropper img {
  width: 150px;
  margin-top: 30px;
}
</style>
