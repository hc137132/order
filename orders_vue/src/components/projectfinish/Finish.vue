<template>
    <div style="margin: 0px auto;width: 90%;">
        <v-btn @click="router.back" color="primary" v-if="!props.orderid">break</v-btn>
        <div class="mt-5">
            <p class="text-h6">关于项目标题-- {{ obj.detail?.title }} 的提交</p>
            <p v-show="!obj.detail?.payment" class="text-body-2">对方未支付悬赏金额，无法查看提交内容</p>
        </div>
        <div>
            <p>提交说明</p>
            <p v-if="!props.orderid">
                <v-textarea v-model="obj.text" variant="outlined" @drop="handledrop($event)"
                    @dragover.prevent></v-textarea>
            </p>

            <v-btn v-if="!props.orderid"><v-icon icon="mdi-file-plus-outline" color="success" size="30"
                    onclick="document.getElementById('addfileField').click()"></v-icon> </v-btn>
            <input type="file" id="addfileField" @change="handgetfile" v-show="obj.bbb" multiple>
            <pre class="text-h6">{{ obj.text }}</pre>
            <p>
            <div v-for="a in obj.textlistjson" :key="a.filename" class="d-flex">
                <v-icon :icon="handlemdi(a.filename)" color="orange-darken-1"></v-icon>
                <span>{{ a.filename }}</span>
                <!-- <iframe ref="iframe" style="width: 100%; height: 600px;"></iframe> -->
                <v-spacer></v-spacer>
                <v-btn @click="previewFile(a.file)" class="text-h6" elevation="0" v-show="handicon(a.filename)">
                    <v-tooltip activator="parent" location="bottom">查看</v-tooltip>
                    <v-icon icon="mdi-fit-to-screen-outline"></v-icon></v-btn>
                <v-btn @click="previewFile(a.file)" class="text-h6" elevation="0" v-show="!handicon(a.filename)">
                    <v-tooltip activator="parent" location="bottom">下载</v-tooltip>
                    <v-icon icon="mdi-download-outline" size="30"></v-icon></v-btn>
                <v-btn @click="handledel(a)" class="text-h6" elevation="0" v-if="!props.orderid">
                    <v-tooltip activator="parent" location="bottom">删除</v-tooltip>
                    <v-icon icon="mdi-trash-can-outline" color="error"></v-icon></v-btn>

            </div>
            </p>
        </div>
        <div class="d-flex align-end justify-end" v-if="!props.orderid">
            <v-spacer></v-spacer>
            <div style="height:47px;margin-right: 10px;">
                <v-checkbox v-model="obj.finish" label="该项目是否完成" color="primary"></v-checkbox>
            </div>
            <v-btn @click="handlelist" class="text-h6" height="40" width="80" color="primary">提交</v-btn>

        </div>
        <div class="loading" v-if="obj.loading">
            <div style="text-align: center;">

                <div>
                    <v-progress-circular size="70" width="4" color="primary" indeterminate></v-progress-circular>
                </div>
                <p class="text-h6">File Loading...</p>
            </div>
        </div>

        <div class="upload" v-if="obj.skill != 0 && obj.skill != 100">
            <div style="text-align: center;">

                <div style="border-radius:5px ;overflow: hidden;">
                    <v-progress-linear color="primary" v-model="obj.skill" height="25">
                        <strong>{{ Math.ceil(obj.skill) }}%</strong>
                    </v-progress-linear>
                </div>
                <p class="text-h6">Uploading...</p>
            </div>
        </div>
        <div style="width:100%;border-top: 2px solid black;margin-top: 50px;"></div>
    </div>


</template>
<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import api from '@/util/api'
import { v4 as uuidv4 } from 'uuid'


const props = defineProps({
    orderid: null
})

const route = useRoute()
const router = useRouter()
const obj = reactive({
    orderid: null,
    detail: null, text: '',
    textlistjson: [], datajson: { text: null, file: [] },
    skill: 0,
    loading: false,
    flag: false, finish: false,


})

