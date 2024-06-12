<template>
    <v-sheet class="stylepointer" width="90%" style="margin: 0 auto;" @click="handledetail(props.data.orderid)">
        <v-card width="100%" class="pa-3 mt-5">
            <div class="text-h4 textoverflow text-center">{{ props.data.title }}</div>
            <div class="mt-5">
                <p v-for="(text, index) in props.data.text_filename" :key="index" class="textoverflow"
                    v-show="text.type == 'text'">{{ text.content }} </p>
                <div v-for="(text, index) in props.data.text_filename" :key="index" v-show="text.type !== 'text'">
                    <v-icon icon="mdi-file-arrow-up-down-outline" color="orange-darken-1"></v-icon>
                    <span> {{text.content }}</span>
                </div>


            </div>
            <div class="d-flex justify-space-between mt-5">
                <div class="text-h6">类别： <span style="color: #4CAF50;">{{ props.data.type }}</span> </div>
                <div class="text-h6">期限： <span style="color: #4CAF50;">{{ obj.date   }}</span> </div>
                <div class="text-h6">金额： <span style="color: #4CAF50;">{{  props.data.money === 0 ? '商议' : props.data.money }}</span> </div>
            </div>
        </v-card>

    </v-sheet>


</template>
<script setup>
import { ref, onMounted, onBeforeMount, reactive } from 'vue'
import api from '@/util/api'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import def from '@/plugins/getdate'

const props = defineProps({
    data: {
        type: Object,
        required: true
    }
})
const router=useRouter()
const store = useStore()
const obj = reactive({
    mdi: '',date:null
})

onBeforeMount(() => {

    if(props.data.deadline<300){
        obj.date='商议'
    }else{
        obj.date=def.date(props.data.deadline)
    }

})

const handledetail=(id)=>{

    router.push({
        path: '/orderdetail', query: {
            orderid: id
        }
    })

}


</script>
<style lang="scss" scoped>
.a {
    border: 1px solid rgb(104, 103, 102);
    height: 40px;
    border-radius: 5px;
}

.b {
    width: 90px;
    background-color: #F5F5F5;
    border-radius: 8% 0% 0% 8%
}

.c {
    width: 200px;
}

.textoverflow {

    overflow: hidden;
    display: -webkit-box;
    /* 将对象作为弹性伸缩盒子模型显示 */
    -webkit-line-clamp: 1;
    /* 行数，值可以改，表示展示X行后多余的缩略展示 */
    -webkit-box-orient: vertical;
    /* 设置或检索伸缩盒对象的子元素的排列方式 */
    word-break: break-all;
    margin: 3px;
}

.stylepointer {
    cursor: pointer
}

.filter {
    margin: 5px 0px 0px 15px;
    cursor: pointer;
    flex-wrap: wrap;

}

.su {
    text-decoration: underline;
    color: rgb(69, 31, 221)
}
</style>