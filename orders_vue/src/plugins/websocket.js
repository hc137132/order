import store from '@/store'
import getdata from '@/plugins/getuserdata'
import api from '@/util/api'
const startchat = () => {

  store.commit('test', 222)

  var ws = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${store.state.userdata.userid}/`)
  ws.onopen = function (event) {
 
    store.commit('createws', ws)
    createDB()
  }
  ws.onmessage =async function (event) {

    if (JSON.parse(event.data).type === 'vretify'){
      ws.send(JSON.parse({type:'result',user:store.state.userdata.userid}))
    } else {
      if (JSON.parse(event.data).from === store.state.userdata.userid) {
        let formdata=new FormData()
        formdata.append('data',event.data)
        formdata.append('type','save')
        api.httptk.post('/message',formdata).then(
          response=>{

            
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
          store.commit('createchat', userdata)
        }
        flag=false
        DBadd(JSON.parse(event.data))
        store.commit('addmessage', { a: JSON.parse(event.data).from, b: JSON.parse(event.data) })
      }
    }

  }

}
const DBadd = (message) => {
  if (!store.state.db) {
    console.error('Database is not ready');
    return;
  }
  const tx = store.state.db.transaction(['message'], 'readwrite');
  const store1 = tx.objectStore('message');
  const request = store1.add(message)
  request.onsuccess = function (e) {
  }
  request.onerror = function (e) {
  }
}

const closechat = () => {

  store.state.ws.onclose = () => {
  };
  store.commit('createws', null)
}


let db = null
const createDB = () => {
  const request = indexedDB.open('message', 1);
  request.onupgradeneeded = function (event) {
    db = event.target.result;
    if (!db.objectStoreNames.contains('message')) {
      var objstore = db.createObjectStore('message', {
        keyPath: 'messageid', 
      });
      objstore.createIndex('from', 'from', { unique: false });
      objstore.createIndex('to', 'to', { unique: false });

    }
  };
  request.onsuccess = function (event) {
    db = event.target.result;
    store.commit('createDB', db)
    DBshow()

  };
  request.onerror = function (event) {
    console.error("Failed to open/upgrade database", event.target.error);
  };

}

const DBshow = async() => {
  let messagelist = []
  

  if (!db) {
    console.error('Database is not open yet.');
    return;
  }
let formdata=new FormData()
formdata.append('type','get')
formdata.append('userid',store.state.userdata.userid)
  await api.httptk.post('/message',formdata).then(response => {
  for(let a of response.data.chatls){
      DBadd(a)//add indexDB 
      messagelist.push(a)
  }
})
  const tx = db.transaction(['message'], 'readonly');
  const store1 = tx.objectStore('message');
  const indexFrom = store1.index('from');
  const indexTo = store1.index('to');
  indexFrom.openCursor().onsuccess = async function (event) {
    var cursor = event.target.result;
    if (cursor) {
      if (cursor.value.from === store.state.userdata.userid || cursor.value.to === store.state.userdata.userid) { // 使用 === 进行严格比较  
        messagelist.push(cursor.value)
      }
      cursor.continue(); 
    } else {
      await handlemessage(messagelist)
    }

  };
}

const handlemessage = async (list) => {
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

  var newmessagelist = []
  for (let b of userlist.filter(a => a !== store.state.userdata.userid)) {
    var lista = list.filter(res => res.from === b || res.to === b)
    lista.sort((a, b) => new Date(a.senddate) - new Date(b.senddate));
    newmessagelist.push({
      contact: b, content: lista, userdata: await getdata.getdata(b, false)
    })
  }
  store.commit('getmessage', newmessagelist)
}



export default { startchat, closechat }