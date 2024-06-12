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

    })
    formdata.append('type', 'get')
    api.httpdetail.post('/orderfinish', formdata).then(res => {
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
            api.httpdetail.post('/gettext', formdata).then(response => {
                obj.text = response.data
            })
        }
        
        if (!order.files) {
            return
        }
        const downloadPromises = order.files.map(a => {
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
                    resolve();  
                }).catch(error => {
                    reject(error);  
                });
            });
        });

        Promise.all(downloadPromises).then(() => {
            obj.loading = false; 
             
        })
    })


})
const handicon = (name) => {
    const fileExtension = name.split('.').pop().toLowerCase();
    const file_formats = ['pdf', 'png', 'jpg', 'jpeg', 'gif', 'txt', 'rtf', 'html', 'xml', 'json', 'mp3', 'wav', 'wma', 'mp4', 'webm', 'ogg', 'aac', 'doc', 'docx', 'ppt', 'xlsx', 'zip', 'rar', 'glb', 'gltf', 'heic', 'heif']
    const isPreviewable = file_formats.includes(fileExtension);
    return isPreviewable
}


function handledrop(event) {
    event.preventDefault();
    event.stopPropagation()
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
const handlelist = () => {
    if (obj.text === '' && obj.textlistjson.length == 0) {
        console.log('asdasd')
        return
    }
    obj.skill = 0
    let data = new FormData()
    var T_Fdata = { text: [], files: [] }//text:[{,uuidname:'',index:x}],file:[{uuidname:'',filename:''}]
    for (var n in obj.textlistjson) {
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
            obj.skill = Math.round((downloadedLength / totalLength) * 100);
        }
    }).then(response => {
        if (response.data.code == 1) {
            router.push('/userhome/tproject')
        }

    }
    )
}
const previewFile = (file) => {
    if (!file) {
        return;
    }

    if (handicon(file.name)) {

        
        const url = URL.createObjectURL(file);
        window.open(url, '_blank');

        
    } else {
        const url = URL.createObjectURL(file);
        const a = document.createElement('a');
        a.href = url;
        a.download = file.name; 
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        URL.revokeObjectURL(url);
    }
};
const handledel = (data) => {
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