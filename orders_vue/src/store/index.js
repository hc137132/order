import { createStore } from 'vuex'
import createPersistedstate from 'vuex-persistedstate' //安装数据持久化工具
import getdata from '@/plugins/getuserdata'

export default createStore({
  state: {
    userdata: {
      email: null,
      avatar: null,
      userid:null,
      date: null,
      introduction: null,
      phonenumber: null,
      nickname: '',
    },
    ws:null,
    loadingtext:0,test:0,
    loading: false,
    fileload:true,
    login:false,
    type: [],
    app:true,
    db:null,
    newmessagelist:[],
    messagelist:[
    //   {contact:'f38f8f333bf54dd09ae58a9f3e76e822',content:[
    //     // 这就是一条message
    //     {messageid:'',from:'f38f8f333bf54dd09ae58a9f3e76e822',to:'018b876360784ca2be96ac29b09b86ab',type:'text',content:'asdasdasd卡仕达',uuidname:'',unread:false,senddate: 1715578912,}] },
     ],
     createchat:false,
     openmessage:false,

  },
  getters: {
  },
  mutations: {
    createws(state,data){
      state.ws=data
    },
    test(state,data){
      state.test=data
      console.log('test success')
    },
    updatauser(state, data) {
      state.userdata = data
      // var arrf=['email','avatar','date','introduction','phonenumber','nickname']
      // arrf.forEach((key)=>{
      //   state.userdata.key=data[key]
      // }) 
    },
    typehandle(state, data) {
     
      for(var n in data){
        state.type.push(data[n].typename)
      }
    
    },
    login(state,data){
      state.login=data
    },
    getmessage(state,data){
      state.messagelist=data
    },
    updatemessage(state,data){
      // console.log(data)
      for(let a in state.messagelist){
        if(state.messagelist[a].contact==data.contact){
          state.messagelist[a].content==data.content
          // console.log(state.messagelist[a])
        }
      } 
      
    },
    addmessage(state,data){
     
      for(let a of state.messagelist){
        if(a.contact===data.a){
          a.content.push(data.b)
        return 
        }
      }
      
    },
  

    createchat(state,userdata){
      
      state.messagelist.unshift({contact:userdata.userid,content:[],userdata:userdata})
      // console.log({contact:userdata.userid,content:[],userdata:userdata})
    },
    createDB(state,data){
        state.db=data
    },
    openmessage(state){
      state.openmessage=!state.openmessage
    },
    filtermessage(state,str){
      if(str){
        let lsIN=state.messagelist.filter(item => item.userdata.email.includes(str))
        let lsNO=state.messagelist.filter(item => !item.userdata.email.includes(str))
        console.log(lsIN,lsNO)
        state.messagelist=[...lsIN, ...lsNO]
      }
    }
    
  },
  actions: {
  },
  modules: {
  },
  plugins: [
    // 持久化插件
    createPersistedstate({
      storage: window.sessionStorage,
      reducer(state) {
        return {
          // 只储存state中的dataList
          userdata: state.userdata,
          login:state.login

        }
      }
    })
  ],


})
