<template>
    <v-sheet width="200" class="ashow d-flex align-center justify-center mt-3 pl-1 rounded-lg"
        @contextmenu.prevent="handleRightClick">
        <v-sheet>
            
                <div class="av">
                    <v-img v-if="props.data.userdata.avatar" :src="'data:image/*;base64,' + props.data.userdata.avatar"
                        alt="John"></v-img>
                    <v-icon icon="mdi-account-circle" v-if="!props.data.userdata.avatar" size="50"
                        color="#42A5F5"></v-icon>
                </div>
            
        </v-sheet>
        <v-sheet class="text-start" width="110">
            <p class="text-start ellipsis ">{{ props.data.userdata.email }}</p>
        </v-sheet>
        <v-badge floating color="error" offset-x="5" v-show="props.unread != 0" offset-y="-15"
            :content="props.unread <= 10 ? props.unread : '9+'">
            <v-sheet height="100%"></v-sheet>
        </v-badge>
        <v-sheet width="15" height="15" class="mr-2"> <v-icon @click.stop="handledele" v-show="obj.menu"
                icon="mdi-close-circle-outline" size="25"></v-icon> </v-sheet>

    </v-sheet>
</template>
<script setup>
import { reactive, onMounted, watch, computed } from 'vue';
import api from '@/util/api'
import def from '@/plugins/getdate'
import { useStore } from 'vuex';

const props = defineProps({
    data: null, index: null, nowindex: null, unread: 0,
})
const store = useStore()
const obj = reactive({
    unread: 0,
    showunread: false, menu: false,

})

const handleread = () => {
    console.log()
    obj.unread = 0
    for (var a of props.data.content) {
        if (!a.unread && props.data.contact === a.to) {
            obj.unread++
        }
    }
    console.log(obj.unread)

}

watch(() => props.nowindex, () => {
    if (props.nowindex === props.index) {
        // 改变unread==true
        handlestoreunread(props.data)
    }

})


const handleRightClick = () => {
    obj.menu = !obj.menu

}
const handledele = () => {
    var newmessage = store.state.messagelist.filter(a => a !== props.data)
    store.commit('getmessage', newmessage)
}

const handlestoreunread = (data) => {
    var list = []
    if (data) {
        for (let a in data.content) {
            if (!data.content[a].unread) {
                var b = data.content[a]
                b.unread = true
                list.push(b)//改变store，
                // console.log('yes read')
                handleunread(data.content[a].messageid)//改变indexdb

            } else {
                list.push(data.content[a])
            }
        }
    }
    //    console.log({contact:data.contact,content:list})
    store.commit('updatemessage', { contact: data.contact, content: list })
}
// 消除 indexdb unread
const handleunread = (id) => {

    const request = indexedDB.open('message', 1)
    request.onsuccess = function (event) {
        const db = event.target.result;
        // 创建一个读写事务  
        const transaction = db.transaction(['message'], 'readwrite');
        const objectStore = transaction.objectStore('message');

        // 使用 get 方法根据主键查找数据  
        const getRequest = objectStore.get(id);

        getRequest.onsuccess = function (event) {
            const data = event.target.result;
            if (data) {
                // 修改数据  
                data.unread = true;
                // console.log(data.unread)
                //   使用 put 方法更新数据  
                const putRequest = objectStore.put(data);
                putRequest.onsuccess = function (event) {
                    // console.log('Data updated successfully');  
                };

                putRequest.onerror = function (event) {
                    console.error('Error updating data', event.target.errorCode);
                };
            } else {
                console.log('No data found for the given primary key');
            }
        };

        getRequest.onerror = function (event) {
            console.error('Error fetching data', event.target.errorCode);
        };

    }
}
</script>
<style lang="scss" scoped>
.ashow {
    box-shadow: none;
    border: none;
    height: 60px;
    transition: all 0.15s ease-in-out 0s;
    /* 延迟*/

}

.av {

    width: 50px;
    border-radius: 50%;
    overflow: hidden;
    transition: width 0.15s ease-in-out 0s;
    /* 延迟*/

}

.ashow:hover {
    box-shadow: 10px 5px 5px rgb(81, 130, 79);
    border: 1.5px solid rgb(13, 160, 72);
    height: 70px;

}

.ashow:hover .av {
    width: 60px;
}

.ellipsis {
    /* 设置文本在一行内显示 */
    white-space: nowrap;
    /* 当内容溢出容器时隐藏超出部分 */
    overflow: hidden;
    /* 当文本溢出时显示省略号 */
    text-overflow: ellipsis;

    /* 为了确保省略号显示，你可能还需要设置宽度或最大宽度 */
    width: 100%;
    /* 或者使用具体的像素值，例如 200px */
    /* 如果需要，你还可以设置 line-height 来控制行高 */
    line-height: 1.5;
}
</style>