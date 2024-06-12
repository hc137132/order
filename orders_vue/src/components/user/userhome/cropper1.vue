<template>
  <div class="d-flex align-center justify-space-around">
    <div class="img-container text-center d-flex align-center justify-center" @dragenter="enter" @drop="handledrop"
      @dragleave="leave" @dragover.prevent>
      <img :src="obj.url" v-show="obj.url" ref="image" style="max-width: 200px;max-height: 150px;">
      <v-sheet v-show="!obj.url">
        <v-icon icon="mdi-file-upload-outline" :size="obj.filesize"></v-icon>
        <p>拖拽此处上传</p>
      </v-sheet>

    </div>

    <v-sheet width="100" class="text-center">
      <div class="before" style="width: 100px;height: 100px;border-radius: 50% 50%;"> </div>
      <div class="d-flex align-center justify-space-around mt-3">

        <v-btn onclick="document.getElementById('aaaa').click()" color="primary" prepend-icon="mdi-file"> 选择文件</v-btn>
        <input type="file" id="aaaa" @change="changefile($event)" v-show="obj.aaa" />
        <v-btn @click="sureSava" prepend-icon="mdi-file" color="primary" class="ml-2">确定</v-btn>
      </div>

    </v-sheet>

    <!-- <img :src="obj.afterImg" alt=""> -->

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

// onMounted(() => {
//   init()
// }
// )


const changefile = (e) => {
  var file = e.target.files[0]
  if (!file) return;
  const reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onload = function (e) {
    obj.url = e.target.result
    // console.log(obj.url)
    // var url = e.result.substring(e.result.indexOf(",") + 1);
    // obj.url = "data:image/png;base64," + url;
    // that.$refs['imgimg'].setAttribute('src','data:image/png;base64,'+url);
    image.src = obj.url
    //判断是否创建实例，如果有就delete

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
    // autoCropArea: 1,//剪裁框和图片最窄边缘的比例（1为饱满
    ready: function () {
      // 显示当前裁剪框的位置和尺寸
      // console.log(obj.myCropper.getData());
    },
  })



  // console.log(obj.myCropper.getCanvasData())
}


function handledrop(event) {
  // event.stopPropagation();
  event.preventDefault();
  console.log('success')
  obj.filesize = 50
  const file = event.dataTransfer.files[0]
  // console.log(file)
  // obj.filename = file[0].name
  const reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onload = function (e) {
    obj.url = e.target.result
    // console.log(obj.url)
    // var url = e.result.substring(e.result.indexOf(",") + 1);
    // obj.url = "data:image/png;base64," + url;
    // that.$refs['imgimg'].setAttribute('src','data:image/png;base64,'+url);
    image.src = obj.url

    init()
    obj.myCropper.replace(image.src)


  }
}

function enter(event) {
  event.stopPropagation();
  event.preventDefault();
  obj.div = event.target//这一步是用来确定进入的div是谁，以确保进入子元素的时候样式不改变，
  // console.log('enter',)
  obj.filesize = 70
}
function leave(event) {
  event.stopPropagation();
  event.preventDefault();
  // console.log('leave',)
  //这一步就是验证是否离开进来的div时，也就是真正的离开，而不是进入子元素也改变
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

  // console.log(obj.afterImg)
  //child send father,second augrment is send value
  emit('geturl', obj.afterImg)
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.container {
  display: flex;
}

.before {
  width: 100px;
  height: 100px;
  overflow: hidden;
  /* 这个属性可以得到想要的效果 */
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
