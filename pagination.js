$(document).ready(function() {  
    pageSize = 10 
	nowPag=1
   pageNation()
    // 注册分页操作的按钮点击事件  
    $("#first").click(pageNation);  
    $("#back").click(pageNation);  
    $("#next").click(pageNation);  
    $("#last").click(pageNation);  
  
});  
  
// 分页操作的函数  
var pageNation = function() {  
    // 获取所有的数据条数  
    countSize = $("#show tr").size();  
    // 获取总页数  
    countPage = Math.ceil(countSize / pageSize);  
    // 处理翻页的操作  
    if (this.nodeType == 1) {  
        var idValue = $(this).attr("id");  
        if ("first" == idValue) {  
 
            nowPag = 1;  
        } else if ("back" == idValue) {   
            if (nowPag > 1) {  
                nowPag--;  
            }  
  
        } else if ("next" == idValue) {  
            if (nowPag < countPage) {  
                nowPag++;  
            }  
        } else if ("last" == idValue) {   
            nowPag = countPage;  
        }  
  
    }  

    // 获取显示开始和结束的下标  
    starIndex = (nowPag - 1) * pageSize + 1;  
    endIndex = nowPag * pageSize;  
  
    if (endIndex > countSize) {  
		endIndex = countSize;  
    }  
	if (countSize < pageSize) {  
 
        endIndex = countSize;  
    }  
  
    if (starIndex == endIndex) {  
        // 显示的操作  
        $("#show tr:eq(" + (starIndex - 1) + ")").show();  
        $("#show tr:lt(" + (starIndex - 1) + ")").hide();  
    } else {  
        // 显示的操作  
        $("#show tr:gt(" + (starIndex - 1) + ")").show();  
        $("#show tr:lt(" + (endIndex - 1) + ")").show();  
  
        // 隐藏的操作  
        $("#show tr:lt(" + (starIndex - 1) + ")").hide();  
        $("#show tr:gt(" + (endIndex - 1) + ")").hide();  
    }   
	$("#pageInfo").text("第" + nowPag + "页"); 
};  