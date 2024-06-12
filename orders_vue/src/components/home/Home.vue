<template>
    <v-sheet width="90%" style="margin: 0 auto;">
        <div>
            <v-carousel height="200" show-arrows="hover" cycle hide-delimiter-background interval="3000">
                <v-carousel-item v-for="(slide, i) in obj.carouseldata" :key="i" :src="slide.src">

                </v-carousel-item>
            </v-carousel>
        </div>
        <div class="mt-5">
            <div class="d-flex">
                <v-spacer></v-spacer>
                <div class="d-flex justify-start a ">
                    <div class="b">
                        <v-select v-model="obj.searchselect" class="text-body-2 ml-2" :items="['主题', '用户']"
                            density="compact" variant="plain"></v-select>
                    </div>
                    <div class="c">
                        <v-text-field v-model="obj.searchtext" variant="plain" density="compact">
                        </v-text-field>
                    </div>

                </div>
                <v-btn elevation="0" @click="handlesearch(obj.searchselect)">搜索</v-btn> <v-btn elevation="0"
                    @click="handleinit">清除筛选/排序</v-btn>
            </div>

        </div>
        <div class="ml-3">
            <div class="d-flex justify-start mt-3">
                <v-sheet width="20%" style="margin-top: 5px;">
                    类别
                </v-sheet><v-sheet width="100%" class="d-flex" ref="default1" style="flex-wrap: wrap;">
                    <span class="filter" @click="handlefilter($event, data, 'type')"
                        v-for="data in obj.headerstext.type" :key="data">{{ data }}</span>

                </v-sheet>
            </div>
            <div class="d-flex justify-start mt-3">
                <v-sheet width="20%" style="margin-top: 5px;">
                    完成期限
                </v-sheet><v-sheet width="100%" class="d-flex" style="flex-wrap: wrap;">
                    <span class="filter" @click="handlefilter($event, data, 'deadline')"
                        v-for="data in obj.headerstext.deadline" :key="data">{{ data }}</span>
                </v-sheet>
            </div>
            <div class="d-flex justify-start mt-3">
                <v-sheet width="20%" style="margin-top: 5px;">
                    发布日期
                </v-sheet><v-sheet width="100%" class="d-flex" style="flex-wrap: wrap;">
                    <span class="filter" @click="handlefilter($event, data, 'createdate')"
                        v-for="data in obj.headerstext.createdate" :key="data">{{ data }}</span>
                </v-sheet>
            </div>
            <div class="d-flex justify-start mt-3">
                <v-sheet width="20%" style="margin-top: 5px;">
                    悬赏金额
                </v-sheet><v-sheet class="d-flex" width="100%" style="flex-wrap: wrap;">
                    <span class="filter" @click="handlefilter($event, data, 'money')"
                        v-for="data in obj.headerstext.money" :key="data">{{ data }}</span>
                </v-sheet>
            </div>
            <div class="d-flex justify-start mt-3">
                <v-sheet width="20%">
                    排序
                </v-sheet>
                <v-sheet class=" " width="100%">
                    <span class="filter" @click="handlesort('date')">发布日期 <v-icon :icon="obj.dateicon"
                            size="20"></v-icon></span>
                    <span class="filter" @click="handlesort('money')">金额<v-icon :icon="obj.moneyicon"
                            size="20"></v-icon></span>
                </v-sheet>
            </div>
        </div>
        <div v-show="obj.search" class="mt-3 ml-3 mb-3"> 以下是对{{ obj.searchfalgselect }} :
            <strong>"{{ obj.searchfalgtext }}"</strong> 的搜索结果
        </div>

        
        <div class="mt-3 text-body-1 ">
            <Textindex :data="data" v-for="(data, index) in obj.orderslist" :key="index" />

        </div>


        <div ref="loadpage" class="text-center text-h6 mt-5">
            <div v-show="obj.isloading">
                <p><v-progress-circular color="primary" indeterminate></v-progress-circular></p>
                <p>LOADING......</p>
            </div>
            <div v-show="done == 'end' ? true : false">NOT MORE DATA</div>
        </div>
    </v-sheet>
</template>
<script setup>
import { reactive, onMounted, ref, watch, onUnmounted } from 'vue'
import api from '@/util/api'
import Textindex from '@/components/home/Textindex.vue'
import router from '@/router';
import def from '@/plugins/getdate'
import { useStore } from 'vuex';
 
const store=useStore()
const loadpage = ref()
const default1 = ref()
const done = ref(null)
const obj = reactive({
    searchselect: '主题', dateicon: 'mdi-sort-ascending', moneyicon: 'mdi-sort-ascending', search: false, searchfalgtext: '', searchfalgselect: '',
    searchtext: null,
    isloading: false,
    headerstext: {
        type: [],
        deadline: ['全部', '商议', '30天以上', '30-15天', '15-7天', '7天以下'],
        createdate: ['全部', '30天以上', '30-15天', '15-7天', '7天以下'],
        money: ['全部', '商议', '5000元以上', '5000-3000元', '3000-1000元', '1000元以下']
    },
    page: 1,
    carouseldata: [
        {
            src: 'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg',
        },
        {
            src: 'https://cdn.vuetifyjs.com/images/carousel/sky.jpg',
        },
        {
            src: 'https://cdn.vuetifyjs.com/images/carousel/bird.jpg',
        },
        {
            src: 'https://cdn.vuetifyjs.com/images/carousel/planet.jpg',
        },
    ],
    filterdict: {
        type: [], deadline: [], createdate: [], money: []
    },
    oldorderslist: [],
    orderslist: [

    ]

})
const handleinit = () => {
    location.reload();

}

