$(document).ready(function(){
 
Date.prototype.Format = function (fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
};

day_before=new Date()
day_after=new Date()
$("#day_before").click(function(){
var current_date=$("#datepicker").val();
var current_date = Date.parse(current_date);
var current_date = new Date(current_date);
day_before.setDate(current_date.getDate()-1);
$("#datepicker").val(day_before.Format("yyyy-MM-dd"));
});

$("#day_after").click(function(){
var current_date=$("#datepicker").val();
var current_date = Date.parse(current_date);
var current_date = new Date(current_date);
day_after.setDate(current_date.getDate()+1);
$("#datepicker").val(day_after.Format("yyyy-MM-dd"));
});

$("#transfer").click(function(){
var field1=$("#id_field1").val();
var field2=$("#id_field2").val();
var mid=field1;
$("#id_field1").val(field2);
$("#id_field2").val(mid);
});

});

