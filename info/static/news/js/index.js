var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据


$(function () {

    updateNewsData()
    // 首页分类切换
    $('.menu li').click(function () {
        var clickCid = $(this).attr('data-cid')
        $('.menu li').each(function () {
            $(this).removeClass('active')
        })
        $(this).addClass('active')

        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid

            // 重置分页参数
            cur_page = 1
            total_page = 1
            updateNewsData()
        }
    })

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 100) {
            // TODO判断页数，去更新新闻数据
            // console.log("bottom")
            if (!data_querying){
                data_querying = true

                if (cur_page < total_page){
                    cur_page += 1
                    updateNewsData()
                }
            }


        }
    })
})

function updateNewsData() {
    //TODO更新新闻数据
    var params = {
        "page": cur_page,
        "cid": currentCid,

    }

    $.get("/news_list", params, function (resp) {
        data_querying = false
        if(resp.errno == "0"){
            total_page = resp.data.total_page

            if(cur_page == 1){
                $(".list_con").html("")
            }

            for (var i=0;i<resp.data.news_dict_li.length;i++) {
                var news = resp.data.news_dict_li[i]
                var content = '<li>'
                content += '<a href="/news/' + news.id + '" class="news_pic fl"><img src="' + news.index_image_url + '?imageView2/1/w/170/h/170"></a>'
                content += '<a href="/news/' + news.id + '" class="news_title fl">' + news.title + '</a>'
                content += '<a href="/news/' + news.id + '" class="news_detail fl">' + news.digest + '</a>'
                content += '<div class="author_info fl">'
                content += '<div class="source fl">来源：' + news.source + '</div>'
                content += '<div class="time fl">' + news.create_time + '</div>'
                content += '</div>'
                content += '</li>'
                $(".list_con").append(content)
            }
        }else{
            alert(resp.errmsg)
        }
    })

}
