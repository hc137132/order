<template>
    <v-sheet>
        <v-card height="350" width="300">
            <v-card-title>
                你将进行人机验证
            </v-card-title>
            <v-card-subtitle>
                请依次点击 <span v-for="text in obj.text" :key="text"> {{ text }}&nbsp</span>
            </v-card-subtitle>
            <v-card-text>
                

                <v-img @click="handel" cover width="280" height="180" :src="obj.url"></v-img>
                <!-- <img :src="obj.url" alt="" @click="handel"> -->
                <div class="success" v-show="obj.success">
                    <div style="width: 70px;height: 70px;overflow: hidden;border: 3px solid #4CAF50;border-radius: 50% 50%;">
                    <div style="position: relative;"> <v-icon icon="mdi-check-bold" color="success" size="60"></v-icon></div>
                   
                    <v-sheet class="show">
                        </v-sheet>
                     </div>
                    
                </div>

                <tools v-for="data in obj.complist" :key="data.number" :data="data" v-show="!obj.success"></tools>
                <p v-show="!obj.result"><v-icon icon="mdi-alert-circle-outline" color="error"></v-icon>验证失败,请重新验证</p>
            </v-card-text>

            <v-card-actions class="d-flex justify-end">
                <v-icon color="primary" icon="mdi-reload" @click="handlereload" class="aaa"></v-icon>
            </v-card-actions>

        </v-card>


    </v-sheet>
</template>
<script setup>
import { reactive, watch, onMounted } from 'vue'
import tools from '@/views/Tools.vue'
import http from '@/util/axiosfz.js';

const emit = defineEmits(['robotverify'])//default chlid send father
const obj = reactive({
    complist: [],
    style: 'position:relative;',
    url: '',
    result: true,
    text: null,
    position: null,
    indexlist: [0, 1, 2, 3],
    success:false,
    flag:1

})

const handel = (e) => {

    var x = e.pageX;
    var y = e.pageY - 10;//相对于浏览器
    var x = e.pageX - 10;
    var zx = e.offsetX//相对标签
    var zy = e.offsetY//减去图片的高度
    var data = { x: zx - 10, y: zy - 180 - 10, number: obj.complist.length + 1 }
    obj.complist.push(data)
    obj.style = `position:relative;top:${zy}px;left:${zx}px`
    // console.log(x, y, zx, zy, obj.complist)
    if (obj.complist.length === 4) {
        //verify
        obj.indexlist.forEach(ele => {
            if (obj.complist[ele].x + 10 <= obj.position[ele][0] + 20 && obj.complist[ele].x + 10 >= obj.position[ele][0] - 20 &&
            obj.complist[ele].y + 180+10 <= obj.position[ele][1] + 20 && obj.complist[ele].y +180 +10 >= obj.position[ele][1] - 20
            ) {
                obj.flag++
                if(obj.flag===5){

                    obj.result=true
                    obj.success=true
                }
            }else{
               obj.result=false
            }
        });
        //child send father,second augrment is send value
        emit('robotverify', obj.result)
    }
}

const handlereload = () => {
    obj.flag=1
    obj.complist.splice(0)
    http.get('/robotverify').then(response => {
        // console.log(response.data)
        obj.url = `data:image/png;base64,${response.data.image_data}`
        obj.text = response.data.text
        obj.position = response.data.position

    })
}
onMounted(() => {
    handlereload()
})

</script>

<style lang="scss" scoped>
.aaa {
    cursor: pointer; 


}
.success{
    position: absolute; top:80px;width: 290px;height: 190px;
     display: flex;left: -5px;
     align-items: center;
     justify-content: center;
     overflow: hidden;
    background-color: aliceblue;
    //  backdrop-filter: blur(5px);//磨砂背景效果
     
}   
.show{
    background-color:  aliceblue;;width: 300px;
            height: 300px;position: relative;top: -100%;
            transform: rotate(-30deg);
            animation: success 2.5s linear 1;
            transform-origin: top left;
            animation-fill-mode: both
}
@keyframes success
{
    from {transform: rotate(0deg)}
    to {transform: rotate(-90deg)}
}

</style>