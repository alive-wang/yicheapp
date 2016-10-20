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
today_day=new Date();
last_day=new Date();
week_before_day=new Date();
month_before_day=new Date();
quarter_before_day=new Date();
last_day.setDate(today_day.getDate()-1);
week_before_day.setDate(today_day.getDate()-7);
month_before_day.setDate(today_day.getDate()-30);
quarter_before_day.setDate(today_day.getDate()-90);
$("#7day").click(function(){
$("#datepicker").val(week_before_day.Format("yyyy-MM-dd"));
$("#datepicker1").val(last_day.Format("yyyy-MM-dd"));
});

$("#30day").click(function(){
$("#datepicker").val(month_before_day.Format("yyyy-MM-dd"));
$("#datepicker1").val(last_day.Format("yyyy-MM-dd"));
});

$("#90day").click(function(){
$("#datepicker").val(quarter_before_day.Format("yyyy-MM-dd"));
$("#datepicker1").val(last_day.Format("yyyy-MM-dd"));
});
});