const handlegetorders = async () => {
    // console.log(charfield, name)
    let formdata = new FormData()
    formdata.append('filterdict', JSON.stringify(obj.filterdict))
    formdata.append('page', obj.page)
    if (obj.search) {

        formdata.append('search', 'yes')
        formdata.append('stype', obj.searchselect)
        console.log(obj.searchselect)
        formdata.append('sname', obj.searchtext)
    }

    // formdata.append('name', name)
    await api.httptk.post('/filterdata', formdata).then(response => {
        console.log(response.data)
        obj.orderslist.push(...response.data.orderlist);
        // 按照createdate sort
        obj.orderslist.sort(function (a, b) {
            return b.createdate - a.createdate
        })
        if (response.data.page === 'end') {
            // 没有跟多数据了
            done.value = 'end'
        }
        console.log(obj.orderslist)
    })
    obj.isloading = false
}
const deletelist = (datalist, data) => {
    var list = []
    for (var a of datalist) {
        if (a !== data) {
            list.push(a)
        }
    }
    return list
}
const listappend = (data, type) => {

    // console.log(obj.filterdict[type].indexOf(data),data)
    if (obj.filterdict[type].indexOf(data) >= 0) {
        obj.filterdict[type] = deletelist(obj.filterdict[type], data)
    } else {
        obj.filterdict[type].push(data)
    }
    obj.orderslist = []
    done.value=null
    handlegetorders()
}


watch(() => obj.orderslist, () => {
    console.log('改变了', obj.orderslist)
})

const handlefilter = (e, data, type) => {
    //handlegetorders(type, data)
    // console.log(data,type)
    obj.page = 1
    listappend(data, type)
    // console.log(data, type)
    if (data === '全部') {

        var borther = e.target.parentNode.children//all borther element
        for (let n of borther) {
            n.classList.add('su')
        }
        // console.log(e.target.parentNode.childNodes)
    } else {
        const firstSibling = e.target.parentNode.children[0]
        firstSibling.classList.remove('su')//first borther element
        if (e.target.classList.contains('su')) {
            e.target.classList.remove('su')
        }
        else {
            e.target.classList.add('su')
        }
    }
}

onMounted(() => {
    // 在组件挂载后设置滚动事件监听器  
    window.addEventListener('scroll', checkElementInViewport);
    handlegetorders()
    console.log(default1.value.classList)
    console.log(store.state.type)
    api.http.get('/typehandle').then( res=>{
            console.log(res.data)
            obj.headerstext.type=['全部' ,...res.data.data ]
        }
    )
    

})
const handlesort = (type) => {
    switch (type) {
        case 'date':
            if (obj.dateicon === 'mdi-sort-ascending') {
                obj.orderslist.sort(function (a, b) {
                    obj.dateicon = 'mdi-sort-descending'
                    return a.createdate - b.createdate
                })
            } else {
                obj.dateicon = 'mdi-sort-ascending'
                obj.orderslist.sort(function (a, b) {
                    return b.createdate - a.createdate
                })
            }
            break
        case 'money':
            if (obj.moneyicon === 'mdi-sort-ascending') {
                obj.orderslist.sort(function (a, b) {
                    obj.moneyicon = 'mdi-sort-descending'
                    return a.money - b.money
                })
            } else {
                obj.moneyicon = 'mdi-sort-ascending'
                obj.orderslist.sort(function (a, b) {
                    return b.money - a.money
                })
            }
            break
    }
}
const handlesearch = () => {
    if (!obj.searchtext) {
        return
    }
    obj.orderslist = []
    obj.search = true
    obj.page = 1
    obj.searchfalgselect = obj.searchselect
    obj.searchfalgtext = obj.searchtext
    handlegetorders()

}

// 检查元素是否在视口内的函数  
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// 当元素进入视口时执行的函数  
function onElementInViewport() {
    if (loadpage.value && isInViewport(loadpage.value)) {
        // 在这里执行你需要的操作  
        // 如果你只想执行一次，可以取消滚动事件的监听器  
        // 但是，这可能会阻止其他依赖于滚动事件的代码正常工作  
        // window.removeEventListener('scroll', checkElementInViewport); 
        // console.log(obj.page,done.value,22222) 
        if (obj.isloading || done.value === 'end') {
            // if data loading or page is end ,return 
            return
        } else {
            obj.isloading = true
            obj.page++
            console.log(obj.page)
            handlegetorders(obj.page)
            console.log(obj.page)
        }



    }
}

// 滚动事件监听器  
function checkElementInViewport() {
    onElementInViewport();
}



// 在组件卸载前移除滚动事件监听器  
onUnmounted(() => {
    window.removeEventListener('scroll', checkElementInViewport);
});  
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