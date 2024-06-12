//timestamp to date
function date(time){
    if(time){
        var date = new Date(time *1000);  // 参数需要毫秒数，所以这里将秒数乘于 1000

        var Y = date.getFullYear() + '-';
        var M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
        var D = date.getDate() + ' ';
        var h = date.getHours() + ':';
        var m = date.getMinutes() + ':';
        var s = date.getSeconds();
        var datetime=Y+M+D
        return datetime

    }else{
        var date = new Date();  // 参数需要毫秒数，所以这里将秒数乘于 1000

        var Y = date.getFullYear() + '-';
        var M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
        var D = date.getDate() + ' ';
        var h = date.getHours() + ':';
        var m = date.getMinutes() + ':';
        var s = date.getSeconds();
        var datetime=Y+M+D
        return datetime
    }
    
}
//date to timestamp
function gettime(date){
    let timestamp = Date.parse(new Date(date).toString());
    timestamp = timestamp / 1000; //时间戳为13位需除1000，时间戳为13位的话不需除1000
    

    return timestamp;
}
//date to timestamp
function gettimetime(time){
    if(time){
        var date = new Date(time *1000);  // 参数需要毫秒数，所以这里将秒数乘于 1000
        var h = date.getHours() + ':';
        var m = date.getMinutes()
        if(m<10){
            m='0'+m+ ':'
        }else{
            m=m+ ':'
        }


        var s = date.getSeconds();
        if(s<10){
            s='0'+s
        }
        var time=h+m+s
        return time

    }else{
        var date = new Date();  // 参数需要毫秒数，所以这里将秒数乘于 1000
        var h = date.getHours() + ':';
        var m = date.getMinutes() ;
        if(m<10){
            m='0'+m+ ':'
        }else{
            m=m+ ':'
        }
        var s = date.getSeconds();
        if(s<10){
            s='0'+s
        }
        var time=h+m+s
        return time
    }
}
export default {date,gettime,gettimetime}