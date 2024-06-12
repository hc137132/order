import store from '@/store'
import getdata from '@/plugins/getuserdata'
import api from '@/util/api'
const startchat = () => {

  store.commit('test', 222)

  //create websocket
  var ws = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${store.state.userdata.userid}/`)
  ws.onopen = function (event) {
    // 这个函数会在django self.accept()执行后触发
    console.log('websocket contact success')
    store.commit('createws', ws)
    createDB()
  }
  ws.onmessage =async function (event) {

    // 接收到消息后的操作receive a messaged operate
    console.log('receive a message', JSON.parse(event.data))
    // fisrt 不用判断是否是当前打开当前message dialog,unread==false ,add indexdb
    if (JSON.parse(event.data).type === 'vretify'){
      ws.send(JSON.parse({type:'result',user:store.state.userdata.userid}))//当类型等于验证时，返回自己的userid
    } else {
      if (JSON.parse(event.data).from === store.state.userdata.userid) {
        console.log('对方不在线')
        let formdata=new FormData()
        formdata.append('data',event.data)
        formdata.append('type','save')
        api.httptk.post('/message',formdata).then(
          response=>{console.log(response.data)
            
          }
        )
      } else {
        let flag = false
        for (let a of store.state.messagelist) {
          if (a.contact === JSON.parse(event.data).from) {
            flag = true
          }
        }
        if (!flag) {
         let userdata=await getdata.getdata(JSON.parse(event.data).from, false)
          console.log(userdata)
          store.commit('createchat', userdata)
        }
        flag=false
        DBadd(JSON.parse(event.data))
        //add store.state.messagelist
        store.commit('addmessage', { a: JSON.parse(event.data).from, b: JSON.parse(event.data) })
      }
    }

  }

}
//send消息receive or send a message add indexdb
const DBadd = (message) => {
  if (!store.state.db) {
    console.error('Database is not ready');
    return;
  }
  console.log(message)
  const tx = store.state.db.transaction(['message'], 'readwrite');
  const store1 = tx.objectStore('message');
  const request = store1.add(message)
  request.onsuccess = function (e) {
    console.log('Message added to IndexedDB successfully');
  }
  request.onerror = function (e) {
    console.log('indexDB error', e.target.error)
  }
}

const closechat = () => {

  store.state.ws.onclose = () => {
    console.log('已关闭')
  };
  store.commit('createws', null)
}


let db = null
const createDB = () => {
  // 创建一个打开数据库的请求  
  const request = indexedDB.open('message', 1);
  request.onupgradeneeded = function (event) {
    // 获取数据库实例  
    db = event.target.result;
    // 如果不存在，则创建名为message的对象存储  ,==数据表
    if (!db.objectStoreNames.contains('message')) {
      var objstore = db.createObjectStore('message', {
        keyPath: 'messageid', // 使用messageid作为主键  
      });
      // 创建索引（可选，用于快速查询）  
      // const messageStore = db.transaction('message', 'readwrite').objectStore('message');
      objstore.createIndex('from', 'from', { unique: false });
      objstore.createIndex('to', 'to', { unique: false });

    }
  };
  request.onsuccess = function (event) {
    // 数据库打开成功，确保db不是null  
    db = event.target.result;
    store.commit('createDB', db)//赋值到store
    //提取数据库聊天消息
    DBshow()
    console.log('indexDB open success')

  };
  request.onerror = function (event) {
    console.error("Failed to open/upgrade database", event.target.error);
  };

}

const DBshow = async() => {
  let messagelist = []
  

  // 确保数据库已打开  
  if (!db) {
    console.error('Database is not open yet.');
    return;
  }
// get django messsage
let formdata=new FormData()
formdata.append('type','get')
formdata.append('userid',store.state.userdata.userid)
  await api.httptk.post('/message',formdata).then(response => {
  console.log(response.data)
  for(let a of response.data.chatls){
      DBadd(a)//add indexDB 
      messagelist.push(a)
  }
})
  // 创建一个读写事务  
  const tx = db.transaction(['message'], 'readonly');
  const store1 = tx.objectStore('message');
  // 使用索引查询
  const indexFrom = store1.index('from');
  const indexTo = store1.index('to');
  indexFrom.openCursor().onsuccess = async function (event) {
    var cursor = event.target.result;
    // console.log(store.state.userdata)
    if (cursor) {
      if (cursor.value.from === store.state.userdata.userid || cursor.value.to === store.state.userdata.userid) { // 使用 === 进行严格比较  
        messagelist.push(cursor.value)
        // console.log(cursor.value)
      }
      cursor.continue(); // 继续到下一个条目  
    } else {
      console.log('All entries displayed.');
      await handlemessage(messagelist)
    }

  };
}
// {contact:'',content:[这就是一条message
// {from:'',to:'',type:'',content:'',uuidname:'',lookover:false,sendtime:}] }
// 第一步，筛选联系人，userlist[],在此之前，get 后端的message留言
// 第二步，create contact newmessagelist:{contact:'',content:[这就是一条message ]}
// 第三步，add messagelist newmessagelist:{contact:'',content:[{ from....}]}
const handlemessage = async (list) => {
  // first get userlist =[userA,userB,...]
  let userlist = []
  for (let a of list) {
    if (a.from === store.state.userdata.userid || a.to === store.state.userdata.userid) {
      if (!userlist.includes(a.from)) {
        userlist.push(a.from)
      }
      if (!userlist.includes(a.to)) {
        userlist.push(a.to)
      }

    }
  }

  console.log(userlist.filter(a => a !== store.state.userdata.userid))
  // second [{contact:userA,content:[{mesgaeid:....},{mesgaeid:....}]} ]
  var newmessagelist = []
  for (let b of userlist.filter(a => a !== store.state.userdata.userid)) {
    var lista = list.filter(res => res.from === b || res.to === b)
    lista.sort((a, b) => new Date(a.senddate) - new Date(b.senddate));
    newmessagelist.push({
      contact: b, content: lista, userdata: await getdata.getdata(b, false)
    })
  }
  console.log(newmessagelist)
  store.commit('getmessage', newmessagelist)
}



export default { startchat, closechat }