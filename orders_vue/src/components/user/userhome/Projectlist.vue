<template>
    <v-sheet width="100%" height="100%">
        <v-sheet width="100%" height="80" class=" mt-5 d-flex align-self-start justify-start">

            <v-sheet width="100%" class="d-flex justify-start align-center" height="60">
                <v-btn class="text-h6  ml-5" @click="add" color="primary" height="50" width="130">
                    <v-icon icon="mdi-plus" size="30"></v-icon>发布任务</v-btn>
                <v-spacer></v-spacer>
                <div class="d-flex justify-start a">
                    <div class="b">
                        <v-select v-model="obj.searchselect" class="text-body-2 ml-2" :items="['主题', '金额', '接单用户']"
                            density="compact" variant="plain"></v-select>
                    </div>
                    <div class="c">
                        <v-text-field v-model="obj.searchtext" variant="plain" density="compact">
                        </v-text-field>
                    </div>

                </div>

                <v-btn elevation="0" @click="search">搜索</v-btn> <v-btn elevation="0"
                    @click="handleicon('', 'all')">清除筛选/排序</v-btn>
            </v-sheet>
        </v-sheet>
        <v-sheet min-height="400px">

            <v-table :hover="true" fixed-header>
                <thead fixed-header>

                    <tr class="text-h6">
                        <th>项目主题</th>
                        <th @click="handleicon(obj.dateicon, 'date')"> <span class="text-h6 stylebtn">发布日期</span>
                            <v-icon size="20" :icon="obj.dateicon"></v-icon>
                        </th>
                        <th>
                            <v-menu>
                                <template v-slot:activator="{ props }">
                                    <span v-bind="props" class="stylebtn">
                                        类型
                                    </span>
                                </template>
                                <v-list class="text-center">
                                    <v-list-item v-for="data in store.state.type" :key="data"
                                        @click="handleicon(data, 'type')">
                                        {{ data }}
                                    </v-list-item>
                                </v-list>
                            </v-menu>
                        </th>
                        <th>
                            <v-menu>
                                <template v-slot:activator="{ props }">
                                    <span v-bind="props" class="stylebtn">
                                        完成期限
                                    </span>
                                </template>
                                <v-list class="text-center">
                                    <v-list-item @click="handleicon('商议', 'deadline')" class="stylebtn">
                                        商议
                                    </v-list-item>
                                    <v-divider></v-divider>
                                    <v-list-item-title class="text-body-1 stylebtn"
                                        @click="handleicon(obj.deadlineicon, 'deadline')">已指定
                                        <v-icon :icon="obj.deadlineicon" size="20"></v-icon>
                                    </v-list-item-title>

                                </v-list>
                            </v-menu>
                        </th>
                        <th><v-menu>
                                <template v-slot:activator="{ props }">
                                    <span v-bind="props" class="stylebtn">
                                        悬赏金额
                                    </span>
                                </template>
                                <v-list class="text-center">
                                    <v-list-item @click="handleicon('商议', 'money')" class="stylebtn">
                                        商议
                                    </v-list-item>
                                    <v-list-item @click="handleicon(obj.moneyicon, 'money')"
                                        class="text-end stylebtn">已指定<v-icon :icon="obj.moneyicon"
                                            size="20"></v-icon></v-list-item>
                                </v-list>
                            </v-menu>
                        </th>
                        <th><v-menu>
                                <template v-slot:activator="{ props }">
                                    <span v-bind="props" class="stylebtn">
                                        接单情况
                                    </span>
                                </template>
                                <v-list class="text-center">
                                    <v-list-item>
                                        <v-list-item-title class="stylebtn"
                                            @click="handleicon('yes', 'takename')">已接单</v-list-item-title>
                                        <v-list-item-title class="stylebtn"
                                            @click="handleicon('No', 'takename')">未接单</v-list-item-title>
                                    </v-list-item>
                                </v-list>
                            </v-menu></th>
                        <th><v-menu>
                                <template v-slot:activator="{ props }">
                                    <v-btn elevation="0" v-bind="props" class="text-h6">
                                        完成情况
                                    </v-btn>
                                </template>
                                <v-list class="text-center">
                                    <v-list-item>
                                        <v-list-item-title class="stylebtn"
                                            @click="handleicon('Yes', 'finish')">已完成</v-list-item-title>
                                        <v-list-item-title class="stylebtn"
                                            @click="handleicon('No', 'finish')">未完成</v-list-item-title>
                                    </v-list-item>
                                </v-list>
                            </v-menu></th>
                        <th><v-menu>
                                <template v-slot:activator="{ props }">
                                    <v-btn elevation="0" v-bind="props" class="text-h6">
                                        订单支付
                                    </v-btn>
                                </template>
                                <v-list class="text-center">
                                    <v-list-item>
                                        <v-list-item-title class="stylebtn"
                                            @click="handleicon('Yes', 'payment')">已支付</v-list-item-title>
                                        <v-list-item-title class="stylebtn"
                                            @click="handleicon('No', 'payment')">未支付</v-list-item-title>
                                    </v-list-item>
                                </v-list>
                            </v-menu></th>
                        <th class="text-center">操作 </th>

                    </tr>
                </thead>
                <tbody>

                    <tr v-for="item in obj.datalist" :key="item.orderid" class="text-center stylebtn"
                        @click="handledetail(item)">
                        <td>
                            <div style="overflow: hidden;max-width:70px;white-space: nowrap;">{{ item.title }}</div>
                            <v-tooltip activator="parent" location="top" class="aa">{{ item.title }}</v-tooltip>
                        </td>
                        <td>{{ def.date(item.createdate) }}</td>
                        <td>{{ item.type }}</td>
                        <td>{{ orderdeadline(item.deadline) }}</td>
                        <td>{{ item.money === 0 ? '商议' : item.money }}</td>
                        <td><Getname :id="item.takename"/></td>
                        <td><div calss="d-flex align-center text-center"></div><ComFinish :data="item" type="getfinish"/></td>
                        <td>{{ !item.payment ? '未支付' : '已支付' }}</td>
                        <td>
                            <v-btn elevation="0" @click.stop="handledelete(item)"><v-icon icon="mdi-trash-can-outline"
                                    size="27" color="error"></v-icon><v-tooltip activator="parent"
                                    location="top">删除</v-tooltip></v-btn>
                        </td>
                    </tr>
                </tbody>
            </v-table>
        </v-sheet>
        <!-- 分页 -->
        <v-spacer></v-spacer>
        <v-sheet>

            <v-container>
                <v-pagination v-model="obj.page" :length="obj.pagelen" :total-visible="7"
                    color="primary"></v-pagination>
            </v-container>
        </v-sheet>
        <v-dialog v-model="obj.showdel" width="auto">
            <v-card max-width="400">
                <v-card-title>
                    <v-icon icon="mdi-alert" color="warning"></v-icon>
                    注意
                </v-card-title>
                <v-card-item>
                    项目删除后将不可恢复，请提前下载项目文件
                </v-card-item>
                <template v-slot:actions>
                    <v-spacer></v-spacer>
                    <v-btn class="ms-auto" text="确定" @click="dialog(obj.deldata)"></v-btn>
                    <v-btn class="ms-auto" text="取消" @click="obj.showdel = false"></v-btn>
                </template>
            </v-card>
        </v-dialog>
    </v-sheet>
