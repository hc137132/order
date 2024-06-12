<template>
    <v-sheet width="100%" class="pl-3 pr-5">
        <v-dialog v-model="obj.overlay" persistent max-width="300" class="text-center">
            <span class="text-body-1">上传中</span>
            <v-card class="rounded-pill">

                <v-progress-linear v-model="obj.skill" color="info" height="25">

                    <strong>{{ Math.ceil(obj.skill) }}%</strong>

                </v-progress-linear>
            </v-card>
        </v-dialog>
        <v-dialog :model-value="obj.dialog">
            <v-card max-width="400">
                <v-card-title><v-icon icon="mdi-alert" color="warning"></v-icon> 警告</v-card-title>
                <v-card-text>
                    文件大小不超过20M，请重新选择文件
                </v-card-text>
                <template v-slot:actions>
                    <v-btn class="ms-auto" text="Ok" @click="obj.dialog = false"></v-btn>
                </template>
            </v-card>
        </v-dialog>

        <v-sheet class="elsticky">
            <v-sheet class="">
                <v-row class="">
                    <v-col md="6" sm="11" class="d-flex align-center justify-center">
                        <p class="text-subtitle-1">项目标题:</p>
                        <v-text-field variant="outlined" density="compact" v-model="obj.title"></v-text-field>
                    </v-col>
                    <v-col md="5" sm="11" class="d-flex align-center justify-cneter ">
                        <p class="text-subtitle-1">类别:</p><v-select density="compact" v-model="obj.selecttype"
                            :items="store.state.type" variant="outlined"></v-select>
                    </v-col>
                </v-row>
                <v-row class=" mt-n5">
                    <v-col md="6" sm="11" class="d-flex align-center justify-center ">

                        <p class="text-subtitle-1 text-center">完成时限：</p>
                        <v-menu v-model="obj.menu" :close-on-content-click="false" location="center">
                            <template v-slot:activator="{ props }">
                                <v-text-field variant="outlined" density="compact" v-bind="props" v-model="obj.newdate"
                                    :disabled="obj.checkdate" ></v-text-field>

                            </template>
                            <v-card min-width="300">
                                <v-date-picker v-model="obj.date" :min="obj.today"></v-date-picker>
                                <v-divider></v-divider>
                                <v-card-actions>
                                    <v-spacer></v-spacer>

                                    <v-btn variant="text" @click="obj.menu = false">
                                        关闭
                                    </v-btn>
                                    <v-btn color="primary" variant="text" @click="obj.menu = false">
                                        确定
                                    </v-btn>
                                </v-card-actions>
                                <div
                                    style="position:absolute;top: 0px;width:100%;height:19%;background-color: #673AB7;">
                                    <p class="text-body-1 mt-3 ml-5" style="color: aliceblue">请选择日期</p>
                                    <p class="text-h4 mt-3 ml-5" style="color: aliceblue">{{ obj.newdate }} {{ obj.week
                                        }}</p>
                                </div>
                                <div
                                    style="position:absolute;top: 27%;width:100%;height:7%;background-color: white;display: flex;align-items: center;justify-content: center">
                                    <div
                                        style="display: flex;align-items: center;justify-content: space-around;width:93%">

                                        <p style="color:#E53935;">日</p>
                                        <p>一</p>
                                        <p>二</p>
                                        <p>三</p>
                                        <p>四</p>
                                        <p>五</p>
                                        <p style="color:#E53935;">六</p>
                                    </div>
                                </div>
                               
                            </v-card>
                        </v-menu>

                        <v-checkbox color="primary" v-model="obj.checkdate" label="商议"></v-checkbox>
                    </v-col>
                    <v-col md="5" sm="11" class="d-flex align-center justify-cneter mt-n5">
                        <p class="text-subtitle-1">悬赏金额:</p>
                        <v-text-field density="compact" variant="outlined" label="￥" type="number" v-model="obj.money"
                            :disabled="obj.checkmoney"></v-text-field>
                        <v-checkbox v-model="obj.checkmoney" label="商议" color="primary"></v-checkbox>

                    </v-col>
                </v-row>
            </v-sheet>
            <v-sheet>
                <p class="text-subtitle-1">需求详情 <span class="text-body-2">（*文件和文件夹可直接拖拽入此文本框，文件大小不超过20M）</span></p>
                <v-textarea variant="outlined" rows="3" row-height="15" @dragenter="enter" @drop="handledrop($event)"
                    @dragleave="leave" v-model="obj.text" style="white-space:pre-wrap"></v-textarea>
            </v-sheet>

        </v-sheet>
        <v-sheet class="">
            <v-btn @click="handleaddtext" class="text-center text-subtitle-1 mr-2" elevation="0"><v-icon
                    icon="mdi-plus"></v-icon>
                段落</v-btn>
            <v-btn onclick="document.getElementById('addfileField').click()" class="text-subtitle-1" elevation="0">
                <v-icon icon="mdi-plus"></v-icon>
                文件</v-btn>
            <input type="file" id="addfileField" @change="handgetfile" v-show="obj.bbb" multiple>

        </v-sheet>

        <v-sheet class="d-flex justify-center overflow-auto">
            <v-sheet max-width="800" width="100%" class="overflow-auto">

                <!-- <draggable v-model="obj.textlistjson" @start="obj.drag = true" @end="obj.drag = false" item-key="id">
                    <template #item="{ element }">
                        <Text :data="element" @func="handDel" ></Text>
                    </template>