onMounted(() => {
    if (props.orderid) {
        obj.orderid = props.orderid

    } else if (route.query.orderid) {
        obj.orderid = route.query.orderid
    }

    obj.loading = true

    var formdata = new FormData()
    formdata.append('id', obj.orderid)
    api.httptk.post('getorderdetail', formdata).then(response => {
        obj.detail = response.data; // 更新 detail 为 API 响应的数据  
        console.log(response.data);

    })
    formdata.append('type', 'get')
    api.httpdetail.post('/orderfinish', formdata).then(res => {
        console.log(res.data.data)
        if (!res.data.data) {
            obj.loading = false;
            return
        }
        obj.flag = true
        obj.finish = res.data.finish
        let order = JSON.parse(res.data.data)

        if (order.text) {
            let formdata = new FormData()
            formdata.append('uuid', order.text)
            console.log(order.text)
            api.httpdetail.post('/gettext', formdata).then(response => {
                console.log(response.data)
                obj.text = response.data
            })
        }
        // obj.textlistjson.push(
        // { type: 'file', filename: file.name, file: file, size: file.size })
        // 创建一个用于存储 Promise 的数组 
        console.log(order.files)
        if (!order.files) {
            return
        }
        const downloadPromises = order.files.map(a => {
            // 使用箭头函数直接返回Promise，无需在外部声明download函数  
            return new Promise((resolve, reject) => {
                let formdata = new FormData();
                formdata.append('type', 'finish');
                formdata.append('uuidname', a.uuidname);
                api.httpdetail.post('/filedown', formdata, {
                    responseType: 'blob',
                }).then(response => {
                    const blob = new Blob([response.data]);
                    let fileType=null
                    if (['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'psd', 'svg', 'tiff', 'image'].indexOf(a.uuidname.split('.')[1]) >= 0) {
                         fileType = 'image/' + a.uuidname.split('.')[1]; 
                    } else {
                       fileType = 'application/' + a.uuidname.split('.')[1];
                    }
                    

                    const file = new File([blob], a.filename, { type: fileType });
                    obj.textlistjson.push({ type: 'file', filename: file.name, file: file, size: file.size });
                    resolve(); // 当文件下载并处理后，解决Promise  
                }).catch(error => {
                    reject(error); // 如果发生错误，拒绝Promise  
                });
            });
        });

        // 使用Promise.all等待所有downloadPromises都完成  
        Promise.all(downloadPromises).then(() => {
            // 所有文件都已下载并处理完成，可以在这里继续后续操作  
            obj.loading = false; // 假设您想在这里关闭加载状态  
            // ... 其他后续代码 ...  
        })
    })


})
const handicon = (name) => {
    const fileExtension = name.split('.').pop().toLowerCase();
    const file_formats = ['pdf', 'png', 'jpg', 'jpeg', 'gif', 'txt', 'rtf', 'html', 'xml', 'json', 'mp3', 'wav', 'wma', 'mp4', 'webm', 'ogg', 'aac', 'doc', 'docx', 'ppt', 'xlsx', 'zip', 'rar', 'glb', 'gltf', 'heic', 'heif']
    const isPreviewable = file_formats.includes(fileExtension); // 可以添加更多可预览的文件类型  

    return isPreviewable
}


function handledrop(event) {
    // event.stopPropagation();
    event.preventDefault();
    event.stopPropagation()
    console.log('success')
    const files = event.dataTransfer.items
    console.log(files)
    for (const file of files) {
        //  DataTransferItem 对象 
        const item = file.webkitGetAsEntry()
        if (item.isFile) {
            item.file((file) => {
                // 在这里你可以处理 File 对象的属性，例如 name, size, type 等
                obj.textlistjson.push(
                    { type: 'file', filename: file.name, file: file, size: file.size })

            })
        } else {
            uploadDirectory(item)
        }
    }
    console.log(obj.textlistjson)
}
function uploadDirectory(directory) {
    const reader = directory.createReader();
    reader.readEntries((entries) => {
        entries.forEach((entry) => {
            if (entry.isFile) {
                entry.file((file) => {
                    // 在这里你可以处理 File 对象的属性，例如 name, size, type 等
                    obj.textlistjson.push(
                        { type: 'file', filename: file.name, file: file, size: file.size })
                })
            } else if (entry.isDirectory) {
                uploadDirectory(entry);
            }
        });
    });
}
const handgetfile = (e) => {
    var a = null
    for (var n = 0; n < e.target.files.length; n++) {
        if (e.target.files[n].size < 2097152000) {
            obj.textlistjson.push(
                { type: 'file', filename: e.target.files[n].name, file: e.target.files[n], size: e.target.files[n].size })

        } else {
            obj.dialog = true//file size alter
        }
    }
}
//将预案textlistjson的list data 分类排序成一个新的list====datajson
const handlelist = () => {
    if (obj.text === '' && obj.textlistjson.length == 0) {
        console.log('asdasd')
        return
    }
    obj.skill = 0
    let data = new FormData()
    var T_Fdata = { text: [], files: [] }//text:[{,uuidname:'',index:x}],file:[{uuidname:'',filename:''}]
    for (var n in obj.textlistjson) {
        // console.log(obj.textlistjson[n].file.name.split('.').slice(-1))
        let filenewname = uuidv4() + '.' + obj.textlistjson[n].file.name.split('.').slice(-1)[0]
        data.append(filenewname, obj.textlistjson[n].file)
        T_Fdata.files.push({
            uuidname: filenewname, filename: obj.textlistjson[n].filename
        })
    }

    let textuuidname = uuidv4()
    T_Fdata.text = textuuidname
    data.append(textuuidname, obj.text)
    data.append('id', route.query.orderid)
    data.append('orderjson', JSON.stringify(T_Fdata))
    console.log(T_Fdata)
    if (obj.flag) {
        data.append('type', 'update')
    } else {
        data.append('type', 'create')
    }
    data.append('finish', obj.finish)

    api.httpdetail.post('/orderfinish', data, {
        onUploadProgress: (progressEvent) => {
            const totalLength = progressEvent.total;
            const downloadedLength = progressEvent.loaded;
            // console.log(totalLength, downloadedLength);
            obj.skill = Math.round((downloadedLength / totalLength) * 100);
        }
    }).then(response => {
        console.log(response.data)
        if (response.data.code == 1) {
            router.push('/userhome/tproject')
        }

    }
    )
}
const previewFile = (file) => {
    // console.log(file)
    if (!file) {
        return;
    }

    if (handicon(file.name)) {

        //file to url

        // 如果可以在浏览器中预览，创建一个Object URL并使用window.open 
        console.log(file)
        const url = URL.createObjectURL(file);
        window.open(url, '_blank');

        // 当新窗口/标签页关闭时，释放URL对象（可选，但推荐）  
        // window.addEventListener('unload', () => {
        //     URL.revokeObjectURL(url);
        // }, { once: true });
    } else {
        // 如果不能预览，触发下载  
        const url = URL.createObjectURL(file);
        const a = document.createElement('a');
        a.href = url;
        a.download = file.name; // 保持原始文件名（包括后缀）  
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        // 释放URL对象  
        URL.revokeObjectURL(url);
    }
};
const handledel = (data) => {
    // console.log(data)
    obj.textlistjson = obj.textlistjson.filter(res => res != data)
}
const handlemdi = (filename) => {
    if (['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'psd', 'svg', 'tiff', 'image'].indexOf(filename.split('.').slice(-1)[0]) >= 0) {
        return 'mdi-image'
    } else if (['mp4', 'm2v', 'mkv', 'video'].indexOf(filename.split('.').slice(-1)[0]) >= 0) {
        return 'mdi-folder-play'
    } else {
        return 'mdi-file-arrow-up-down-outline'
    }

}
</script>
<style lang="scss" scoped>
.loading {
    width: 100%;
    height: 100%;
    border: 1px solid black;
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0px;
    left: 0px;

    background-image: linear-gradient(to right, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.5));

    /* 使用backdrop-filter属性来模糊背景，但注意这可能会影响到性能 */
    backdrop-filter: blur(10px);
    background-color: rgba(248, 249, 248, 0.3);

}

.upload {
    position: absolute;
    display: flex;
    width: 100%;
    height: 100%;
    justify-content: center;
    align-items: center;
    top: 0px;
    left: 0px;
}
</style>