</template>
<script setup>
// import { Session } from 'inspector';

import api from '@/util/api'
import def from '@/plugins/getdate'
import { reactive, onUpdated, onMounted, watch } from 'vue';
import { useStore } from 'vuex'
import { useRouter } from 'vue-router';
import Getname from '@/components/user/userhome/Getname.vue'
import ComFinish from './ComFinish.vue';


const store = useStore()
const router = useRouter()
const obj = reactive({
    aa: '', searchselect: '主题', searchtext: '',
    page: 1, pagelen: 0,
    width: 100,
    thead: ['项目主题', '发布日期', '分类', '完成期限', '悬赏金额', '承接用户', '完成进度', '操作'],
    datalist: [],
    resdatalist: [],
    dateicon: 'mdi-sort-ascending', lineicon: 'mdi-sort', moneyicon: 'mdi-sort-ascending', deadlineicon: 'mdi-sort-ascending',
    olddatalist: [], showdel: false,

})

onMounted(() => {
    // window.onresize = function () {
    //     //   console.log("宽度", document.documentElement.clientWidth);
    //     //   console.log("高度", document.documentElement.clientHeight);
    //     obj.width = document.documentElement.clientWidth
    // }
    // obj.width = document.documentElement.clientWidth
    var data = new FormData()
    data.append('email', store.state.userdata.email)
    api.httptk.post('/getorders', data).then(res => {
        console.log(res.data)
        obj.resdatalist = res.data.datalist
        obj.olddatalist = res.data.datalist
        //sort
        obj.resdatalist.sort(function (a, b) {
            return b.createdate - a.createdate
        })
        page()

    })

})
watch(() => obj.page, () => {
    page()
})
const orderdeadline=(date)=>{
    console.log(date)
    if(date===null || date===0 ||date===100){
        return '商议'
    }else{
        return def.date(date)
    }


}
const handleicon = (icon, item) => {
    switch (item) {
        case 'date':
            if (icon === 'mdi-sort-ascending') {
                obj.dateicon = 'mdi-sort-descending'
                obj.resdatalist.sort(function (a, b) {
                    return a.createdate - b.createdate
                })

            } else {
                obj.dateicon = 'mdi-sort-ascending'
                obj.resdatalist.sort(function (a, b) {
                    return b.createdate - a.createdate
                })

            }
            break
        case 'deadline':
            if (icon === '商议') {

                obj.resdatalist = obj.olddatalist.filter(x => x.deadline === 'None')
                // console.log(obj.resdatalist, obj.resdatalist.length)

            } else if (icon === 'mdi-sort-descending') {
                obj.deadlineicon = 'mdi-sort-ascending'
                obj.resdatalist = obj.olddatalist.filter(x => x.deadline !== 'None')
                obj.resdatalist.sort(function (a, b) {
                    return a.deadline - b.deadline
                })
            }
            else if (icon === 'mdi-sort-ascending') {
                obj.deadlineicon = 'mdi-sort-descending'
                obj.resdatalist = obj.olddatalist.filter(x => x.deadline !== 'None')
                obj.resdatalist.sort(function (a, b) {
                    return b.deadline - a.deadline
                })

            }

            break
        case 'type':
            obj.resdatalist = obj.olddatalist.filter(x => x.type === icon)
            break
        case 'money':
            if (icon === 'mdi-sort-ascending') {
                obj.moneyicon = 'mdi-sort-descending'
                obj.resdatalist.sort(function (a, b) {
                    return b.money - a.money
                })

            } else if (icon === 'mdi-sort-descending') {
                obj.moneyicon = 'mdi-sort-ascending'
                obj.resdatalist = obj.olddatalist.filter(x => x.money !== 0)
                obj.resdatalist.sort(function (a, b) {
                    return a.money - b.money
                })
                for (var n in obj.olddatalist.filter(x => x.money === 0)) {
                    obj.resdatalist.push(obj.olddatalist.filter(x => x.money === 0)[n])
                }

            } else {
                obj.resdatalist = obj.olddatalist.filter(x => x.money === 0)
            }

            break
        case 'takename':
            if (icon === 'No') {
                obj.resdatalist = obj.olddatalist.filter(x => x.takename === null)
            } else {
                obj.resdatalist = obj.olddatalist.filter(a => a.takename !== null)
            }
            break
        case 'finish':
            if (icon === 'No') {
                obj.resdatalist = obj.olddatalist.filter(x => x.finish === '' || x.finish===null)
            } else {
                obj.resdatalist = obj.olddatalist.filter(a => a.finish !== '' && a.finish !==null)
            }
            break

        case 'payment':
            if (icon === 'No') {
                obj.resdatalist = obj.olddatalist.filter(x => x.payment === '0')
            } else {
                obj.resdatalist = obj.olddatalist.filter(a => a.payment !== '0')
            }
            break

        case 'all':
            obj.resdatalist = obj.olddatalist
            handleicon('mdi-sort-descending', 'date')
            break

    }


    obj.page = 1
    page()
}