</draggable> -->
                <Text :data="data" @func="handDel" v-for="data in obj.textlistjson" :key="data.type"></Text>

            </v-sheet>
        </v-sheet>
        <v-sheet width="100%" class="d-flex align-end justify-end mt-5">
            <v-btn width="207" class="ml-2 text-subtitle-1" color="primary" @click="handleaddpro">发布任务</v-btn>
        </v-sheet>

        <v-dialog v-model="obj.senddialog" max-width="800" transition="dialog-bottom-transition">
            <v-card>


                <projectdetail :data="obj.datajson"></projectdetail>


                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text="取消" variant="text" @click="obj.senddialog = false"></v-btn>
                    <v-btn text="确定" variant="text" @click="affirmsend"></v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="obj.alertdialog" max-width="480">
            <v-card title="提示" color="#FFF176">
                <v-card-text>
                    <p>
                        &ensp;&ensp;&ensp;{{ obj.alerttext }} </p>
                </v-card-text>
                <v-card-actions>

                    <v-spacer></v-spacer>
                    <v-btn variant="text" @click="obj.alertdialog = false" class="mr-5"><span
                            class="text-body-1">确定</span></v-btn>

                </v-card-actions>
            </v-card>
        </v-dialog>

    </v-sheet>
</template>
<script setup>

import { reactive, onUpdated, watch, onMounted } from 'vue';
import Text from '@/components/detail/Porjecttext.vue'
import store from '@/store';
import api from '@/util/api'
import def from '@/plugins/getdate'
import { v4 as uuidv4 } from 'uuid'
import projectdetail from './Porjectdetail.vue'
import router from '@/router';




onMounted(() => {

    
    obj.today=def.date()
})

var obj = reactive({
    drag: false, menu: false, senddialog: false, fromdata: null,
    date: null, month: null, week: '',
    filename: '', selecttype: null,
    textlistjson: [], money: null,
    filesize: '',
    filescr: '',
    checkdate: false,
    checkmoney: false,
    date: null,
    newdate: null,
    menu: false,
    filelist: [], text: '',
    dialog: false,
    type: [],
    n: 0,
    alerttext: '', alertdialog: false,
    datajson: { title: '', date: null, money: null, type: '', text: [], file: [] },
    overlay: false, skill: 0,today:null
})

const sortarray=(list)=>{
if(list.length>0){
    let lista =list.sort((a, b) => a.index - b.index)
    for(let a in lista){
        lista[a].index=a
    }
    return lista
}

}
function handleaddtext() {

    if (obj.text !== '') {
        obj.textlistjson.push(
            { type: 'text', content: obj.text, index: obj.n }


        )
        obj.n++
    }
    obj.text = ''
}
const handlelist = () => {
    if (obj.checkdate) {
        obj.datajson.date = '商议'
    } else {
        obj.datajson.date = def.gettime(obj.date,obj.date)
    }

    obj.datajson.type = obj.selecttype
    obj.datajson.title = obj.title
    if (obj.checkmoney) {
        obj.datajson.money = null
    } else {
        obj.datajson.money = obj.money
    }

    obj.datajson.text = []
    obj.datajson.file = []
    for (var n in obj.textlistjson) {
        if (obj.textlistjson[n].type === 'text') {
            obj.datajson.text.push({
                content: obj.textlistjson[n].content,
                index: obj.textlistjson[n].index
            })
        } else {
            obj.datajson.file.push(
                { filename: obj.textlistjson[n].filename, file: obj.textlistjson[n].file, size: obj.textlistjson[n].size }
            )

        }


    }

}
function handDel(n) {
    obj.textlistjson = obj.textlistjson.filter(function (item) {
        return item != n
    })
}





