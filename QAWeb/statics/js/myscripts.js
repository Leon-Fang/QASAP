$(function(){
    var pathName = window.location.pathname;
    var reg = new RegExp("[0-9]+");
    var pageCounts = localStorage.getItem("totalPage");
    if(pathName.match(reg) != null){
        var pagination = parseInt(pathName.match(reg)[0]);
        if(pageCounts != pagination){
            console.log(pageCounts);
            console.log(pagination);
            $("li.morePage").prevAll().find("div").each(function(){
                $(this).find("a").remove();
                var aELe = $("<a class=\"page-link\"></a>").attr("href","/news/"+pagination+"/").text(pagination);
                $(this).append(aELe);
                pagination++;
            });
        };
        $("ul#paginationId").find("li").each(function(){
            if($(this).text() == pagination){
                $(this).addClass("active").siblings("li").removeClass("active");
            };
        });    
    };
    
});


$("div.list-group").find("a").click(function(){
    var newsTitle = $(this).find("h4").text();
    var newsCotent =  $(this).find("div#newsContents").text();
    $("h5.modal-title").text(newsTitle);
    $("div.modal-body").text(newsCotent);
});

$("ul#paginationId").find("li").click(function(){
    var currentPageIndex = parseInt($(this).siblings("li.active").text());
    var fisrtNum = $(this).prevAll().length;
    var lastNum = $(this).nextAll().length;
    var pageCounts = parseInt($("ul#paginationId").find("a.lastPage").text());
    localStorage.setItem('totalPage',pageCounts);
    if(currentPageIndex > 1){
        $("ul#paginationId").find("li:first").removeClass("disabled");
    }else{
        $("ul#paginationId").find("li:first").addClass("disabled");
    };

    if(fisrtNum === 0){
        if($(this).hasClass("disabled")){

        }else{
            $(this).siblings("li.active").prev().addClass("active").siblings("li").removeClass("active");
        }
    }

    if(lastNum === 0){
        $(this).addClass("disabled");
    }
    
    

});

$("div.page-item").find("a").click(function(){
    $(this).parents("li").addClass("active").siblings("li").removeClass("active");

});

$("li.morePage").find("div").on("click","a",function(){
   var prevNo =parseInt($("li.morePage").prev().text());
   $("li.morePage").prevAll().find("div a").each(function(){
      $(this).text(prevNo);
      $(this).attr("href","/news/"+prevNo+"/");
      prevNo++;
   });  
   localStorage.setItem('latestPage', prevNo); 
});