const page = () => {

    var len = obj.resdatalist.length
    // 总行数取余页面大小，等于0，则页数为整页数，否则有余数，则页数为正页数加一
    if (len % 7 == 0) {
        obj.pagelen = len / 7
    } else {
        obj.pagelen = Math.ceil(len / 7)
    }
    console.log(len, obj.pagelen)
    obj.datalist = obj.resdatalist.slice((obj.page - 1) * 7, (obj.page - 1) * 7 + 7)

}
function add() {
    router.push('/userhome/myproject/addproject')
}
onUpdated(() => {
    console.log(222)
})

const search = () => {
    if (!obj.searchtext) {
        obj.resdatalist = obj.olddatalist
        obj.page = 1
        page()
        return
    }
    obj.resdatalist = obj.olddatalist.filter((a) => {
        switch (obj.searchselect) {
            case '主题':
                if (a.title.includes(obj.searchtext)) {
                    return a
                }
                break
            case '金额':
                if (String(a.money).includes(obj.searchtext)) {
                    return a
                }
                break
            case '接单用户':
                if (a.taname && a.takename.includes(obj.searchtext)) {
                    return a
                }
                break
        }
    })
    obj.page = 1
    page()
}

const handledetail = (data) => {
    console.log(data)
    router.push({
        path: '/userhome/detail', query: {
            orderid: data.orderid
        }
    })

}
const handledelete = (data) => {
    obj.showdel = true
    obj.deldata = data
    console.log(data)
}
const dialog = (data) => {
    obj.showdel = false
    console.log(22222)
    var formdata = new FormData()
    formdata.append('oldorderid', data.orderid)
    formdata.append('email', store.state.userdata.email)
    api.httptk.post('/updataorder', formdata).then(res => {
        console.log(res.data)
        if (res.data.code === 0) {
            router.push('/404')

        } else {

            window.location.reload()

        }


    })
}
</script>
<style lang="scss" scoped>
.add {
    position: fixed;
    bottom: 50px;
}

.stylebtn {
    cursor: pointer
}

.thwidth {
    width: 50px;
}

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
</style>