function handledrop(event) {
    event.preventDefault();
    event.stopPropagation()
    obj.filesize = 40
    const files = event.dataTransfer.items
    for (const file of files) {
        const item = file.webkitGetAsEntry()
        if (item.isFile) {
            item.file((file) => {
                obj.textlistjson.push(
                    { type: 'file', filename: file.name, file: file, size: file.size })

            })
        } else {
            uploadDirectory(item)
        }
    }

}
function uploadDirectory(directory) {
    const reader = directory.createReader();
    reader.readEntries((entries) => {
        entries.forEach((entry) => {
            if (entry.isFile) {
                entry.file((file) => {
                    obj.textlistjson.push(
                        { type: 'file', filename: file.name, file: file, size: file.size })

                })
            } else if (entry.isDirectory) {
                uploadDirectory(entry);
            }
        });
    });
}
function enter(event) {
    event.stopPropagation();
    event.preventDefault();
    obj.filesize = 70
}
function leave(event) {
    event.stopPropagation();
    event.preventDefault();
    obj.filesize = 40
}
watch(() => obj.date, (newvalue, oldvalue) => {
    
    getdate(newvalue)

})

const getdate = (date) => {
    var year = new Date(date).getFullYear()
    var month = new Date(date).getMonth() + 1
    var day = new Date(date).getDate()
    var dayweek = new Date(date).getDay();
    var weeks = new Array("星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六");
    obj.week = weeks[dayweek]
    obj.month = month
    obj.newdate = year + '-' + month + '-' + day

}
const handgetfile = (e) => {
    var a = null

    for (var n = 0; n < e.target.files.length; n++) {
        if (e.target.files[n].size < 2097152000) {
            obj.textlistjson.push(
                { type: 'file', filename: e.target.files[n].name, file: e.target.files[n], size: e.target.files[n].size })

        } else {
            obj.dialog = true
        }

    }
}
const handleaddpro = () => {
    if (handlealert() === false) {
        obj.alertdialog = true
        return
    }
    var data = new FormData()
    data.append('email', store.state.userdata.email)
    data.append('title', obj.title)
    if (obj.checkdate) {
        data.append('date', 'None')
    } else {
        data.append('date', def.gettime(obj.date))
    }
    data.append('createdate', def.gettime(new Date()))//create date
    data.append('type', obj.selecttype)//project type
    if (obj.checkmoney) {
        data.append('money', 0)
    } else {
        data.append('money', obj.money)
    }
    var T_Fdata = { text: [], files: [] }//text:[{,uuidname:'',index:x}],file:[{uuidname:'',filename:''}]
    for (var n in obj.textlistjson) {
        if (obj.textlistjson[n].type === 'text') {
            let textname = uuidv4()
            data.append(textname, obj.textlistjson[n].content)
            T_Fdata.text.push({
                uuidname: textname, index: obj.textlistjson[n].index
            })
        } else {
            let filenewname = uuidv4() + '.' + obj.textlistjson[n].file.name.split('.').slice(-1)[0]
            data.append(filenewname, obj.textlistjson[n].file)
            T_Fdata.files.push({
                uuidname: filenewname, filename: obj.textlistjson[n].filename
            })
        }
    }
    T_Fdata.text=sortarray(T_Fdata.text)
    data.append('tfdata', JSON.stringify(T_Fdata))
    var reg1 = new RegExp("-", "g")
    data.append('orderid', uuidv4().replace(reg1, ""))
    obj.fromdata = data
    handlelist()
    obj.senddialog = true

}
const affirmsend = () => {

    obj.overlay = true
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/addorder', true);
    xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
            obj.skill = Math.round((e.loaded / e.total) * 100);
        }
    };
    xhr.onload = () => {
        if (xhr.status === 200) {
            obj.overlay = false
            router.push('/userhome/myproject')
        } else {
            console.error('Upload failed');
            router.push('/404')
        }
    };
    xhr.onerror = () => {
        console.error('An error occurred during the upload');
        router.push('/404')
    };
    xhr.onreadystatechange = function () {//Call a function when the state changes.
        if (xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {//xhr.readyState == 4等价于XMLHttpRequest.DONE

            var responseText = xhr.responseText;

            var obj = JSON.parse(responseText);
          
        }
    }

    xhr.send(obj.fromdata);
    obj.senddialog = false
    


}
const handlealert = () => {
    if (!obj.title) {
        obj.alerttext = '请输入项目标题'
        return false
    }
    if (!obj.selecttype) {
        obj.alerttext = '请选择项目类型'
        return false
    }
    if (obj.newdate === null && obj.checkdate === false) {
        obj.alerttext = "请选择完成时限"
        return false
    }
    if (obj.money === null && obj.checkmoney === false) {
        obj.alerttext = "请输入悬赏金额"
        return false
    }

    if (obj.textlistjson.length === 0) {
        obj.alerttext = '请描述项目需求'
        return false
    }
}
</script>
<style lang="scss" scoped>
.elsticky {
    position: sticky;
    top: 10px;
}

.d {
    position: absolute;
    top: 0px;
    width: 500px;
    height: 100px;

}
</style>
